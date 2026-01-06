# Deployment Checklist

## 📦 Complete Package Contents

This package contains everything you need to deploy Plex Lifecycle Manager:

### Required Files
```
plex-lifecycle-manager/
├── README.md                    ← Start here! Full documentation
├── docker-compose.yml           ← Docker deployment config
├── Dockerfile                   ← Container image definition
├── requirements_docker.txt      ← Python dependencies
│
├── app/
│   ├── smart_cleanup.py        ← Analysis engine
│   ├── web_ui.py               ← Web server & API
│   └── templates/
│       └── index.html          ← Web interface
│
├── config/                      ← Auto-created on first run
├── reports/                     ← Auto-created on first run
└── logs/                        ← Auto-created on first run
```

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Prepare Files
```bash
# Create base directory
mkdir -p /path/to/plex-lifecycle
cd /path/to/plex-lifecycle

# Copy all files from package to this directory
# Ensure directory structure matches above
```

### Step 2: Start Container
```bash
# Build and start
docker-compose up -d

# Check if running
docker ps | grep plex-lifecycle
```

### Step 3: Access Web UI
```
Open browser: http://YOUR-SERVER-IP:8765
```

### Step 4: Configure
1. Go to Configuration tab
2. Enter Plex URL and Token
3. (Optional) Enter Sonarr/Radarr details
4. Configure cleanup rules
5. **Important:** Disable "NL Audio Priority" if you don't use Dutch audio!
6. Save configuration

### Step 5: Run First Analysis
1. Go to Analysis tab
2. Click "Start Analysis"
3. Wait 15-30 minutes
4. Go to Reports tab
5. Review results

---

## ⚙️ Configuration Quick Reference

### Minimum Required
- **Plex URL**: `http://192.168.1.100:32400`
- **Plex Token**: Get from Plex Web App (see README)

### Recommended
- **Sonarr**: Enables continuing series protection
- **Radarr**: Enables unmonitoring before deletion

### Important Settings
- **NL Audio Priority**: 
  - ✅ Enable if you use Dutch audio
  - ❌ Disable if you don't (prevents keeping low-quality versions)

---

## 🔍 Finding Credentials

### Plex Token
1. Open Plex Web App
2. Play any item
3. Click ⓘ → View XML
4. Look in URL: `X-Plex-Token=XXXXX`

Full guide: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

### Sonarr API Key
Settings → General → Security → API Key

### Radarr API Key
Settings → General → Security → API Key

---

## ✅ Verification Steps

### After Deployment
- [ ] Container is running: `docker ps`
- [ ] Web UI accessible: `http://SERVER:8765`
- [ ] Configuration saved successfully
- [ ] Analysis completes without errors
- [ ] Report generated in Reports tab

### Before First Deletion
- [ ] Reviewed report carefully
- [ ] Tested with 1-2 unimportant items
- [ ] Verified files actually deleted
- [ ] Confirmed Plex updated correctly
- [ ] Checked backup file created

---

## 🛟 Quick Troubleshooting

### Container won't start
```bash
docker logs plex-lifecycle
# Look for error messages
```

### Can't connect to Plex
- Use server IP, not localhost
- Check firewall
- Verify Plex is running
- Test: `curl http://PLEX-IP:32400`

### Analysis hangs
```bash
docker logs -f plex-lifecycle
# Watch for errors or progress
```

### Need to restart
```bash
docker-compose restart
```

### Need to rebuild
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

---

## 📊 Expected Timeline

### First Analysis (varies by library size)
- Small (<500 items): 5-10 minutes
- Medium (500-1000): 10-20 minutes
- Large (1000+ items): 20-40 minutes

### Deletion (per item)
- Movies: 1-5 seconds
- TV Shows: 10-30 seconds (depends on episode count)

---

## ⚠️ Safety Reminders

1. **No undo** - Deleted files are gone forever
2. **Test first** - Start with 1-2 items
3. **Backup important** - Keep copies of irreplaceable media
4. **Review carefully** - TV shows require manual selection for a reason
5. **Check logs** - If something seems wrong, check logs first

---

## 📝 Maintenance Schedule

### Weekly
- None required!

### Monthly
- Run analysis
- Review and delete flagged items
- Check logs for recurring errors

### Quarterly
- Cleanup old reports (built-in button)
- Review cleanup rules
- Adjust thresholds if needed

---

## 💡 Pro Tips

1. **Conservative start**: Use high age thresholds initially (5+ years)
2. **Gradual adjustment**: Lower thresholds after you're comfortable
3. **TV show caution**: Always manually review TV shows
4. **Regular runs**: Monthly analysis keeps library clean
5. **Log review**: Check logs occasionally for silent errors

---

## 🆘 Getting Help

### Check These First
1. README.md - Complete documentation
2. Docker logs: `docker logs plex-lifecycle`
3. Web UI logs: Check /logs directory
4. Analysis reports: Check /reports directory

### Common Issues
- **Port conflict**: Change port in docker-compose.yml
- **Permission errors**: Ensure directories writable
- **Connection refused**: Check firewalls and IPs
- **Timeout errors**: Already fixed in v2 (120s timeout)

---

## 📄 File Customization Guide

### Want to change the port?
**Edit:** `docker-compose.yml`
```yaml
ports:
  - "8080:8765"  # Change left side only
```

### Want to change cleanup rules?
**Option 1:** Web UI → Configuration tab (recommended)
**Option 2:** Edit `config/config.yaml` directly

### Want to change timeout for large TV shows?
**Edit:** `app/web_ui.py`
```python
plex = PlexServer(plex_url, plex_token, timeout=180)  # Increase
```

### Want to disable NL audio priority?
**Web UI:** Configuration → Uncheck "NL Audio Priority"
**Or edit:** `config/config.yaml`
```yaml
duplicates:
  nl_audio_priority: false
```

---

## 🎯 Success Criteria

You'll know it's working when:
- ✅ Analysis completes without errors
- ✅ Reports show sensible deletion candidates
- ✅ Test deletions work correctly
- ✅ Files disappear from disk
- ✅ Plex updates immediately
- ✅ Backups are created
- ✅ No errors in logs

---

**Ready to deploy? Start with README.md for full documentation!**
