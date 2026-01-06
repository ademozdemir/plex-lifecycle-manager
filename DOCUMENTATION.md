# Plex Lifecycle Manager 🎬

**Smart media cleanup for Plex with Dutch audio priority and intelligent rules**

Automatically identify and clean up unwatched, watched-too-long-ago, and duplicate media from your Plex library with intelligent rules, Dutch audio preservation, and Sonarr/Radarr integration.

---

## ✨ Features

### Core Features
- 🎯 **Smart Cleanup Rules** - Age-based cleanup for unwatched/watched content
- 🔍 **Duplicate Detection** - Find and remove duplicate movies/shows
- 🇳🇱 **Dutch Audio Priority** - Preserve Dutch audio tracks over higher quality (configurable!)
- 📊 **TV Show Manual Review** - TV shows require explicit user approval before deletion
- 🔒 **Continuing Series Protection** - Automatically protects ongoing TV shows from deletion
- 📈 **Beautiful Web UI** - Modern, responsive interface for analysis and execution
- 🔄 **Sonarr/Radarr Integration** - Automatic unmonitoring before deletion
- 💾 **Automatic Backups** - JSON backups created before any deletion
- 📄 **Comprehensive Reports** - JSON, HTML, and CSV output formats

### Execution Features
- ✅ **Pre-selection** - Movies auto-selected, TV shows manual review
- 🎛️ **Flexible Filtering** - Filter by Movies/TV Shows/All
- 📑 **Pagination** - Handle large libraries (20/50/100/All items per page)
- 🗑️ **Batch Deletion** - Delete multiple items at once
- 🔐 **Safety Confirmation** - Type "DELETE" to confirm destructive actions
- 🧹 **Complete Cleanup** - Removes files AND folders from disk
- 📋 **Report Management** - Cleanup old reports to save disk space

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Plex Media Server
- (Optional) Sonarr
- (Optional) Radarr

### Installation

1. **Clone or download this repository**
```bash
mkdir -p /path/to/plex-lifecycle
cd /path/to/plex-lifecycle
```

2. **Create directory structure**
```bash
mkdir -p app/templates config reports logs
```

3. **Copy files to directories:**
```
/path/to/plex-lifecycle/
├── docker-compose.yml
├── Dockerfile
├── requirements_docker.txt
├── app/
│   ├── smart_cleanup.py
│   ├── web_ui.py
│   └── templates/
│       └── index.html
├── config/           # Created automatically
├── reports/          # Created automatically
└── logs/            # Created automatically
```

4. **Build and start the container**
```bash
docker-compose up -d
```

5. **Access the Web UI**
```
http://YOUR-SERVER-IP:8765
```

6. **Configure your settings** (see Configuration section below)

---

## ⚙️ Configuration

### First Time Setup

1. **Navigate to Configuration tab** in the Web UI

2. **Plex Server Settings** (Required)
   - **Plex URL**: `http://YOUR-SERVER-IP:32400`
   - **Plex Token**: See [Finding Your Plex Token](#finding-your-plex-token)

3. **Sonarr Integration** (Optional but recommended for TV shows)
   - Enable Sonarr Integration checkbox
   - **Sonarr URL**: `http://YOUR-SERVER-IP:8989`
   - **Sonarr API Key**: See [Finding Sonarr API Key](#finding-sonarr-api-key)

4. **Radarr Integration** (Optional but recommended for movies)
   - Enable Radarr Integration checkbox
   - **Radarr URL**: `http://YOUR-SERVER-IP:7878`
   - **Radarr API Key**: See [Finding Radarr API Key](#finding-radarr-api-key)

5. **Cleanup Rules**
   - **Unwatched Age Threshold**: Delete if unwatched for X years (default: 5)
   - **Watched Age Threshold**: Delete if last viewed X years ago (default: 2)
   - **Low Rating Threshold**: Consider low-rated if < X stars (default: 3)
   - **Large File Threshold**: Consider large if > X GB (default: 50)
   - **NL Audio Priority**: ⚠️ **Enable if you want to keep Dutch audio** (disable if you don't care about Dutch audio!)

6. **Duplicate Detection**
   - Enable Duplicate Detection checkbox
   - Uses title + year matching
   - Prefers higher quality, but respects NL audio priority if enabled

7. **Click "Save Configuration"**

---

## 🔑 Finding API Keys and Tokens

### Finding Your Plex Token

**Method 1: Via Plex Web App**
1. Open Plex Web App
2. Play any media item
3. Click the **ⓘ** (info) button
4. Click **"View XML"**
5. Look in the URL bar: `...&X-Plex-Token=XXXXX`
6. Copy the token after `X-Plex-Token=`

**Method 2: Via Plex Settings**
1. Go to Plex Settings
2. Click your username → Account
3. Scroll to "Authorized Devices"
4. The token is visible in network requests (use browser dev tools)

**Official Plex Documentation:**
https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

### Finding Sonarr API Key

1. Open Sonarr web interface
2. Go to **Settings** → **General**
3. Scroll to **Security** section
4. Copy the **API Key**

### Finding Radarr API Key

1. Open Radarr web interface
2. Go to **Settings** → **General**
3. Scroll to **Security** section
4. Copy the **API Key**

---

## 📖 Usage Guide

### Workflow

#### 1. **Run Analysis**
```
Analysis Tab → Start Analysis
Wait ~15-30 minutes (depends on library size)
```

The analysis will:
- Scan all configured Plex libraries
- Apply cleanup rules based on your settings
- Check Sonarr for continuing TV series
- Detect duplicates
- Generate comprehensive reports

#### 2. **Review Report**
```
Reports Tab → View latest report
```

**What you'll see:**
- **Movies**: Pre-selected with ✓ checkboxes (auto-recommended for deletion)
- **TV Shows**: NOT pre-selected, require manual review
- **Continuing Series**: Disabled checkbox, protected from deletion

**Badges:**
- 🟢 **Continuing Series** - Active TV shows (Sonarr)
- 🟠 **Manual Review** - TV shows requiring user decision
- 🇳🇱 **NL** - Has Dutch audio track

#### 3. **Adjust Selection**
```
Use filters: [All] [Movies Only] [TV Shows Only]
Pagination: 20/50/100/All items per page

Buttons:
- "Select All Movies" - Select only movies
- "Select All Visible" - Select everything visible
- "Deselect All" - Clear all selections
```

**Selection Strategy:**
- ✅ **Movies**: Pre-selected based on rules - uncheck what you want to keep
- ✅ **TV Shows**: NOT pre-selected - check what you want to delete
- ❌ **Continuing Series**: Cannot be selected (protected)

#### 4. **Delete Selected Items**
```
Click "Delete Selected" button
Review summary popup
Type "DELETE" to confirm
Wait for completion
```

**What happens during deletion:**
1. Backup created: `backup_before_delete_TIMESTAMP.json`
2. Items unmonitored in Sonarr/Radarr (prevents re-download)
3. Items deleted from Plex database
4. Files deleted from disk
5. Folders deleted from disk
6. Summary report shown

#### 5. **Cleanup Old Reports** (Optional)
```
Reports Tab → Click "Cleanup Old Reports"
Enter number of reports to keep (default: 5)
Confirm
```

Deletes old:
- JSON reports
- HTML reports
- CSV reports
- Old backups (keeps last 10)

---

## 📁 File Structure & Explanation

### Project Structure
```
/path/to/plex-lifecycle/
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Docker image definition
├── requirements_docker.txt     # Python dependencies
│
├── app/
│   ├── smart_cleanup.py       # Main analysis engine
│   ├── web_ui.py              # Web server & API
│   └── templates/
│       └── index.html         # Web interface
│
├── config/
│   └── config.yaml            # Your configuration (auto-generated)
│
├── reports/                    # Analysis reports
│   ├── deletion_plan_*.json   # JSON reports
│   ├── deletion_plan_*.html   # HTML reports
│   ├── deletion_plan_*.csv    # CSV reports
│   └── backup_before_delete_*.json  # Pre-deletion backups
│
└── logs/
    ├── cleanup.log            # Analysis logs
    └── web_ui.log            # Web server logs
```

### File Descriptions

#### **smart_cleanup.py** - Analysis Engine
**What it does:**
- Connects to Plex, Sonarr, Radarr
- Scans all configured libraries
- Applies cleanup rules to identify candidates
- Detects duplicates with NL audio priority
- Checks Sonarr for continuing series
- Generates reports (JSON, HTML, CSV)

**What you can customize:**
- Cleanup rules (via Web UI Configuration)
- Library mappings (automatically detected from Plex)
- Audio priority logic (NL audio checkbox)
- Duplicate detection rules (enabled/disabled)

**Key functions:**
- `scan_plex()` - Scans Plex libraries
- `apply_rules()` - Applies cleanup rules
- `detect_duplicates()` - Finds duplicates
- `generate_report()` - Creates reports

#### **web_ui.py** - Web Server & API
**What it does:**
- Runs Flask web server on port 8765
- Provides REST API for frontend
- Handles configuration management
- Executes analysis in background
- Performs actual file deletions
- Manages reports and backups

**What you can customize:**
- Port number (in docker-compose.yml)
- Timeout values (for large TV show deletions)
- Report retention (via cleanup endpoint)

**Key endpoints:**
- `GET /api/config` - Load configuration
- `POST /api/config` - Save configuration
- `POST /api/analysis/start` - Start analysis
- `GET /api/analysis/status` - Check progress
- `GET /api/reports` - List reports
- `POST /api/execute/delete` - Execute deletion
- `POST /api/cleanup/reports` - Cleanup old reports

#### **index.html** - Web Interface
**What it does:**
- Modern, responsive web interface
- Configuration management
- Analysis progress tracking
- Report viewing with pagination
- Item selection and filtering
- Delete execution with safety checks

**What you can customize:**
- Styling (CSS at the top)
- Default pagination size (JavaScript variables)
- Button labels and text
- Color scheme

---

## 🔧 Advanced Configuration

### Docker Compose Customization

**Change port:**
```yaml
ports:
  - "8080:8765"  # Change left side (host port)
```

**Change paths:**
```yaml
volumes:
  - ./config:/config
  - ./reports:/reports
  - ./logs:/logs
  - /your/media/path:/media/movies:ro  # Read-only mount
```

### Manual Configuration (config.yaml)

**Location:** `/path/to/plex-lifecycle/config/config.yaml`

**Example configuration:**
```yaml
plex:
  url: "http://192.168.1.100:32400"
  token: "YOUR_PLEX_TOKEN"

sonarr:
  enabled: true
  url: "http://192.168.1.100:8989"
  api_key: "YOUR_SONARR_API_KEY"

radarr:
  enabled: true
  url: "http://192.168.1.100:7878"
  api_key: "YOUR_RADARR_API_KEY"

rules:
  movies:
    unwatched_age_years: 5.0
    watched_age_years: 2.0
    low_rating_threshold: 3.0
    large_file_gb: 50
  
  tv_shows:
    unwatched_age_years: 5.0
    fully_watched_age_years: 0.5
    partially_watched_age_years: 2.0

duplicates:
  enabled: true
  nl_audio_priority: false  # Set to false if you don't care about Dutch audio
```

---

## 🛡️ Safety Features

### Built-in Protections

1. **Dry Run Mode** - Analysis never deletes files
2. **Manual TV Show Review** - TV shows require explicit user selection
3. **Continuing Series Protection** - Active shows protected via Sonarr
4. **Confirmation Required** - Must type "DELETE" to confirm
5. **Pre-deletion Backup** - JSON backup of all metadata created
6. **Sonarr/Radarr Unmonitoring** - Prevents automatic re-download
7. **Per-item Error Handling** - One failure doesn't stop the process
8. **Comprehensive Logging** - All actions logged to files

### What Gets Deleted

When you execute a deletion:
- ✅ Item removed from Plex database
- ✅ Media files deleted from disk
- ✅ Folders deleted from disk (including metadata)
- ✅ Item unmonitored in Sonarr/Radarr

### What Does NOT Get Deleted

- ❌ Continuing series (protected by Sonarr status)
- ❌ Items not selected (obviously!)
- ❌ Backup metadata (kept in reports folder)

### Limitations

- **No undo** - Deleted files are permanently removed
- **Backup contains metadata only** - Not the actual media files
- **Title matching for Sonarr/Radarr** - May fail if titles differ
- **No multi-user support** - Designed for single-user personal use

---

## 🐛 Troubleshooting

### Container won't start
```bash
# Check logs
docker logs plex-lifecycle

# Common issues:
# - Port 8765 already in use (change in docker-compose.yml)
# - Missing files (verify all files are in correct locations)
# - Permission issues (ensure directories are writable)
```

### Can't connect to Plex/Sonarr/Radarr
```bash
# Check if services are accessible from container
docker exec plex-lifecycle curl -I http://YOUR-PLEX-IP:32400

# Common issues:
# - Firewall blocking access
# - Wrong IP address (use host IP, not localhost)
# - Services not running
# - Wrong port numbers
```

### Analysis takes too long
```bash
# Normal analysis time:
# - Small library (<500 items): 5-10 minutes
# - Medium library (500-1000 items): 10-20 minutes  
# - Large library (1000+ items): 20-40 minutes

# Check progress in logs:
docker logs -f plex-lifecycle
```

### Deletion timeout for large TV shows
```bash
# Already fixed in latest version (120s timeout)
# If still timing out, increase in web_ui.py:
# plex = PlexServer(plex_url, plex_token, timeout=300)
```

### No TV shows in report
```bash
# Possible causes:
# 1. No TV shows meet cleanup rules (normal!)
# 2. Check rules in config.yaml (tv_shows section)
# 3. Verify TV libraries are configured in Plex
# 4. Check logs for errors during analysis
```

---

## 📊 Understanding Reports

### Report Format (JSON)

```json
{
  "timestamp": "2026-01-06T08:47:28.426000",
  "total_items": 25,
  "total_size_gb": 234.56,
  "items": [
    {
      "title": "Movie Title",
      "year": 2020,
      "plex_id": "12345",
      "library_name": "Movies",
      "media_type": "movie",
      "file_size_gb": 15.5,
      "has_nl_audio": true,
      "resolution": "1080p",
      "delete_reason": "Unwatched for 5.7 years",
      "delete_priority": 5,
      "auto_recommended": true,
      "requires_manual_review": false,
      "is_continuing": false
    }
  ]
}
```

### Fields Explained

- **auto_recommended**: `true` for movies (pre-selected), `false` for TV shows
- **requires_manual_review**: `true` for TV shows (user must select)
- **is_continuing**: `true` for active TV shows (protected)
- **delete_priority**: Higher = more urgent to delete (1-10 scale)
- **has_nl_audio**: `true` if Dutch audio track detected

---

## 🎯 Best Practices

### Initial Setup

1. **Start conservative** - Set high age thresholds (5+ years)
2. **Run analysis first** - Review reports before deleting anything
3. **Test with a few items** - Delete 1-2 test items first
4. **Verify results** - Check Plex and filesystem after test deletion
5. **Adjust rules** - Lower thresholds if you want more aggressive cleanup

### Regular Maintenance

1. **Run analysis monthly** - Keep library clean
2. **Review TV shows carefully** - Manual review prevents mistakes
3. **Cleanup old reports** - Keep disk space available
4. **Check logs occasionally** - Catch any recurring errors
5. **Backup important media** - This tool permanently deletes files!

### NL Audio Priority

**If you DON'T use Dutch audio:**
- ⚠️ **Disable "NL Audio Priority" in Configuration**
- This prevents the tool from keeping lower-quality versions just for Dutch audio

**If you DO use Dutch audio:**
- ✅ **Enable "NL Audio Priority" in Configuration**
- Tool will prefer versions with Dutch audio, even if lower quality

---

## 📝 License

This project is provided as-is with no warranty. Use at your own risk!

---

## 🙏 Credits

Originally developed for personal use to manage a Plex library with Dutch audio priority.

---

## ⚠️ Important Disclaimer

**THIS TOOL PERMANENTLY DELETES FILES FROM YOUR DISK!**

- Always review reports before deletion
- Test with non-important items first
- Keep backups of important media
- The backup files contain metadata only, not the actual media files
- No undo feature - deleted files are gone forever

**Use at your own risk!**
