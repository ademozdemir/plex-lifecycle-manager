# 🎬 Plex Lifecycle Manager

**Smart media cleanup for Plex with Dutch audio priority**

Version 2.0.0 | January 2026

---

## 👋 Welcome!

Thank you for downloading Plex Lifecycle Manager!

This tool helps you automatically identify and clean up:
- ✅ Unwatched movies and TV shows
- ✅ Watched-too-long-ago content
- ✅ Duplicate media files
- ✅ Large unwatched files

With intelligent protection for:
- 🔒 Continuing TV series (via Sonarr)
- 🇳🇱 Dutch audio tracks (optional)
- 📋 Manual TV show review

---

## 🚀 Quick Start (Choose Your Path)

### **New Users** → Start Here! 📖
**Read:** [INDEX.md](INDEX.md) → [QUICKSTART.md](QUICKSTART.md)

Get running in 10 minutes with step-by-step instructions.

### **Experienced Users** → Skip to Installation 🏃
**Read:** [README.md](README.md)

Complete documentation with all features explained.

### **Just Want to See What's Inside?** 📦
**Read:** [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md)

Detailed overview of all files and their purpose.

---

## ⚡ Super Quick Start (3 Steps)

```bash
# 1. Extract package and navigate
cd /path/to/plex-lifecycle-manager

# 2. Start container
docker-compose up -d

# 3. Open Web UI
http://YOUR-SERVER-IP:8765
```

Then configure via Web UI and run your first analysis!

---

## 📚 Documentation Overview

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **[INDEX.md](INDEX.md)** | Navigation guide | 2 min |
| **[QUICKSTART.md](QUICKSTART.md)** | Get started fast | 5 min |
| **[README.md](README.md)** | Complete docs | 15 min |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Deploy checklist | 10 min |
| **[PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md)** | File overview | 5 min |
| **[CHANGELOG.md](CHANGELOG.md)** | Version history | 5 min |
| **[config.example.yaml](config.example.yaml)** | Config reference | 10 min |

---

## ⚠️ Important: Read This First!

### This Tool Permanently Deletes Files

- ❌ **No undo** - Deleted files are gone forever
- ✅ **Test first** - Start with 1-2 unimportant items
- 💾 **Backup important media** - Keep copies of irreplaceable content
- 📋 **Manual TV review** - TV shows require explicit selection

**Please read the [LICENSE](LICENSE) file for full disclaimer.**

---

## 🇳🇱 About Dutch Audio Priority

This tool was originally developed for a Dutch user, hence the "NL Audio Priority" feature.

**If you DON'T use Dutch audio:**
- ⚠️ **Disable "NL Audio Priority"** in Configuration tab
- This prevents keeping lower-quality versions just for Dutch audio

**If you DO use Dutch audio:**
- ✅ **Enable "NL Audio Priority"** in Configuration tab
- Tool will prefer versions with Dutch audio, even if lower quality

---

## 🎯 What's Included

✅ Complete Docker deployment (ready to run)  
✅ Modern Web UI (port 8765)  
✅ Analysis engine with smart rules  
✅ Duplicate detection  
✅ Sonarr/Radarr integration  
✅ Comprehensive reports (JSON, HTML, CSV)  
✅ Safety features (confirmations, backups)  
✅ Complete documentation  

---

## 🔧 Requirements

- Docker & Docker Compose
- Plex Media Server
- (Optional) Sonarr - for TV show protection
- (Optional) Radarr - for movie management

---

## 📖 Documentation Structure

```
📁 plex-lifecycle-manager/
│
├── 🚀 START HERE.md              ← You are here!
├── 📍 INDEX.md                    ← Navigation guide
├── ⚡ QUICKSTART.md               ← 10-minute setup
├── 📖 README.md                   ← Complete docs
│
├── 📋 DEPLOYMENT.md               ← Deploy checklist
├── 📦 PACKAGE_CONTENTS.md         ← File overview
├── 📝 CHANGELOG.md                ← Version history
├── ⚖️  LICENSE                    ← MIT License
│
├── 🐳 docker-compose.yml          ← Docker config
├── 📄 config.example.yaml         ← Config example
│
└── 🔧 app/                        ← Application code
    ├── smart_cleanup.py
    ├── web_ui.py
    └── templates/index.html
```

---

## 🆘 Need Help?

1. **Check:** [INDEX.md](INDEX.md) → Find documentation by topic
2. **Read:** [QUICKSTART.md](QUICKSTART.md) → Common issues section
3. **Review:** [README.md](README.md) → Troubleshooting section
4. **Verify:** [DEPLOYMENT.md](DEPLOYMENT.md) → Verification steps
5. **Check logs:** `docker logs plex-lifecycle`

---

## 🎉 Ready to Start?

### Recommended Path:
1. ✅ Read [INDEX.md](INDEX.md) (2 minutes)
2. ✅ Read [QUICKSTART.md](QUICKSTART.md) (5 minutes)
3. ✅ Follow installation steps (10 minutes)
4. ✅ Configure via Web UI (5 minutes)
5. ✅ Run first analysis (15-30 minutes)
6. ✅ Review results carefully
7. ✅ Test with 1-2 items
8. ✅ Enjoy your cleaned-up library! 🎬

---

## 💡 Pro Tips

- Start with conservative settings (high age thresholds)
- Always review reports before deletion
- Test with unimportant items first
- Run analysis monthly for best results
- Keep backups of irreplaceable media

---

## 📊 Features at a Glance

| Feature | Description |
|---------|-------------|
| 🎯 Smart Rules | Age-based cleanup for movies & TV |
| 🔍 Duplicates | Find and remove duplicate files |
| 🇳🇱 NL Audio | Preserve Dutch audio (optional) |
| 🔒 TV Protection | Manual review + continuing series |
| 📊 Reports | JSON, HTML, CSV formats |
| 🌐 Web UI | Modern responsive interface |
| 🔄 Integration | Sonarr & Radarr support |
| 💾 Backups | Automatic pre-deletion backups |
| 🧹 Complete Cleanup | Removes files AND folders |
| 🔐 Safety | Confirmations, protections |

---

**Thank you for using Plex Lifecycle Manager!**

Questions? Start with [INDEX.md](INDEX.md) to find the right documentation.

---

**Version:** 2.0.0  
**Release Date:** 2026-01-06  
**License:** MIT  
**Author:** Originally developed for personal use with Dutch audio priority

**⚠️ Disclaimer:** This software permanently deletes files. Use at your own risk. See [LICENSE](LICENSE) for details.
