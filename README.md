# Plex Lifecycle Manager by Claude and me

<div align="center">

**Smart media cleanup for Plex with intelligent rules and Dutch audio priority**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)]()
[![Python](https://img.shields.io/badge/Python-3.12-green.svg)]()
[![Version](https://img.shields.io/badge/Version-2.1.1-orange.svg)]()

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Installation](#-installation) • [Screenshots](#-screenshots)

</div>

---

## 🎬 What is This?

Plex Lifecycle Manager is a **smart cleanup tool** for Plex Media Server that helps you automatically identify and clean up unwatched, watched-too-long-ago, and duplicate media files based on intelligent rules.

**Key Features:**
- 🎯 Smart age-based cleanup rules for movies and TV shows
- 🔍 Duplicate detection with configurable quality preferences
- 🇳🇱 Optional Dutch audio priority (can be disabled!)
- 📊 TV show manual review with continuing series protection
- 🌐 Modern web interface with batch operations
- 🔄 Optional scheduled analysis
- 💾 Automatic backups before deletion
- 🔒 Safety features: confirmations, protections, extensive logging

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/plex-lifecycle-manager.git
cd plex-lifecycle-manager

# 2. Start Docker container
docker-compose up -d

# 3. Open Web UI
http://YOUR-SERVER-IP:8765

# 4. Configure and run first analysis
# See QUICKSTART.md for detailed instructions
```

**First time user?** → Read **[QUICKSTART.md](QUICKSTART.md)** for a 10-minute setup guide!

---

## ✨ Features

### Core Functionality
- **Smart Cleanup Rules** - Age-based deletion for unwatched/watched content
- **Duplicate Detection** - Find and remove duplicate movies/shows
- **TV Show Protection** - Manual review required + automatic continuing series protection
- **Batch Operations** - Delete multiple items at once with filtering and pagination
- **Comprehensive Reports** - JSON, HTML, and CSV output formats

### Integrations
- **Plex Media Server** - Direct API integration
- **Sonarr** - Automatic continuing series detection and unmonitoring
- **Radarr** - Automatic unmonitoring before deletion

### Safety Features
- ✅ Manual TV show review (prevents accidental deletions)
- ✅ Continuing series protection (via Sonarr integration)
- ✅ Type "DELETE" confirmation (safety check)
- ✅ Automatic pre-deletion backups (metadata only)
- ✅ Comprehensive logging (all actions tracked)
- ✅ Per-item error handling (one failure doesn't stop process)

### Optional Features
- **Scheduled Analysis** - Run analysis automatically (daily/weekly/monthly)
- **Dutch Audio Priority** - Preserve Dutch audio tracks over quality (disable if not needed!)
- **Report Management** - Cleanup old reports automatically

---

## 📖 Documentation

**Start here:**
- **[START_HERE.md](START_HERE.md)** - Welcome guide and navigation
- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 10 minutes
- **[README.md](README.md)** - Complete documentation

**Additional docs:**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment checklist and troubleshooting
- **[PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md)** - File overview and customization guide
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[INDEX.md](INDEX.md)** - Documentation index

---

## 🔧 Installation

### Prerequisites
- Docker & Docker Compose
- Plex Media Server
- (Optional) Sonarr - for TV show protection
- (Optional) Radarr - for movie management

### Docker Deployment (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/plex-lifecycle-manager.git
cd plex-lifecycle-manager

# 2. Configure (optional - can also configure via Web UI)
cp config.example.yaml config/config.yaml
# Edit config/config.yaml with your Plex/Sonarr/Radarr details

# 3. Start container
docker-compose up -d

# 4. Check logs
docker logs -f plex-lifecycle

# 5. Access Web UI
http://YOUR-SERVER-IP:8765
```

### Configuration

See **[QUICKSTART.md](QUICKSTART.md#configuration)** for detailed configuration guide.

**Minimum required:**
- Plex URL: `http://YOUR-PLEX-IP:32400`
- Plex Token: [How to find](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

**Recommended:**
- Sonarr integration (for TV show protection)
- Radarr integration (for movie management)

**Important:**
- ⚠️ **Disable "NL Audio Priority"** if you don't use Dutch audio!

---

## 📊 Screenshots

### Web Interface
- Modern, responsive design
- Tab-based navigation
- Configuration management
- Analysis progress tracking
- Report viewing with pagination
- Batch deletion with safety checks

*(Add screenshots here if desired)*

---

## 🎯 Usage

### Basic Workflow

1. **Configure** - Set up Plex, Sonarr, Radarr credentials
2. **Run Analysis** - Scan libraries and apply cleanup rules
3. **Review Report** - Check flagged items (movies pre-selected, TV shows manual)
4. **Delete Items** - Execute deletion with confirmation
5. **Verify** - Check Plex and filesystem

### Scheduled Analysis (Optional)

Enable scheduled analysis in Configuration tab:
- **Frequency:** Daily, Weekly, or Monthly
- **Time:** Any time in 24-hour format (e.g., 03:00)
- **Day:** For weekly/monthly schedules

The scheduler runs in the background and logs all activity.

**Note:** Scheduled analysis is **optional** and **safe** - if it fails, manual analysis still works!

---

## ⚠️ Important Warnings

**THIS TOOL PERMANENTLY DELETES FILES FROM YOUR DISK!**

- ❌ **No undo** - Deleted files are gone forever
- ✅ **Test first** - Start with 1-2 unimportant items
- 💾 **Backup important media** - Keep copies of irreplaceable content
- 📋 **Read documentation** - Especially safety features and best practices

**The backup files contain metadata only, not the actual media files!**

---

## 🛠️ Customization

### Cleanup Rules
Adjust via Web UI Configuration tab or edit `config/config.yaml`:
- Unwatched age thresholds
- Watched age thresholds
- Low rating thresholds
- Large file thresholds

### File Structure
See **[PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md)** for detailed file descriptions and customization points.

---

## 🐛 Troubleshooting

### Common Issues

**Container won't start:**
```bash
docker logs plex-lifecycle
# Check for error messages
```

**Can't connect to Plex:**
- Use server IP, not localhost
- Verify Plex is running
- Check firewall settings

**No TV shows in report:**
- This is normal if no TV shows meet cleanup rules!
- Check rules in config.yaml (tv_shows section)

**Deletion timeout:**
- Already fixed in v2.0.0 (120s timeout)
- For very large TV shows (200+ episodes), increase in web_ui.py

See **[README.md#troubleshooting](README.md#-troubleshooting)** for complete troubleshooting guide.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Important Disclaimer:**
This software permanently deletes files from your storage. The authors are not responsible for lost data or accidental deletions. Use at your own risk!

---

## 🙏 Credits

Originally developed for personal use to manage a Plex library with Dutch audio priority.

Special thanks to:
- PlexAPI developers
- Sonarr and Radarr projects
- Flask and APScheduler communities

---

## 📞 Support

- **Documentation:** See [START_HERE.md](START_HERE.md) for navigation
- **Issues:** Use GitHub Issues for bugs and feature requests
- **Discussions:** Use GitHub Discussions for questions

---

## 🔄 Version History

See **[CHANGELOG.md](CHANGELOG.md)** for detailed version history.

**Current Version:** 2.0.0
- Complete Execute Mode V2 with batch operations
- TV show manual review and continuing series protection
- Optional scheduled analysis
- Enhanced safety features
- Modern web interface

---

## 🚧 Roadmap

Future considerations (not guaranteed):
- Multi-user authentication
- More granular TV show rules
- Custom rule sets per library
- Email notifications
- Statistics dashboard
- Search functionality in reports

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Development setup:**
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/plex-lifecycle-manager.git
cd plex-lifecycle-manager

# Build and run
docker-compose up -d

# View logs
docker logs -f plex-lifecycle

# Make changes to files in app/
# Restart to see changes
docker-compose restart
```

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ for Plex users who want a clean, organized library

</div>
