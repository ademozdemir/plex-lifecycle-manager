# Quick Start Guide 🚀

**Get Plex Lifecycle Manager running in 10 minutes!**

---

## Prerequisites

✅ Docker & Docker Compose installed  
✅ Plex Media Server running  
✅ (Optional) Sonarr running  
✅ (Optional) Radarr running

---

## Installation (3 steps)

### 1. Deploy Files

```bash
# Create directory
mkdir -p /path/to/plex-lifecycle
cd /path/to/plex-lifecycle

# Extract package contents here
# Ensure you have:
# - docker-compose.yml
# - Dockerfile
# - requirements_docker.txt
# - app/ directory with all files
```

### 2. Start Container

```bash
# Build and run
docker-compose up -d

# Verify it's running
docker ps | grep plex-lifecycle
```

### 3. Access Web UI

```
Open browser: http://YOUR-SERVER-IP:8765
```

✅ **You should see the Plex Lifecycle Manager interface!**

---

## Configuration (5 minutes)

### Step 1: Get Your Plex Token

**Quick method:**
1. Open Plex Web App
2. Play any video
3. Click **ⓘ** (info button)
4. Click **"View XML"**
5. Look in URL: `...X-Plex-Token=YOUR_TOKEN_HERE`
6. Copy the token

### Step 2: Configure in Web UI

1. Click **Configuration** tab
2. Enter **Plex Settings:**
   - URL: `http://192.168.1.100:32400` (use your Plex IP)
   - Token: (paste token from Step 1)

3. **(Optional)** Enter **Sonarr Settings:**
   - Enable checkbox
   - URL: `http://192.168.1.100:8989`
   - API Key: (Settings → General → Security → API Key)

4. **(Optional)** Enter **Radarr Settings:**
   - Enable checkbox
   - URL: `http://192.168.1.100:7878`
   - API Key: (Settings → General → Security → API Key)

5. **Cleanup Rules:**
   - Keep defaults for first run
   - ⚠️ **Important:** Uncheck "NL Audio Priority" if you don't use Dutch audio!

6. Click **"Save Configuration"**

✅ **Configuration saved!**

---

## First Analysis (2 steps)

### Step 1: Run Analysis

1. Click **Analysis** tab
2. Click **"Start Analysis"** button
3. Wait 15-30 minutes (grab coffee ☕)
4. Progress bar will show completion

### Step 2: Review Results

1. Click **Reports** tab
2. Click **"View"** on the latest report
3. Review flagged items

**What you'll see:**
- ✅ Movies pre-selected (uncheck to keep)
- ❌ TV Shows NOT pre-selected (check to delete)
- 🟢 Continuing Series (protected, can't delete)

✅ **Analysis complete!**

---

## First Deletion (3 steps - CAREFUL!)

### ⚠️ DANGER ZONE - TEST FIRST! ⚠️

**Start with 1-2 unimportant items!**

### Step 1: Select Test Items

1. In the report, find 1-2 items you DON'T want
2. Make sure they're checked
3. Verify the count: "X items selected"

### Step 2: Execute Deletion

1. Click **"Delete Selected"** button
2. Review the confirmation popup
3. Type **DELETE** (all caps)
4. Click confirm

### Step 3: Verify Results

1. Check Plex - items should be gone
2. Check filesystem - folders should be gone
3. Check backup created in `/reports` directory

✅ **If successful, you can now delete more items!**

---

## Common First-Time Issues

### "Can't connect to Plex"
- Use server IP, not `localhost`
- Check Plex is running
- Verify token is correct
- Test: `curl http://YOUR-PLEX-IP:32400`

### "Port 8765 already in use"
Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:8765"  # Change left side
```

### "No TV shows in report"
This is usually normal! TV shows only appear if they meet cleanup rules:
- Unwatched for 5+ years, OR
- Fully watched 6+ months ago, OR
- Partially watched 2+ years ago

### "Analysis takes forever"
Normal! Analysis time:
- Small library: 5-10 min
- Medium library: 10-20 min
- Large library: 20-40 min

Watch progress: `docker logs -f plex-lifecycle`

---

## Essential Safety Tips

🚨 **READ THIS BEFORE DELETING ANYTHING!** 🚨

1. **No undo** - Deleted files are gone forever
2. **Test first** - Start with 1-2 items
3. **Review carefully** - TV shows require manual selection
4. **Backup important** - Keep copies of irreplaceable media
5. **Check logs** - `docker logs plex-lifecycle`

---

## Quick Reference

### Restart Container
```bash
docker-compose restart
```

### View Logs
```bash
docker logs -f plex-lifecycle
```

### Stop Container
```bash
docker-compose down
```

### Rebuild After Changes
```bash
docker-compose down
docker-compose build
docker-compose up -d
```

---

## Next Steps

Once you're comfortable:

1. **Adjust cleanup rules** in Configuration tab
2. **Run analysis monthly** to keep library clean
3. **Cleanup old reports** using the button in Reports tab
4. **Lower age thresholds** for more aggressive cleanup

---

## Need More Help?

📖 **Full Documentation:** README.md  
📋 **Detailed Deployment:** DEPLOYMENT.md  
🔧 **Troubleshooting:** README.md → Troubleshooting section  
📝 **Version History:** CHANGELOG.md

---

**That's it! You're ready to manage your Plex library! 🎉**

*Remember: Start small, test carefully, and always review before deletion!*
