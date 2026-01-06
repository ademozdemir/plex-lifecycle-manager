#!/usr/bin/env python3
"""
Smart Plex Lifecycle Manager
============================
Intelligent content cleanup based on watch history, age, quality, and audio.

Features:
- Age-based cleanup (unwatched/watched rules)
- Rating-based cleanup
- Duplicate detection with NL audio priority
- Sonarr/Radarr integration (unmonitor)
- Smart TV show cleanup (entire series)
- Comprehensive reporting
"""

import os
import sys
import yaml
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class MediaItem:
    """Represents a media item (movie or show)"""
    title: str
    year: Optional[int]
    plex_id: str
    library_id: str
    library_name: str
    media_type: str  # 'movie' or 'show'
    file_path: str
    file_size_gb: float
    added_date: datetime
    last_viewed_date: Optional[datetime]
    view_count: int
    rating: Optional[float]
    resolution: Optional[str]
    video_codec: Optional[str]
    has_nl_audio: bool
    audio_tracks: List[str]
    guid: str  # For duplicate detection
    
    # For TV shows
    total_episodes: int = 0
    watched_episodes: int = 0
    
    # Cleanup decision
    should_delete: bool = False
    delete_reason: str = ""
    delete_priority: int = 0  # Higher = more urgent
    
    # Manual review flags
    requires_manual_review: bool = False  # TV shows need manual selection
    is_continuing: bool = False  # Series still ongoing (from Sonarr)
    auto_recommended: bool = False  # Movies auto-flagged, shows need manual check


@dataclass
class DeletionPlan:
    """Plan for items to delete"""
    timestamp: str
    total_items: int
    total_size_gb: float
    items_by_reason: Dict[str, int]
    items: List[MediaItem]


class PlexLifecycleManager:
    """Main lifecycle manager"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize manager with config"""
        self.config = self.load_config(config_path)
        self.plex = None
        self.sonarr = None
        self.radarr = None
        self.media_items: List[MediaItem] = []
        self.duplicates: Dict[str, List[MediaItem]] = defaultdict(list)
        
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML"""
        logger.info(f"Loading configuration from {config_path}")
        
        if not os.path.exists(config_path):
            logger.error(f"Config file not found: {config_path}")
            sys.exit(1)
            
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            
        logger.info("✓ Configuration loaded")
        return config
    
    def connect_services(self):
        """Connect to Plex, Sonarr, Radarr"""
        logger.info("=" * 80)
        logger.info("CONNECTING TO SERVICES")
        logger.info("=" * 80)
        
        # Connect to Plex
        try:
            from plexapi.server import PlexServer
            
            plex_url = self.config['plex']['url']
            plex_token = self.config['plex']['token']
            
            logger.info(f"Connecting to Plex at {plex_url}...")
            self.plex = PlexServer(plex_url, plex_token)
            logger.info(f"✓ Connected to Plex: {self.plex.friendlyName}")
            
        except ImportError:
            logger.error("plexapi not installed. Run: pip install plexapi")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Failed to connect to Plex: {e}")
            sys.exit(1)
        
        # Connect to Sonarr (optional)
        if self.config.get('sonarr', {}).get('enabled'):
            try:
                from pyarr import SonarrAPI
                sonarr_cfg = self.config['sonarr']
                self.sonarr = SonarrAPI(sonarr_cfg['url'], sonarr_cfg['api_key'])
                logger.info(f"✓ Connected to Sonarr at {sonarr_cfg['url']}")
            except ImportError:
                logger.warning("pyarr not installed. Sonarr integration disabled.")
                logger.warning("Install with: pip install pyarr")
            except Exception as e:
                logger.warning(f"Failed to connect to Sonarr: {e}")
        
        # Connect to Radarr (optional)
        if self.config.get('radarr', {}).get('enabled'):
            try:
                from pyarr import RadarrAPI
                radarr_cfg = self.config['radarr']
                self.radarr = RadarrAPI(radarr_cfg['url'], radarr_cfg['api_key'])
                logger.info(f"✓ Connected to Radarr at {radarr_cfg['url']}")
            except ImportError:
                logger.warning("pyarr not installed. Radarr integration disabled.")
                logger.warning("Install with: pip install pyarr")
            except Exception as e:
                logger.warning(f"Failed to connect to Radarr: {e}")
        
        logger.info("")
    
    def analyze_audio_tracks(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        Analyze audio tracks to detect NL/Dutch audio
        Returns: (has_nl_audio, list_of_languages)
        """
        try:
            import subprocess
            
            # Use ffprobe to get audio stream info
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_streams',
                '-select_streams', 'a',
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                logger.debug(f"Could not analyze audio for {file_path}")
                return False, []
            
            data = json.loads(result.stdout)
            languages = []
            has_nl = False
            
            for stream in data.get('streams', []):
                # Check language tag
                lang = stream.get('tags', {}).get('language', '').lower()
                if lang:
                    languages.append(lang)
                    
                # Check for Dutch
                if lang in ['nl', 'nld', 'dut', 'dutch']:
                    has_nl = True
                
                # Also check title for "Nederlands" or "Dutch"
                title = stream.get('tags', {}).get('title', '').lower()
                if 'nederlands' in title or 'dutch' in title or 'nl' in title:
                    has_nl = True
            
            return has_nl, languages
            
        except FileNotFoundError:
            logger.warning("ffprobe not found. Audio detection disabled.")
            logger.warning("Install with: apt-get install ffmpeg")
            return False, []
        except Exception as e:
            logger.debug(f"Error analyzing audio for {file_path}: {e}")
            return False, []
    
    def scan_library(self, library_config: Dict) -> List[MediaItem]:
        """Scan a library and create MediaItem objects"""
        lib_id = library_config['id']
        lib_name = library_config['name']
        lib_type = library_config['type']
        
        logger.info(f"\nScanning library: {lib_name} (ID {lib_id}, type: {lib_type})")
        
        try:
            section = self.plex.library.sectionByID(lib_id)
        except Exception as e:
            logger.error(f"Could not access library {lib_id}: {e}")
            return []
        
        items = []
        all_content = section.all()
        total = len(all_content)
        
        logger.info(f"Found {total} items in {lib_name}")
        
        for idx, content in enumerate(all_content, 1):
            if idx % 50 == 0:
                logger.info(f"  Processing {idx}/{total}...")
            
            try:
                if lib_type == 'movie':
                    item = self._process_movie(content, lib_id, lib_name)
                else:  # show
                    item = self._process_show(content, lib_id, lib_name)
                
                if item:
                    items.append(item)
                    
            except Exception as e:
                logger.warning(f"Error processing {content.title}: {e}")
                continue
        
        logger.info(f"✓ Processed {len(items)} items from {lib_name}")
        return items
    
    def _process_movie(self, movie, lib_id: str, lib_name: str) -> Optional[MediaItem]:
        """Process a movie into MediaItem"""
        try:
            # Get primary media file
            if not movie.media:
                return None
            
            media = movie.media[0]
            part = media.parts[0]
            file_path = part.file
            file_size_gb = part.size / (1024**3) if part.size else 0
            
            # Get dates
            added = movie.addedAt
            last_viewed = movie.lastViewedAt if movie.isWatched else None
            
            # Analyze audio
            has_nl, audio_langs = self.analyze_audio_tracks(file_path)
            
            # Get resolution and codec
            resolution = media.videoResolution if hasattr(media, 'videoResolution') else None
            codec = media.videoCodec if hasattr(media, 'videoCodec') else None
            
            item = MediaItem(
                title=movie.title,
                year=movie.year,
                plex_id=movie.ratingKey,
                library_id=lib_id,
                library_name=lib_name,
                media_type='movie',
                file_path=file_path,
                file_size_gb=round(file_size_gb, 2),
                added_date=added,
                last_viewed_date=last_viewed,
                view_count=movie.viewCount if hasattr(movie, 'viewCount') else 0,
                rating=movie.userRating if hasattr(movie, 'userRating') else None,
                resolution=resolution,
                video_codec=codec,
                has_nl_audio=has_nl,
                audio_tracks=audio_langs,
                guid=movie.guid
            )
            
            return item
            
        except Exception as e:
            logger.debug(f"Error processing movie {movie.title}: {e}")
            return None
    
    def _process_show(self, show, lib_id: str, lib_name: str) -> Optional[MediaItem]:
        """Process a TV show into MediaItem"""
        try:
            # Get all episodes
            episodes = show.episodes()
            total_eps = len(episodes)
            watched_eps = sum(1 for ep in episodes if ep.isWatched)
            
            # Get primary file from first episode for analysis
            if not episodes or not episodes[0].media:
                return None
            
            first_ep = episodes[0]
            media = first_ep.media[0]
            part = media.parts[0]
            
            # For shows, we use the show's directory as file_path
            file_path = str(Path(part.file).parent.parent)  # Go up to show dir
            
            # Calculate total size of all episodes
            total_size = 0
            for ep in episodes:
                if ep.media and ep.media[0].parts:
                    total_size += ep.media[0].parts[0].size or 0
            
            file_size_gb = total_size / (1024**3)
            
            # Get dates
            added = show.addedAt
            
            # Last viewed is most recent episode view
            last_viewed = None
            for ep in episodes:
                if ep.isWatched and ep.lastViewedAt:
                    if not last_viewed or ep.lastViewedAt > last_viewed:
                        last_viewed = ep.lastViewedAt
            
            # Analyze audio from first episode
            has_nl, audio_langs = self.analyze_audio_tracks(part.file)
            
            # Get resolution and codec from first episode
            resolution = media.videoResolution if hasattr(media, 'videoResolution') else None
            codec = media.videoCodec if hasattr(media, 'videoCodec') else None
            
            item = MediaItem(
                title=show.title,
                year=show.year if hasattr(show, 'year') else None,
                plex_id=show.ratingKey,
                library_id=lib_id,
                library_name=lib_name,
                media_type='show',
                file_path=file_path,
                file_size_gb=round(file_size_gb, 2),
                added_date=added,
                last_viewed_date=last_viewed,
                view_count=watched_eps,
                rating=show.userRating if hasattr(show, 'userRating') else None,
                resolution=resolution,
                video_codec=codec,
                has_nl_audio=has_nl,
                audio_tracks=audio_langs,
                guid=show.guid,
                total_episodes=total_eps,
                watched_episodes=watched_eps
            )
            
            return item
            
        except Exception as e:
            logger.debug(f"Error processing show {show.title}: {e}")
            return None
    
    def apply_rules(self):
        """Apply cleanup rules to all media items"""
        logger.info("\n" + "=" * 80)
        logger.info("APPLYING CLEANUP RULES")
        logger.info("=" * 80)
        
        now = datetime.now()
        
        for item in self.media_items:
            # Get rules for this library
            lib_config = next(
                (lib for lib in self.config['libraries'] if str(lib['id']) == str(item.library_id)),
                None
            )
            
            if not lib_config:
                continue
            
            rule_name = lib_config['rules']
            rules = self.config['rules'].get(rule_name, {})
            
            if item.media_type == 'movie':
                self._apply_movie_rules(item, rules, now)
            else:  # show
                self._apply_show_rules(item, rules, now)
    
    def _apply_movie_rules(self, item: MediaItem, rules: Dict, now: datetime):
        """Apply rules to a movie"""
        age_days = (now - item.added_date).days
        age_years = age_days / 365.25
        
        # Rule 1: Unwatched + old
        if item.view_count == 0:
            threshold = rules.get('unwatched_age_years', 5)
            if age_years > threshold:
                item.should_delete = True
                item.auto_recommended = True  # Movies are auto-flagged
                item.delete_reason = f"Unwatched for {age_years:.1f} years (threshold: {threshold}y)"
                item.delete_priority = 3
                return
        
        # Rule 2: Watched but old view
        if item.view_count > 0 and item.last_viewed_date:
            days_since_view = (now - item.last_viewed_date).days
            years_since_view = days_since_view / 365.25
            threshold = rules.get('watched_age_years', 2)
            
            if years_since_view > threshold:
                item.should_delete = True
                item.auto_recommended = True  # Movies are auto-flagged
                item.delete_reason = f"Last watched {years_since_view:.1f} years ago (threshold: {threshold}y)"
                item.delete_priority = 2
                return
        
        # Rule 3: Low rating + age
        if item.rating and item.rating < rules.get('low_rating_threshold', 3):
            threshold = rules.get('low_rating_age_years', 1)
            if age_years > threshold:
                item.should_delete = True
                item.auto_recommended = True  # Movies are auto-flagged
                item.delete_reason = f"Low rating ({item.rating}⭐) and {age_years:.1f} years old"
                item.delete_priority = 4
                return
        
        # Rule 4: Large file unwatched
        if item.view_count == 0 and item.file_size_gb > rules.get('large_file_gb', 50):
            threshold = rules.get('large_file_unwatched_years', 3)
            if age_years > threshold:
                item.should_delete = True
                item.auto_recommended = True  # Movies are auto-flagged
                item.delete_reason = f"Large file ({item.file_size_gb:.1f}GB) unwatched for {age_years:.1f} years"
                item.delete_priority = 5  # High priority - saves space
                return
    
    def _apply_show_rules(self, item: MediaItem, rules: Dict, now: datetime):
        """Apply rules to a TV show - ANALYSIS ONLY, no auto-flagging"""
        age_days = (now - item.added_date).days
        age_years = age_days / 365.25
        
        watch_percentage = (item.watched_episodes / item.total_episodes * 100) if item.total_episodes > 0 else 0
        
        # Check if continuing series
        is_continuing = False
        if self.sonarr and self._is_show_continuing(item.title):
            is_continuing = True
            item.is_continuing = True
            item.requires_manual_review = True
            item.delete_reason = "⚠️ Continuing series - Not recommended for deletion"
            item.delete_priority = 0  # Low priority, just for display
            logger.info(f"Marked {item.title} as continuing series in Sonarr")
            # DON'T return early! Series should appear in report (but disabled)
        
        # All TV shows require manual review
        item.requires_manual_review = True
        item.should_delete = False  # Never auto-flag TV shows!
        
        # If already marked as continuing, keep that reason and return
        if is_continuing:
            return
        
        # If not continuing, analyze against rules
        # Rule 1: Fully watched + old (ANALYSIS ONLY)
        if watch_percentage == 100 and item.last_viewed_date:
            days_since_view = (now - item.last_viewed_date).days
            years_since_view = days_since_view / 365.25
            threshold = rules.get('fully_watched_age_years', 0.5)
            
            if years_since_view > threshold:
                # Store reason for user info, but don't auto-flag
                item.delete_reason = f"📊 Analysis: Fully watched, last view {years_since_view:.1f} years ago"
                item.delete_priority = 2
                return
        
        # Rule 2: Completely unwatched + old (ANALYSIS ONLY)
        if watch_percentage == 0:
            threshold = rules.get('unwatched_age_years', 5)
            if age_years > threshold:
                item.delete_reason = f"📊 Analysis: Never watched, added {age_years:.1f} years ago"
                item.delete_priority = 3
                return
        
        # Rule 3: Partially watched + old (ANALYSIS ONLY)
        if 0 < watch_percentage < 100 and item.last_viewed_date:
            days_since_view = (now - item.last_viewed_date).days
            years_since_view = days_since_view / 365.25
            threshold = rules.get('partially_watched_age_years', 2)
            
            if years_since_view > threshold:
                item.delete_reason = f"📊 Analysis: {watch_percentage:.0f}% watched, abandoned {years_since_view:.1f} years ago"
                item.delete_priority = 4
                return
    
    def detect_duplicates(self):
        """Detect duplicate items and decide which to keep"""
        logger.info("\n" + "=" * 80)
        logger.info("DETECTING DUPLICATES")
        logger.info("=" * 80)
        
        if not self.config['duplicates']['enabled']:
            logger.info("Duplicate detection disabled in config")
            return
        
        # Group by title + year
        groups = defaultdict(list)
        for item in self.media_items:
            if not item.should_delete:  # Don't bother with already marked items
                key = f"{item.title}_{item.year}_{item.library_id}"
                groups[key].append(item)
        
        # Find groups with duplicates
        duplicate_count = 0
        for key, items in groups.items():
            if len(items) > 1:
                duplicate_count += 1
                self._resolve_duplicate_group(items)
        
        logger.info(f"✓ Found {duplicate_count} duplicate groups")
    
    def _resolve_duplicate_group(self, items: List[MediaItem]):
        """Decide which duplicate to keep"""
        logger.info(f"\nDuplicate found: {items[0].title} ({items[0].year})")
        
        nl_audio_priority = self.config['duplicates']['nl_audio_priority']
        
        # Sort by NL audio first, then quality
        def sort_key(item):
            # NL audio gets highest priority if enabled
            nl_score = 1000 if (nl_audio_priority and item.has_nl_audio) else 0
            
            # Quality score
            quality_map = {'2160p': 400, '1080p': 300, '720p': 200, '480p': 100}
            quality_score = quality_map.get(item.resolution, 0)
            
            # Codec score
            codec_map = {'hevc': 30, 'h265': 30, 'h264': 20, 'x264': 20}
            codec_score = codec_map.get(item.video_codec.lower() if item.video_codec else '', 0)
            
            # File size (smaller is slightly better if quality is same)
            size_penalty = item.file_size_gb * 0.1
            
            return nl_score + quality_score + codec_score - size_penalty
        
        # Sort items (highest score first = keep)
        sorted_items = sorted(items, key=sort_key, reverse=True)
        
        # Keep first (highest score), mark others for deletion
        keeper = sorted_items[0]
        
        for item in sorted_items[1:]:
            reason_parts = [f"Duplicate of better version"]
            
            if nl_audio_priority and keeper.has_nl_audio and not item.has_nl_audio:
                reason_parts.append("(other has NL audio)")
            elif keeper.resolution != item.resolution:
                reason_parts.append(f"(other is {keeper.resolution} vs {item.resolution})")
            
            item.should_delete = True
            item.delete_reason = " ".join(reason_parts)
            item.delete_priority = 6  # High priority for duplicates
            
            logger.info(f"  KEEP: {keeper.resolution} NL:{keeper.has_nl_audio} {keeper.file_size_gb}GB")
            logger.info(f"  DELETE: {item.resolution} NL:{item.has_nl_audio} {item.file_size_gb}GB - {item.delete_reason}")
    
    def _is_show_continuing(self, show_title: str) -> bool:
        """
        Check if a TV show is still continuing (more seasons coming) via Sonarr
        Returns True if show is "Continuing", False if "Ended" or not found
        """
        if not self.sonarr:
            return False  # No Sonarr = can't check, assume not continuing
        
        try:
            # Get all series from Sonarr
            all_series = self.sonarr.get_series()
            
            # Find matching series by title
            for series in all_series:
                sonarr_title = series.get('title', '').lower()
                if sonarr_title == show_title.lower():
                    # Check status
                    status = series.get('status', '').lower()
                    logger.debug(f"Sonarr status for {show_title}: {status}")
                    
                    # "continuing" = more seasons coming
                    # "ended" = series finished
                    return status == 'continuing'
            
            # Not found in Sonarr = assume not continuing
            logger.debug(f"{show_title} not found in Sonarr")
            return False
            
        except Exception as e:
            logger.warning(f"Error checking Sonarr status for {show_title}: {e}")
            return False  # On error, assume not continuing (safe to delete if other rules match)
    
    def _resolve_duplicate_group_OLD(self, items: List[MediaItem]):
        """Decide which duplicate to keep"""
        logger.info(f"\nDuplicate found: {items[0].title} ({items[0].year})")
        
        nl_audio_priority = self.config['duplicates']['nl_audio_priority']
        
        # Sort by NL audio first, then quality
        def sort_key(item):
            # NL audio gets highest priority if enabled
            nl_score = 1000 if (nl_audio_priority and item.has_nl_audio) else 0
            
            # Quality score
            quality_map = {'2160p': 400, '1080p': 300, '720p': 200, '480p': 100}
            quality_score = quality_map.get(item.resolution, 0)
            
            # Codec score
            codec_map = {'hevc': 30, 'h265': 30, 'h264': 20, 'x264': 20}
            codec_score = codec_map.get(item.video_codec.lower() if item.video_codec else '', 0)
            
            # File size (smaller is slightly better if quality is same)
            size_penalty = item.file_size_gb * 0.1
            
            return nl_score + quality_score + codec_score - size_penalty
        
        # Sort items (highest score first = keep)
        sorted_items = sorted(items, key=sort_key, reverse=True)
        
        # Keep first (highest score), mark others for deletion
        keeper = sorted_items[0]
        
        for item in sorted_items[1:]:
            reason_parts = [f"Duplicate of better version"]
            
            if nl_audio_priority and keeper.has_nl_audio and not item.has_nl_audio:
                reason_parts.append("(other has NL audio)")
            elif keeper.resolution != item.resolution:
                reason_parts.append(f"(other is {keeper.resolution} vs {item.resolution})")
            
            item.should_delete = True
            item.delete_reason = " ".join(reason_parts)
            item.delete_priority = 6  # High priority for duplicates
            
            logger.info(f"  KEEP: {keeper.resolution} NL:{keeper.has_nl_audio} {keeper.file_size_gb}GB")
            logger.info(f"  DELETE: {item.resolution} NL:{item.has_nl_audio} {item.file_size_gb}GB - {item.delete_reason}")
    
    def generate_report(self) -> DeletionPlan:
        """Generate cleanup report"""
        logger.info("\n" + "=" * 80)
        logger.info("GENERATING CLEANUP REPORT")
        logger.info("=" * 80)
        
        # Include items that:
        # 1. Should be deleted (movies auto-flagged), OR
        # 2. Require manual review AND have a delete reason (TV shows that match rules)
        items_to_delete = [
            item for item in self.media_items 
            if item.should_delete or (item.requires_manual_review and item.delete_reason)
        ]
        
        total_size = sum(item.file_size_gb for item in items_to_delete)
        
        # Group by reason
        by_reason = defaultdict(int)
        for item in items_to_delete:
            by_reason[item.delete_reason] += 1
        
        plan = DeletionPlan(
            timestamp=datetime.now().isoformat(),
            total_items=len(items_to_delete),
            total_size_gb=round(total_size, 2),
            items_by_reason=dict(by_reason),
            items=items_to_delete
        )
        
        # Print summary
        print("\n" + "=" * 80)
        print("CLEANUP SUMMARY")
        print("=" * 80)
        print(f"\nTotal items to delete: {plan.total_items}")
        print(f"Total space to free:   {plan.total_size_gb:,.2f} GB")
        print(f"\nBreakdown by reason:")
        print("-" * 80)
        
        for reason, count in sorted(by_reason.items(), key=lambda x: x[1], reverse=True):
            print(f"  {count:3d} items: {reason}")
        
        print("\n" + "=" * 80)
        
        # Save reports
        self._save_reports(plan)
        
        return plan
    
    def _save_reports(self, plan: DeletionPlan):
        """Save reports in multiple formats"""
        output_dir = Path(self.config['reporting']['output_dir'])
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON report
        if self.config['reporting']['generate_json']:
            json_file = output_dir / f"deletion_plan_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                # Convert MediaItems to dicts
                plan_dict = {
                    'timestamp': plan.timestamp,
                    'total_items': plan.total_items,
                    'total_size_gb': plan.total_size_gb,
                    'items_by_reason': plan.items_by_reason,
                    'items': [asdict(item) for item in plan.items]
                }
                json.dump(plan_dict, f, indent=2, default=str)
            logger.info(f"✓ JSON report saved: {json_file}")
        
        # CSV report
        if self.config['reporting']['generate_csv']:
            import csv
            csv_file = output_dir / f"deletion_plan_{timestamp}.csv"
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Title', 'Year', 'Library', 'Type', 'Size (GB)',
                    'Added Date', 'Last Viewed', 'View Count',
                    'Has NL Audio', 'Resolution', 'Rating',
                    'Delete Reason', 'Priority', 'File Path'
                ])
                
                for item in plan.items:
                    writer.writerow([
                        item.title,
                        item.year,
                        item.library_name,
                        item.media_type,
                        item.file_size_gb,
                        item.added_date.strftime('%Y-%m-%d'),
                        item.last_viewed_date.strftime('%Y-%m-%d') if item.last_viewed_date else 'Never',
                        item.view_count,
                        'Yes' if item.has_nl_audio else 'No',
                        item.resolution or 'Unknown',
                        item.rating or 'N/A',
                        item.delete_reason,
                        item.delete_priority,
                        item.file_path
                    ])
            
            logger.info(f"✓ CSV report saved: {csv_file}")
        
        # HTML report
        if self.config['reporting']['generate_html']:
            html_file = output_dir / f"deletion_plan_{timestamp}.html"
            self._generate_html_report(plan, html_file)
            logger.info(f"✓ HTML report saved: {html_file}")
    
    def _generate_html_report(self, plan: DeletionPlan, filepath: Path):
        """Generate nice HTML report"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Plex Cleanup Report - {plan.timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #e5a00d; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .summary-item {{ margin: 10px 0; font-size: 18px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #e5a00d; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f9f9f9; }}
        .nl-badge {{ background: #4CAF50; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; }}
        .priority-high {{ color: #d32f2f; font-weight: bold; }}
        .priority-med {{ color: #f57c00; }}
        .priority-low {{ color: #388e3c; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Plex Cleanup Report</h1>
        <p>Generated: {plan.timestamp}</p>
        
        <div class="summary">
            <div class="summary-item"><strong>Total items to delete:</strong> {plan.total_items}</div>
            <div class="summary-item"><strong>Total space to free:</strong> {plan.total_size_gb:,.2f} GB</div>
        </div>
        
        <h2>Breakdown by Reason</h2>
        <table>
            <tr><th>Reason</th><th>Count</th></tr>
"""
        
        for reason, count in sorted(plan.items_by_reason.items(), key=lambda x: x[1], reverse=True):
            html += f"<tr><td>{reason}</td><td>{count}</td></tr>\n"
        
        html += """
        </table>
        
        <h2>Items to Delete</h2>
        <table>
            <tr>
                <th>Title</th>
                <th>Year</th>
                <th>Library</th>
                <th>Size (GB)</th>
                <th>Added</th>
                <th>Last Viewed</th>
                <th>Views</th>
                <th>Audio</th>
                <th>Resolution</th>
                <th>Reason</th>
            </tr>
"""
        
        for item in sorted(plan.items, key=lambda x: x.delete_priority, reverse=True):
            priority_class = "priority-high" if item.delete_priority >= 5 else "priority-med" if item.delete_priority >= 3 else "priority-low"
            nl_badge = '<span class="nl-badge">NL</span>' if item.has_nl_audio else ''
            last_viewed = item.last_viewed_date.strftime('%Y-%m-%d') if item.last_viewed_date else 'Never'
            
            html += f"""
            <tr>
                <td><strong>{item.title}</strong></td>
                <td>{item.year or 'N/A'}</td>
                <td>{item.library_name}</td>
                <td>{item.file_size_gb:.2f}</td>
                <td>{item.added_date.strftime('%Y-%m-%d')}</td>
                <td>{last_viewed}</td>
                <td>{item.view_count}</td>
                <td>{nl_badge}</td>
                <td>{item.resolution or 'N/A'}</td>
                <td class="{priority_class}">{item.delete_reason}</td>
            </tr>
"""
        
        html += """
        </table>
    </div>
</body>
</html>
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def run_analysis(self):
        """Run full analysis (dry run)"""
        logger.info("=" * 80)
        logger.info("SMART PLEX LIFECYCLE MANAGER - ANALYSIS MODE")
        logger.info("=" * 80)
        
        # Connect to services
        self.connect_services()
        
        # Scan all configured libraries
        for lib_config in self.config['libraries']:
            items = self.scan_library(lib_config)
            self.media_items.extend(items)
        
        logger.info(f"\n✓ Total items scanned: {len(self.media_items)}")
        
        # Apply cleanup rules
        self.apply_rules()
        
        # Detect duplicates
        self.detect_duplicates()
        
        # Generate report
        plan = self.generate_report()
        
        logger.info("\n" + "=" * 80)
        logger.info("✓ ANALYSIS COMPLETE")
        logger.info("=" * 80)
        logger.info(f"\nReview the reports in: {self.config['reporting']['output_dir']}")
        logger.info("\n⚠ DRY RUN MODE - No files have been deleted")
        
        return plan


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Smart Plex Lifecycle Manager')
    parser.add_argument('--config', default='config.yaml', help='Path to config file')
    parser.add_argument('--mode', choices=['analyze', 'execute'], default='analyze',
                       help='Run mode: analyze (dry-run) or execute (actually delete)')
    
    args = parser.parse_args()
    
    manager = PlexLifecycleManager(args.config)
    
    if args.mode == 'analyze':
        manager.run_analysis()
    else:
        logger.error("Execute mode not yet implemented - coming soon!")
        logger.error("For now, use the generated deletion plan to manually delete files")
        sys.exit(1)


if __name__ == '__main__':
    main()
