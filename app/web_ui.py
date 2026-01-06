#!/usr/bin/env python3
"""
Plex Lifecycle Manager - Web UI
================================
Flask-based web interface for smart Plex cleanup
"""

import os
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from threading import Thread
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

# Import our cleanup logic
import sys
sys.path.insert(0, '/app')
from smart_cleanup import PlexLifecycleManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/logs/web_ui.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app)

# Paths
CONFIG_DIR = Path('/config')
REPORTS_DIR = Path('/reports')
LOGS_DIR = Path('/logs')

# Global state
current_analysis = {
    'running': False,
    'progress': 0,
    'status': 'idle',
    'log': []
}

# ============================================================================
# SCHEDULER MODULE (Optional - Safe Standalone)
# ============================================================================

# Try to import scheduler - if it fails, scheduler is simply disabled
scheduler = None
scheduler_enabled = False

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.cron import CronTrigger
    
    scheduler = BackgroundScheduler(daemon=True)
    scheduler_enabled = True
    logger.info("✓ Scheduler module loaded successfully")
except ImportError as e:
    logger.warning(f"⚠ Scheduler module not available: {e}")
    logger.warning("Scheduled analysis disabled - manual execution only")
except Exception as e:
    logger.error(f"✗ Scheduler initialization failed: {e}")
    logger.error("Scheduled analysis disabled - manual execution only")

def scheduled_analysis_job():
    """
    Background job for scheduled analysis
    Safe wrapper with error handling
    """
    global current_analysis
    
    try:
        # Check if analysis is already running
        if current_analysis['running']:
            logger.info("Scheduled analysis skipped - analysis already running")
            return
        
        logger.info("=" * 80)
        logger.info("SCHEDULED ANALYSIS STARTED")
        logger.info("=" * 80)
        
        # Load config to check if scheduling is enabled
        config_path = CONFIG_DIR / 'config.yaml'
        if not config_path.exists():
            logger.warning("Config not found - skipping scheduled analysis")
            return
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check if scheduling is enabled in config
        schedule_config = config.get('schedule', {})
        if not schedule_config.get('enabled', False):
            logger.info("Scheduled analysis is disabled in configuration")
            return
        
        # Run analysis in background
        thread = Thread(target=run_analysis_thread)
        thread.daemon = True
        thread.start()
        
        logger.info("Scheduled analysis thread started successfully")
        
    except Exception as e:
        logger.error(f"Scheduled analysis failed: {e}")
        logger.error("This error does not affect manual analysis")

def init_scheduler():
    """
    Initialize scheduler with config from schedule.yaml (SEPARATE file!)
    Safe - errors don't crash the application
    """
    global scheduler, scheduler_enabled
    
    if not scheduler_enabled:
        logger.info("Scheduler module not available - skipping initialization")
        return False
    
    try:
        # Load schedule config from SEPARATE file
        schedule_config = load_schedule_config()
        
        if not schedule_config.get('enabled', False):
            logger.info("Scheduled analysis is disabled in configuration")
            return False
        
        # Remove existing jobs
        if scheduler.running:
            scheduler.remove_all_jobs()
        
        # Parse schedule
        schedule_time = schedule_config.get('time', '03:00')  # Default: 3 AM
        schedule_days = schedule_config.get('days', 'daily')  # daily, weekly, monthly
        
        # Parse time (HH:MM format)
        try:
            hour, minute = map(int, schedule_time.split(':'))
        except:
            logger.error(f"Invalid schedule time format: {schedule_time}")
            hour, minute = 3, 0  # Default to 3 AM
        
        # Create cron trigger based on config
        if schedule_days == 'daily':
            trigger = CronTrigger(hour=hour, minute=minute)
            schedule_desc = f"daily at {schedule_time}"
        elif schedule_days == 'weekly':
            day_of_week = schedule_config.get('day_of_week', 'mon')  # monday default
            trigger = CronTrigger(day_of_week=day_of_week, hour=hour, minute=minute)
            schedule_desc = f"weekly on {day_of_week} at {schedule_time}"
        elif schedule_days == 'monthly':
            day_of_month = schedule_config.get('day_of_month', 1)  # 1st of month default
            trigger = CronTrigger(day=day_of_month, hour=hour, minute=minute)
            schedule_desc = f"monthly on day {day_of_month} at {schedule_time}"
        else:
            logger.error(f"Invalid schedule days: {schedule_days}")
            return False
        
        # Add job to scheduler
        scheduler.add_job(
            scheduled_analysis_job,
            trigger=trigger,
            id='scheduled_analysis',
            name='Scheduled Plex Cleanup Analysis',
            replace_existing=True
        )
        
        # Start scheduler if not running
        if not scheduler.running:
            scheduler.start()
            logger.info("✓ Scheduler started successfully")
        
        logger.info(f"✓ Scheduled analysis configured: {schedule_desc}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize scheduler: {e}")
        logger.error("Manual analysis will still work normally")
        return False

# ============================================================================
# END OF SCHEDULER MODULE
# ============================================================================


def get_config_path():
    """Get main config file path"""
    return CONFIG_DIR / 'config.yaml'


def get_schedule_config_path():
    """Get schedule config file path - SEPARATE from main config!"""
    return CONFIG_DIR / 'schedule.yaml'


def load_config():
    """Load main configuration (WITHOUT schedule)"""
    config_path = get_config_path()
    
    if not config_path.exists():
        # Return default config WITHOUT schedule
        default = get_default_config()
        default.pop('schedule', None)  # Remove schedule from default
        return default
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
            # Remove schedule if present (legacy)
            config.pop('schedule', None)
            return config
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        default = get_default_config()
        default.pop('schedule', None)
        return default


def load_schedule_config():
    """Load schedule configuration from SEPARATE file"""
    schedule_path = get_schedule_config_path()
    
    if not schedule_path.exists():
        # Return default schedule
        return {
            'enabled': False,
            'time': '03:00',
            'days': 'weekly',
            'day_of_week': 'mon',
            'day_of_month': 1
        }
    
    try:
        with open(schedule_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        logger.error(f"Failed to load schedule config: {e}")
        return {
            'enabled': False,
            'time': '03:00',
            'days': 'weekly',
            'day_of_week': 'mon',
            'day_of_month': 1
        }


def save_schedule_config(schedule_data):
    """Save schedule configuration to SEPARATE file - NEVER touches main config!"""
    schedule_path = get_schedule_config_path()
    
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
        with open(schedule_path, 'w') as f:
            yaml.dump(schedule_data, f, default_flow_style=False, sort_keys=False)
        logger.info("Schedule configuration saved to separate file")
        return True
    except Exception as e:
        logger.error(f"Failed to save schedule config: {e}")
        return False


def save_config(config):
    """Save main configuration - NEVER touches schedule (separate file!)"""
    config_path = get_config_path()
    
    try:
        CONFIG_DIR.mkdir(exist_ok=True)
        
        # Remove schedule from config if present (goes in separate file)
        config.pop('schedule', None)
        
        # Load existing config if it exists
        existing_config = {}
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    existing_config = yaml.safe_load(f) or {}
                    existing_config.pop('schedule', None)  # Remove legacy schedule
            except Exception as e:
                logger.warning(f"Could not load existing config: {e}")
        
        # Handle "cleanup" -> "rules" mapping (Web UI uses "cleanup", config uses "rules")
        if 'cleanup' in config:
            cleanup_data = config.pop('cleanup')
            # Start with existing rules
            if 'rules' in existing_config:
                config['rules'] = existing_config['rules'].copy()
            else:
                config['rules'] = {}
            # Update only the rules sent from frontend
            for rule_key, rule_value in cleanup_data.items():
                config['rules'][rule_key] = rule_value
        
        # Deep merge function
        def deep_merge(base, update):
            """Recursively merge update into base, preserving keys not in update"""
            result = base.copy()
            for key, value in update.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        
        # Start with existing config and deep merge new config
        merged_config = deep_merge(existing_config, config)
        
        # Ensure critical sections exist
        if 'libraries' not in merged_config:
            merged_config['libraries'] = []
            logger.warning("No libraries in config - will need to be configured")
        
        if 'rules' not in merged_config:
            merged_config['rules'] = get_default_config()['rules']
            logger.info("Added default rules to config")
        
        # Save merged config (WITHOUT schedule!)
        with open(config_path, 'w') as f:
            yaml.dump(merged_config, f, default_flow_style=False, sort_keys=False)
        
        logger.info("Main configuration saved (schedule is in separate file)")
        return True
    except Exception as e:
        logger.error(f"Failed to save config: {e}")
        return False


def get_default_config():
    """Get default configuration"""
    return {
        'plex': {
            'url': 'http://localhost:32400',
            'token': ''
        },
        'sonarr': {
            'enabled': False,
            'url': 'http://localhost:8989',
            'api_key': ''
        },
        'radarr': {
            'enabled': False,
            'url': 'http://localhost:7878',
            'api_key': ''
        },
        'rules': {
            'movies': {
                'unwatched_age_years': 5,
                'watched_age_years': 2,
                'low_rating_threshold': 3,
                'low_rating_age_years': 1,
                'large_file_gb': 50,
                'large_file_unwatched_years': 3
            },
            'kids_movies': {
                'unwatched_age_years': 5,
                'watched_age_years': 2,
                'low_rating_threshold': 3,
                'low_rating_age_years': 1,
                'large_file_gb': 50,
                'large_file_unwatched_years': 3
            },
            'tv_shows': {
                'fully_watched_age_years': 0.5,
                'unwatched_age_years': 5,
                'partially_watched_age_years': 2
            },
            'anime': {
                'fully_watched_age_years': 0.5,
                'unwatched_age_years': 5,
                'partially_watched_age_years': 2
            }
        },
        'duplicates': {
            'enabled': True,
            'nl_audio_priority': True,
            'quality_preference': ['2160p', '1080p', '720p', '480p'],
            'codec_preference': ['HEVC', 'H265', 'H264', 'x264']
        },
        'libraries': [
            {'id': 1, 'name': 'Movies', 'type': 'movie', 'rules': 'movies'},
            {'id': 2, 'name': 'KidsMovies', 'type': 'movie', 'rules': 'kids_movies'},
            {'id': 3, 'name': 'TV Shows', 'type': 'show', 'rules': 'tv_shows'},
            {'id': 4, 'name': 'KidsSeries', 'type': 'show', 'rules': 'tv_shows'},
            {'id': 5, 'name': 'Anime', 'type': 'show', 'rules': 'anime'}
        ],
        'execution': {
            'dry_run': True,
            'create_backup_list': True,
            'move_to_trash': False,
            'trash_folder': '/trash',
            'unmonitor_in_sonarr': True,
            'unmonitor_in_radarr': True,
            'delete_from_sonarr': False,
            'delete_from_radarr': False
        },
        'reporting': {
            'output_dir': '/reports',
            'generate_html': True,
            'generate_json': True,
            'generate_csv': True
        },
        'safety': {
            'min_free_space_gb': 100,
            'max_delete_percentage': 50,
            'require_confirmation': True
        },
        'logging': {
            'level': 'INFO',
            'file': '/logs/cleanup.log',
            'console': True
        },
        'schedule': {
            'enabled': False,
            'time': '03:00',
            'days': 'weekly',
            'day_of_week': 'mon',
            'day_of_month': 1
        }
    }


def run_analysis_thread():
    """Run analysis in background thread"""
    global current_analysis
    
    try:
        current_analysis['running'] = True
        current_analysis['progress'] = 0
        current_analysis['status'] = 'Initializing...'
        current_analysis['log'] = []
        
        # Load config
        config_path = get_config_path()
        if not config_path.exists():
            save_config(get_default_config())
        
        # Run analysis
        current_analysis['status'] = 'Running analysis...'
        current_analysis['progress'] = 10
        
        manager = PlexLifecycleManager(str(config_path))
        manager.run_analysis()
        
        current_analysis['progress'] = 100
        current_analysis['status'] = 'Analysis complete!'
        current_analysis['running'] = False
        
        logger.info("Analysis completed successfully")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        current_analysis['status'] = f'Error: {str(e)}'
        current_analysis['running'] = False


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration (combines main config + schedule from separate files)"""
    # Load main config
    config = load_config()
    
    # Load schedule from separate file
    schedule = load_schedule_config()
    
    # Combine for frontend (but they're saved separately!)
    config['schedule'] = schedule
    
    return jsonify(config)


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration (saves main config and schedule separately)"""
    try:
        config = request.json
        
        # Extract schedule data if present (goes to separate file!)
        schedule_data = config.pop('schedule', None)
        
        # Save main config (WITHOUT schedule)
        if not save_config(config):
            return jsonify({'success': False, 'message': 'Failed to save configuration'}), 500
        
        # Save schedule separately if provided
        if schedule_data is not None:
            if not save_schedule_config(schedule_data):
                logger.warning("Failed to save schedule config, but main config was saved")
            else:
                # Re-initialize scheduler with new config
                try:
                    if scheduler_enabled:
                        init_scheduler()
                except Exception as e:
                    logger.warning(f"Failed to re-initialize scheduler: {e}")
        
        # Try to auto-detect libraries if Plex credentials provided
        try:
            if config.get('plex', {}).get('url') and config.get('plex', {}).get('token'):
                auto_detect_libraries()
        except Exception as e:
            logger.warning(f"Library auto-detection failed: {e}")
            # Don't fail the whole save if auto-detection fails
        
        return jsonify({'success': True, 'message': 'Configuration saved'})
    except Exception as e:
        logger.error(f"Failed to update config: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def auto_detect_libraries():
    """Auto-detect Plex libraries and add to config"""
    try:
        config_path = get_config_path()
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        plex_url = config.get('plex', {}).get('url')
        plex_token = config.get('plex', {}).get('token')
        
        if not plex_url or not plex_token:
            return
        
        from plexapi.server import PlexServer
        plex = PlexServer(plex_url, plex_token)
        
        libraries = []
        for section in plex.library.sections():
            lib_type = 'movie' if section.type == 'movie' else 'show' if section.type == 'show' else None
            if lib_type:
                # Determine rule set based on library name
                lib_name_lower = section.title.lower()
                if 'kid' in lib_name_lower or 'child' in lib_name_lower:
                    rules = 'kids_movies' if lib_type == 'movie' else 'kids_series'
                elif 'anime' in lib_name_lower:
                    rules = 'anime'
                else:
                    rules = 'movies' if lib_type == 'movie' else 'tv_shows'
                
                libraries.append({
                    'id': int(section.key),
                    'name': section.title,
                    'type': lib_type,
                    'rules': rules
                })
        
        if libraries:
            # Use save_config to properly merge and preserve all sections
            library_update = {'libraries': libraries}
            if not save_config(library_update):
                logger.error("Failed to save auto-detected libraries")
            else:
                logger.info(f"Auto-detected {len(libraries)} libraries")
    except Exception as e:
        logger.error(f"Library auto-detection failed: {e}")
        raise


@app.route('/api/analysis/start', methods=['POST'])
def start_analysis():
    """Start analysis"""
    global current_analysis
    
    if current_analysis['running']:
        return jsonify({'success': False, 'message': 'Analysis already running'}), 400
    
    # Start analysis in background thread
    thread = Thread(target=run_analysis_thread)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True, 'message': 'Analysis started'})


@app.route('/api/analysis/status', methods=['GET'])
def analysis_status():
    """Get analysis status"""
    return jsonify(current_analysis)


@app.route('/api/reports', methods=['GET'])
def list_reports():
    """List available reports"""
    reports = []
    
    if REPORTS_DIR.exists():
        for file in sorted(REPORTS_DIR.glob('deletion_plan_*.json'), reverse=True):
            try:
                stat = file.stat()
                reports.append({
                    'filename': file.name,
                    'timestamp': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'size': stat.st_size
                })
            except Exception as e:
                logger.error(f"Error reading report {file}: {e}")
    
    return jsonify(reports)


@app.route('/api/reports/<filename>', methods=['GET'])
def get_report(filename):
    """Get specific report"""
    report_path = REPORTS_DIR / filename
    
    if not report_path.exists():
        return jsonify({'error': 'Report not found'}), 404
    
    try:
        with open(report_path, 'r') as f:
            report_data = json.load(f)
        return jsonify(report_data)
    except Exception as e:
        logger.error(f"Error reading report: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/reports/<filename>/download', methods=['GET'])
def download_report(filename):
    """Download report file"""
    report_path = REPORTS_DIR / filename
    
    if not report_path.exists():
        return jsonify({'error': 'Report not found'}), 404
    
    return send_file(report_path, as_attachment=True)


@app.route('/api/execute/delete', methods=['POST'])
def execute_delete():
    """Execute deletion for selected items"""
    try:
        data = request.json
        selected_ids = data.get('selected_ids', [])
        
        if not selected_ids:
            return jsonify({'success': False, 'message': 'No items selected'}), 400
        
        # Convert all IDs to strings for consistent comparison
        selected_ids = [str(id) for id in selected_ids]
        
        logger.info(f"Execute delete request for {len(selected_ids)} items")
        
        # Load latest report to get full item data
        reports = list(REPORTS_DIR.glob('deletion_plan_*.json'))
        if not reports:
            return jsonify({'success': False, 'message': 'No deletion plan found'}), 404
        
        latest_report = max(reports, key=lambda p: p.stat().st_mtime)
        
        with open(latest_report, 'r') as f:
            report_data = json.load(f)
        
        # Filter selected items - convert plex_id to string for comparison
        all_items = report_data.get('items', [])
        items_to_delete = [item for item in all_items if str(item['plex_id']) in selected_ids]
        
        if not items_to_delete:
            logger.error(f"No items found matching selected IDs: {selected_ids}")
            logger.error(f"Available IDs in report: {[str(item['plex_id']) for item in all_items[:5]]}")
            return jsonify({'success': False, 'message': 'Selected items not found in report'}), 404
        
        logger.info(f"Found {len(items_to_delete)} items to delete")
        
        # Create backup list
        backup_file = REPORTS_DIR / f"backup_before_delete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(backup_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'items_to_delete': items_to_delete
            }, f, indent=2, default=str)
        
        logger.info(f"Backup created: {backup_file}")
        
        # Execute deletion
        deleted_count = 0
        failed_count = 0
        errors = []
        
        for item in items_to_delete:
            try:
                success = _delete_item(item)
                if success:
                    deleted_count += 1
                else:
                    failed_count += 1
                    errors.append(f"{item['title']}: Deletion failed")
            except Exception as e:
                failed_count += 1
                errors.append(f"{item['title']}: {str(e)}")
                logger.error(f"Error deleting {item['title']}: {e}")
        
        result = {
            'success': True,
            'deleted': deleted_count,
            'failed': failed_count,
            'errors': errors[:10],  # Max 10 errors
            'backup_file': str(backup_file.name)
        }
        
        logger.info(f"Deletion complete: {deleted_count} deleted, {failed_count} failed")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Execute delete failed: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


def _delete_item(item: dict) -> bool:
    """
    Delete a single item from Plex and filesystem
    Returns True if successful
    """
    try:
        # Load config
        config_path = CONFIG_DIR / 'config.yaml'
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Connect to Plex with extended timeout for large series
        from plexapi.server import PlexServer
        plex_url = config['plex']['url']
        plex_token = config['plex']['token']
        
        # INCREASED TIMEOUT: 120 seconds for large TV series deletions
        plex = PlexServer(plex_url, plex_token, timeout=120)
        
        # Get item from Plex
        plex_item = plex.fetchItem(int(item['plex_id']))
        
        # Unmonitor in Sonarr/Radarr if enabled
        if item['media_type'] == 'show' and config.get('sonarr', {}).get('enabled'):
            if config.get('execution', {}).get('unmonitor_in_sonarr', True):
                _unmonitor_sonarr(item['title'], config)
        
        if item['media_type'] == 'movie' and config.get('radarr', {}).get('enabled'):
            if config.get('execution', {}).get('unmonitor_in_radarr', True):
                _unmonitor_radarr(item['title'], config)
        
        # Get file paths before deleting from Plex
        file_paths = []
        try:
            # For movies: single file or folder
            if item['media_type'] == 'movie':
                for media in plex_item.media:
                    for part in media.parts:
                        file_paths.append(part.file)
            # For TV shows: get all episode files
            elif item['media_type'] == 'show':
                for episode in plex_item.episodes():
                    for media in episode.media:
                        for part in media.parts:
                            file_paths.append(part.file)
        except Exception as e:
            logger.warning(f"Could not get file paths for {item['title']}: {e}")
            # Use file_path from report as fallback
            if item.get('file_path'):
                file_paths.append(item['file_path'])
        
        logger.info(f"Found {len(file_paths)} files to delete for {item['title']}")
        
        # Delete from Plex database first
        plex_item.delete()
        logger.info(f"Deleted from Plex database: {item['title']}")
        
        # Now delete actual files from disk
        import os
        import shutil
        from pathlib import Path
        
        deleted_files = 0
        deleted_folders = set()
        
        for file_path in file_paths:
            try:
                file_path_obj = Path(file_path)
                
                # Delete the file
                if file_path_obj.exists():
                    os.remove(file_path)
                    deleted_files += 1
                    logger.info(f"Deleted file: {file_path}")
                    
                    # Track parent folder for cleanup
                    parent_folder = file_path_obj.parent
                    deleted_folders.add(parent_folder)
                    
                    # For TV shows: also add the show root folder (one level up from season)
                    # Structure: /Series/Show Name/Season 01/episode.mkv
                    if item['media_type'] == 'show':
                        show_root_folder = parent_folder.parent
                        deleted_folders.add(show_root_folder)
                    
                else:
                    logger.warning(f"File not found: {file_path}")
                    
            except Exception as e:
                logger.error(f"Failed to delete file {file_path}: {e}")
        
        # Clean up parent folders (movie/show folders)
        # Sort by depth (deepest first) to delete season folders before show folder
        sorted_folders = sorted(deleted_folders, key=lambda f: len(f.parts), reverse=True)
        
        for folder in sorted_folders:
            try:
                if folder.exists():
                    # For TV shows: be more aggressive - delete entire folder with all content
                    # For Movies: also delete entire folder with all content (posters, subtitles, etc)
                    try:
                        shutil.rmtree(folder)
                        logger.info(f"Deleted folder and all contents: {folder}")
                    except Exception as e:
                        # Fallback: try to delete if empty
                        remaining_files = list(folder.iterdir())
                        if not remaining_files:
                            folder.rmdir()
                            logger.info(f"Deleted empty folder: {folder}")
                        else:
                            logger.warning(f"Could not delete folder {folder}: {e}")
                            logger.info(f"Remaining files: {[f.name for f in remaining_files[:5]]}")
            except Exception as e:
                logger.warning(f"Could not process folder {folder}: {e}")
        
        logger.info(f"Deletion complete: {item['title']} - {deleted_files} files deleted")
        return True
        
    except Exception as e:
        logger.error(f"Failed to delete {item.get('title', 'unknown')}: {e}")
        return False


def _unmonitor_sonarr(title: str, config: dict):
    """Unmonitor series in Sonarr"""
    try:
        from pyarr import SonarrAPI
        sonarr_cfg = config['sonarr']
        sonarr = SonarrAPI(sonarr_cfg['url'], sonarr_cfg['api_key'])
        
        # Find series
        all_series = sonarr.get_series()
        for series in all_series:
            if series.get('title', '').lower() == title.lower():
                series_id = series['id']
                # Update to unmonitored
                sonarr.upd_series({**series, 'monitored': False})
                logger.info(f"Unmonitored in Sonarr: {title}")
                break
    except Exception as e:
        logger.warning(f"Failed to unmonitor in Sonarr: {e}")


def _unmonitor_radarr(title: str, config: dict):
    """Unmonitor movie in Radarr"""
    try:
        from pyarr import RadarrAPI
        radarr_cfg = config['radarr']
        radarr = RadarrAPI(radarr_cfg['url'], radarr_cfg['api_key'])
        
        # Find movie
        all_movies = radarr.get_movie()
        for movie in all_movies:
            if movie.get('title', '').lower() == title.lower():
                movie_id = movie['id']
                # Update to unmonitored
                radarr.upd_movie({**movie, 'monitored': False})
                logger.info(f"Unmonitored in Radarr: {title}")
                break
    except Exception as e:
        logger.warning(f"Failed to unmonitor in Radarr: {e}")


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    stats = {
        'total_reports': 0,
        'last_run': None,
        'total_items_flagged': 0,
        'total_space_flagged_gb': 0
    }
    
    if REPORTS_DIR.exists():
        reports = list(REPORTS_DIR.glob('deletion_plan_*.json'))
        stats['total_reports'] = len(reports)
        
        if reports:
            # Get latest report
            latest = max(reports, key=lambda p: p.stat().st_mtime)
            
            try:
                with open(latest, 'r') as f:
                    data = json.load(f)
                    stats['last_run'] = data.get('timestamp')
                    stats['total_items_flagged'] = data.get('total_items', 0)
                    stats['total_space_flagged_gb'] = data.get('total_size_gb', 0)
            except Exception as e:
                logger.error(f"Error reading latest report: {e}")
    
    return jsonify(stats)


@app.route('/api/cleanup/reports', methods=['POST'])
def cleanup_old_reports():
    """Clean up old reports and backups"""
    try:
        data = request.json
        keep_count = data.get('keep_count', 5)  # Keep last 5 by default
        
        deleted = {
            'reports': 0,
            'backups': 0,
            'html': 0,
            'csv': 0
        }
        
        # Clean reports
        reports = sorted(REPORTS_DIR.glob('deletion_plan_*.json'), 
                        key=lambda p: p.stat().st_mtime, reverse=True)
        for old_report in reports[keep_count:]:
            old_report.unlink()
            deleted['reports'] += 1
            logger.info(f"Deleted old report: {old_report.name}")
        
        # Clean HTML reports
        html_reports = sorted(REPORTS_DIR.glob('deletion_plan_*.html'),
                             key=lambda p: p.stat().st_mtime, reverse=True)
        for old_html in html_reports[keep_count:]:
            old_html.unlink()
            deleted['html'] += 1
        
        # Clean CSV reports
        csv_reports = sorted(REPORTS_DIR.glob('deletion_plan_*.csv'),
                            key=lambda p: p.stat().st_mtime, reverse=True)
        for old_csv in csv_reports[keep_count:]:
            old_csv.unlink()
            deleted['csv'] += 1
        
        # Clean old backups (keep last 10 backups)
        backups = sorted(REPORTS_DIR.glob('backup_before_delete_*.json'),
                        key=lambda p: p.stat().st_mtime, reverse=True)
        for old_backup in backups[10:]:
            old_backup.unlink()
            deleted['backups'] += 1
            logger.info(f"Deleted old backup: {old_backup.name}")
        
        return jsonify({
            'success': True,
            'message': f"Cleaned up {sum(deleted.values())} old files",
            'deleted': deleted
        })
        
    except Exception as e:
        logger.error(f"Failed to cleanup reports: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/schedule/status', methods=['GET'])
def get_schedule_status():
    """Get scheduler status and configuration - reads from separate schedule.yaml"""
    try:
        if not scheduler_enabled:
            return jsonify({
                'enabled': False,
                'available': False,
                'message': 'Scheduler module not available'
            })
        
        # Load schedule config from SEPARATE file
        schedule_config = load_schedule_config()
        is_enabled = schedule_config.get('enabled', False)
        
        # Get next run time if scheduler is running
        next_run = None
        if scheduler and scheduler.running and is_enabled:
            jobs = scheduler.get_jobs()
            if jobs:
                next_run_dt = jobs[0].next_run_time
                if next_run_dt:
                    next_run = next_run_dt.isoformat()
        
        return jsonify({
            'enabled': is_enabled,
            'available': True,
            'running': scheduler.running if scheduler else False,
            'config': schedule_config,
            'next_run': next_run
        })
        
    except Exception as e:
        logger.error(f"Failed to get schedule status: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/schedule/update', methods=['POST'])
def update_schedule():
    """Update scheduler configuration - ONLY touches schedule.yaml, NEVER main config!"""
    try:
        if not scheduler_enabled:
            return jsonify({
                'success': False,
                'message': 'Scheduler module not available'
            }), 400
        
        data = request.json
        
        # Save to SEPARATE schedule.yaml file - main config is NEVER touched!
        if not save_schedule_config(data):
            return jsonify({
                'success': False,
                'message': 'Failed to save schedule configuration'
            }), 500
        
        # Re-initialize scheduler
        success = init_scheduler()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Schedule updated successfully (separate file)'
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Schedule saved but not activated (check logs)'
            })
        
    except Exception as e:
        logger.error(f"Failed to update schedule: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get recent logs"""
    log_file = LOGS_DIR / 'cleanup.log'
    
    if not log_file.exists():
        return jsonify({'logs': []})
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            # Return last 100 lines
            recent_lines = lines[-100:]
            return jsonify({'logs': recent_lines})
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Ensure directories exist
    CONFIG_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Create default config if not exists
    if not get_config_path().exists():
        save_config(get_default_config())
        logger.info("Created default configuration")
    
    # Initialize scheduler (safe - won't crash if it fails)
    try:
        init_scheduler()
    except Exception as e:
        logger.error(f"Scheduler initialization failed: {e}")
        logger.info("Application will continue with manual analysis only")
    
    # Run Flask app
    logger.info("Starting Plex Lifecycle Manager Web UI on port 8765")
    app.run(host='0.0.0.0', port=8765, debug=False)
