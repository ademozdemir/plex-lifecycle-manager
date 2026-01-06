# Installation Guide

**Quick installation guide for GitHub users**

---

## 🚀 Quick Install (5 minutes)

### Prerequisites
- Docker & Docker Compose installed
- Plex Media Server running
- (Optional) Sonarr & Radarr

### Steps

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/plex-lifecycle-manager.git
cd plex-lifecycle-manager

# 2. Copy example config (optional - can configure via Web UI)
cp config.example.yaml config/config.yaml
# Edit config/config.yaml if desired

# 3. Start container
docker-compose up -d

# 4. Access Web UI
# Open browser: http://YOUR-SERVER-IP:8765
```

**That's it!** 🎉

---

## ⚙️ Configuration

### Via Web UI (Recommended)

1. Open `http://YOUR-SERVER-IP:8765`
2. Go to **Configuration** tab
3. Enter your details:
   - Plex URL & Token
   - Sonarr URL & API Key (optional)
   - Radarr URL & API Key (optional)
   - Cleanup rules
   - **Important:** Disable "NL Audio Priority" if you don't use Dutch audio!
4. **Scroll down** for Scheduler settings (optional)
5. Click **Save Configuration**

### Finding API Keys

**Plex Token:**
1. Open Plex Web App
2. Play any video
3. Click ⓘ → View XML
4. Copy token from URL: `X-Plex-Token=...`

[Full guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)

**Sonarr/Radarr API Key:**
1. Open Sonarr/Radarr
2. Settings → General → Security
3. Copy API Key

---

## 📊 First Analysis

1. Go to **Analysis** tab
2. Click **Start Analysis**
3. Wait 15-30 minutes (depends on library size)
4. Go to **Reports** tab
5. Click **View** on latest report
6. Review flagged items
7. **Test with 1-2 items first!**

---

## 🕐 Enable Scheduler (Optional)

1. **Configuration** tab → Scroll to **"📅 Scheduled Analysis"**
2. ✅ Enable Scheduled Analysis
3. Choose time & frequency
4. Click **Save Configuration**

---

## 🔧 Advanced Setup

### Custom Port

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:8765"  # Change left side
```

### Custom Timezone

Edit `docker-compose.yml`:
```yaml
environment:
  - TZ=Europe/Amsterdam  # Your timezone
```

### Volume Mounts

Already configured in `docker-compose.yml`:
```yaml
volumes:
  - ./app:/app              # Application code
  - ./config:/config        # Your configuration
  - ./reports:/reports      # Analysis reports
  - ./logs:/logs           # Application logs
```

---

## 🐛 Troubleshooting

### Container won't start
```bash
docker logs plex-lifecycle
```

### Can't connect to Plex
- Use server IP, not `localhost`
- Check firewall
- Verify Plex is running

### Web UI not loading
```bash
# Check container is running
docker ps | grep plex-lifecycle

# Check logs
docker logs plex-lifecycle

# Restart
docker-compose restart
```

### Scheduler not working
```bash
# Check if module is loaded
docker logs plex-lifecycle | grep -i scheduler

# Should show:
# ✓ Scheduler module loaded successfully
```

---

## 📝 Complete Documentation

- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation:** [DOCUMENTATION.md](DOCUMENTATION.md)
- **Scheduler Guide:** [SCHEDULER.md](SCHEDULER.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **All Docs:** [INDEX.md](INDEX.md)

---

## ⚠️ Important

**This tool permanently deletes files!**

- ✅ Test with unimportant items first
- ✅ Review reports carefully before deletion
- ✅ Keep backups of irreplaceable media
- ❌ No undo - deleted files are gone forever

See [LICENSE](LICENSE) for full disclaimer.

---

## 🆘 Need Help?

1. Check [DOCUMENTATION.md](DOCUMENTATION.md) → Troubleshooting
2. Check [INDEX.md](INDEX.md) for navigation
3. Open GitHub Issue
4. Start GitHub Discussion

---

**Happy cleaning!** 🎬
