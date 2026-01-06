# Project Structure

## 📁 Directory Layout

```
plex-lifecycle-manager/
│
├── 📖 Documentation
│   ├── README.md                  ← Start here! (GitHub landing page)
│   ├── START_HERE.md              ← Welcome guide
│   ├── QUICKSTART.md              ← 10-minute setup
│   ├── DOCUMENTATION.md           ← Complete documentation
│   ├── DEPLOYMENT.md              ← Deployment guide
│   ├── SCHEDULER.md               ← Scheduler guide
│   ├── SCHEDULER_GUI_UPDATE.md    ← GUI update notes
│   ├── INDEX.md                   ← Documentation index
│   ├── PACKAGE_CONTENTS.md        ← File descriptions
│   ├── CHANGELOG.md               ← Version history
│   ├── CONTRIBUTING.md            ← Contribution guidelines
│   └── LICENSE                    ← MIT License
│
├── 🐳 Docker Configuration
│   ├── docker-compose.yml         ← Main deployment file
│   ├── Dockerfile                 ← Container definition
│   └── requirements_docker.txt    ← Python dependencies
│
├── 📝 Configuration
│   ├── config.example.yaml        ← Configuration template
│   └── config/                    ← Your config (auto-generated)
│       └── .gitkeep
│
├── 🔧 Application
│   └── app/
│       ├── smart_cleanup.py       ← Analysis engine
│       ├── web_ui.py              ← Web server & API
│       └── templates/
│           └── index.html         ← Web interface
│
├── 📊 Runtime Directories
│   ├── reports/                   ← Analysis reports (auto-generated)
│   │   └── .gitkeep
│   └── logs/                      ← Application logs (auto-generated)
│       └── .gitkeep
│
└── 🔒 Git
    └── .gitignore                 ← Git ignore rules
```

## 📄 File Descriptions

### Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| **README.md** | GitHub landing page with overview | Everyone |
| **START_HERE.md** | Welcome guide, choose your path | First-time users |
| **QUICKSTART.md** | Get running in 10 minutes | Beginners |
| **DOCUMENTATION.md** | Complete feature documentation | All users |
| **DEPLOYMENT.md** | Deployment checklist | Deployers |
| **SCHEDULER.md** | Scheduler configuration guide | Advanced users |
| **INDEX.md** | Navigation to all docs | Everyone |
| **CONTRIBUTING.md** | How to contribute | Contributors |
| **CHANGELOG.md** | Version history | Everyone |
| **LICENSE** | MIT License | Legal |

### Application Files

| File | Lines | Description |
|------|-------|-------------|
| **smart_cleanup.py** | ~900 | Main analysis engine |
| **web_ui.py** | ~800 | Flask web server & API |
| **index.html** | ~1425 | Web interface with scheduler GUI |

### Configuration Files

| File | Description |
|------|-------------|
| **docker-compose.yml** | Docker deployment config |
| **Dockerfile** | Container image definition |
| **requirements_docker.txt** | Python dependencies |
| **config.example.yaml** | Configuration template with comments |

## 🚀 Getting Started

### New Users
```
1. Read README.md (this file on GitHub)
2. Read QUICKSTART.md
3. Follow installation steps
4. Access Web UI at http://YOUR-SERVER:8765
```

### Developers
```
1. Fork repository
2. Read CONTRIBUTING.md
3. Make changes
4. Submit pull request
```

## 📊 Statistics

- **Total Files:** 23
- **Documentation:** 12 markdown files (~10,000 lines)
- **Code:** 3 files (~3,125 lines)
- **Languages:** Python, JavaScript, HTML, CSS, YAML
- **Version:** 2.1.0
- **License:** MIT

## 🔧 Key Features

- ✅ Smart cleanup rules (movies + TV shows)
- ✅ Duplicate detection with NL audio priority
- ✅ TV show manual review + continuing series protection
- ✅ Modern web UI with scheduler GUI
- ✅ Sonarr/Radarr integration
- ✅ Scheduled analysis (daily/weekly/monthly)
- ✅ Comprehensive reporting (JSON, HTML, CSV)
- ✅ Complete safety features

## 📝 Notes

### Directories
- `config/`, `reports/`, `logs/` are created automatically
- `.gitkeep` files preserve empty directories in git
- User data files are excluded via `.gitignore`

### Volume Mounts
Docker Compose mounts these directories:
- `./app:/app` - Application code (live updates!)
- `./config:/config` - Configuration
- `./reports:/reports` - Analysis reports
- `./logs:/logs` - Application logs

### Files Not in Git
See `.gitignore` for excluded files:
- `config/config.yaml` (contains secrets)
- `reports/*.json` (generated reports)
- `logs/*.log` (application logs)
- Python cache files

## 🎯 Quick Links

- **Installation:** [QUICKSTART.md](QUICKSTART.md)
- **Configuration:** [DOCUMENTATION.md](DOCUMENTATION.md#configuration)
- **Scheduler Setup:** [SCHEDULER.md](SCHEDULER.md)
- **Troubleshooting:** [DOCUMENTATION.md](DOCUMENTATION.md#troubleshooting)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

## 🆘 Support

- **Documentation:** Start with [INDEX.md](INDEX.md)
- **Issues:** Use GitHub Issues
- **Discussions:** Use GitHub Discussions

---

**Version:** 2.1.0  
**Last Updated:** 2026-01-06  
**License:** MIT
