# Plex Lifecycle Manager - Documentation Index

**Smart media cleanup for Plex with Dutch audio priority and intelligent rules**

Version 2.0.0

---

## 📚 Documentation Structure

### 🚀 **Start Here**
1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 10 minutes
2. **[README.md](README.md)** - Complete documentation

### 📖 **Detailed Guides**
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment checklist and troubleshooting
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

### 📄 **Reference**
- **[config.example.yaml](config.example.yaml)** - Example configuration with comments
- **[LICENSE](LICENSE)** - MIT License and disclaimer

---

## 🎯 Choose Your Path

### I want to get started quickly
→ Read **QUICKSTART.md** (10 minutes)

### I want complete documentation
→ Read **README.md** (comprehensive guide)

### I need deployment help
→ Read **DEPLOYMENT.md** (checklist & troubleshooting)

### I want to know what changed
→ Read **CHANGELOG.md** (version history)

### I need configuration examples
→ Read **config.example.yaml** (commented example)

---

## 📁 Project Structure

```
plex-lifecycle-manager/
│
├── 📖 Documentation
│   ├── README.md              ← Main documentation
│   ├── QUICKSTART.md          ← Quick start guide
│   ├── DEPLOYMENT.md          ← Deployment checklist
│   ├── CHANGELOG.md           ← Version history
│   ├── INDEX.md               ← This file
│   └── LICENSE                ← MIT License
│
├── 🐳 Docker Files
│   ├── docker-compose.yml     ← Docker deployment
│   ├── Dockerfile             ← Container definition
│   └── requirements_docker.txt ← Python dependencies
│
├── 📝 Configuration
│   └── config.example.yaml    ← Example configuration
│
├── 🔧 Application
│   └── app/
│       ├── smart_cleanup.py   ← Analysis engine
│       ├── web_ui.py          ← Web server & API
│       └── templates/
│           └── index.html     ← Web interface
│
├── 📊 Runtime Directories (auto-created)
│   ├── config/                ← Your configuration
│   ├── reports/               ← Analysis reports
│   └── logs/                  ← Application logs
│
└── 🔒 Git
    └── .gitignore             ← Git ignore rules
```

---

## 🔍 Quick Reference by Topic

### Installation & Setup
- Getting started: **QUICKSTART.md** → Installation
- Detailed setup: **README.md** → Quick Start
- Configuration: **config.example.yaml**
- Deployment checklist: **DEPLOYMENT.md**

### Configuration
- Finding Plex token: **README.md** → Finding API Keys and Tokens
- Finding Sonarr/Radarr keys: **README.md** → Finding API Keys and Tokens
- Configuration options: **config.example.yaml**
- Advanced config: **README.md** → Advanced Configuration

### Usage
- First analysis: **QUICKSTART.md** → First Analysis
- Understanding reports: **README.md** → Understanding Reports
- Deleting items: **QUICKSTART.md** → First Deletion
- Best practices: **README.md** → Best Practices

### Troubleshooting
- Common issues: **QUICKSTART.md** → Common First-Time Issues
- Detailed troubleshooting: **README.md** → Troubleshooting
- Deployment issues: **DEPLOYMENT.md** → Quick Troubleshooting

### Customization
- File structure: **README.md** → File Structure & Explanation
- Changing rules: **config.example.yaml**
- Advanced customization: **README.md** → Advanced Configuration
- Understanding code: **README.md** → File Descriptions

---

## ⚠️ Important Notes

### Before You Start
1. **This tool permanently deletes files** - No undo!
2. **Test with unimportant items first**
3. **Keep backups of irreplaceable media**
4. **Read the safety features** in README.md

### NL Audio Priority
Originally developed for Dutch users:
- ✅ **Enable** if you use Dutch audio tracks
- ❌ **Disable** if you don't (prevents keeping low-quality versions)
- Configure in Web UI → Configuration tab

### TV Show Protection
- TV shows require **manual review** before deletion
- Continuing series are **automatically protected** via Sonarr
- Movies are **auto-selected** but can be unchecked

---

## 🆘 Getting Help

### Step-by-Step Troubleshooting
1. Check **QUICKSTART.md** → Common First-Time Issues
2. Check **README.md** → Troubleshooting section
3. Review **DEPLOYMENT.md** → Verification Steps
4. Check Docker logs: `docker logs plex-lifecycle`
5. Check application logs in `/logs` directory

### Before Asking for Help
- What are you trying to do?
- What error message did you see?
- What's in the logs? (`docker logs plex-lifecycle`)
- What's your configuration? (without sensitive data!)
- Did you follow the QUICKSTART guide?

---

## 🎯 Success Checklist

- [ ] Read QUICKSTART.md
- [ ] Installed and running (port 8765)
- [ ] Configuration saved (Plex, Sonarr, Radarr)
- [ ] First analysis completed
- [ ] Report reviewed
- [ ] Tested with 1-2 items
- [ ] Verified deletion works correctly
- [ ] Understood safety features
- [ ] Read best practices

---

## 📊 Feature Overview

| Feature | Description | Documentation |
|---------|-------------|---------------|
| Smart Cleanup | Age-based deletion rules | README.md → Features |
| Duplicate Detection | Find and remove duplicates | README.md → Features |
| NL Audio Priority | Preserve Dutch audio | README.md → NL Audio Priority |
| TV Manual Review | User approval required | README.md → Usage Guide |
| Continuing Series | Auto-protection via Sonarr | README.md → Features |
| Web UI | Modern interface | README.md → Usage Guide |
| Batch Deletion | Delete multiple items | QUICKSTART.md → First Deletion |
| Report Management | Cleanup old reports | README.md → Usage Guide |
| Safety Features | Confirmations, backups | README.md → Safety Features |

---

## 🔗 External Resources

- **Plex Token Guide**: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
- **Docker Documentation**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/

---

## 📝 Quick Commands

```bash
# Start container
docker-compose up -d

# View logs
docker logs -f plex-lifecycle

# Restart container
docker-compose restart

# Stop container
docker-compose down

# Rebuild after changes
docker-compose build && docker-compose up -d

# Access Web UI
http://YOUR-SERVER-IP:8765
```

---

## 🎉 Ready to Start?

**New users:** Start with **[QUICKSTART.md](QUICKSTART.md)**

**Experienced users:** Jump to **[README.md](README.md)** for full documentation

**Need help?** Check **[DEPLOYMENT.md](DEPLOYMENT.md)** for troubleshooting

---

**Version:** 2.0.0  
**Last Updated:** 2026-01-06  
**License:** MIT (see LICENSE file)
