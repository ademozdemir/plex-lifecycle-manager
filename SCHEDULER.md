# Scheduled Analysis Guide

**Automatic Plex cleanup on a schedule**

Version 2.0.0+

---

## 📋 Overview

The scheduler module allows you to run Plex Lifecycle Manager analysis automatically on a schedule (daily, weekly, or monthly).

**Features:**
- ✅ Automatic analysis execution
- ✅ Flexible scheduling (daily/weekly/monthly)
- ✅ Safe standalone module (won't break if it fails)
- ✅ Comprehensive logging
- ✅ Easy enable/disable via Web UI

**Important:**
- Scheduler is **optional** - manual analysis always works
- Scheduler is **safe** - errors don't affect rest of application
- Scheduler only runs **analysis** - deletion still requires manual approval

---

## 🚀 Quick Setup

### Via Web UI (Easiest)

1. Open Web UI: `http://YOUR-SERVER-IP:8765`
2. Go to **Configuration** tab
3. Scroll to **Schedule** section
4. Enable scheduled analysis
5. Set your preferred schedule
6. Click **Save Configuration**

### Via Config File

Edit `config/config.yaml`:

```yaml
schedule:
  enabled: true                    # Enable scheduled analysis
  time: "03:00"                    # Time to run (HH:MM, 24-hour)
  days: "weekly"                   # Frequency: daily, weekly, monthly
  day_of_week: "mon"               # For weekly (mon-sun)
  day_of_month: 1                  # For monthly (1-31)
```

Then restart container:
```bash
docker-compose restart
```

---

## ⚙️ Configuration Options

### Schedule Frequency

**Daily:**
```yaml
schedule:
  enabled: true
  time: "03:00"
  days: "daily"
```
Runs every day at 3:00 AM.

**Weekly:**
```yaml
schedule:
  enabled: true
  time: "03:00"
  days: "weekly"
  day_of_week: "mon"     # mon, tue, wed, thu, fri, sat, sun
```
Runs every Monday at 3:00 AM.

**Monthly:**
```yaml
schedule:
  enabled: true
  time: "03:00"
  days: "monthly"
  day_of_month: 1        # 1-31
```
Runs on the 1st of every month at 3:00 AM.

### Time Format

Use 24-hour format (HH:MM):
- `"03:00"` = 3:00 AM
- `"15:30"` = 3:30 PM
- `"00:00"` = Midnight
- `"23:59"` = 11:59 PM

---

## 📊 Monitoring

### Check Scheduler Status

**Via Web UI:**
1. Open Configuration tab
2. Check "Schedule Status" section
3. See: Enabled, Next Run Time

**Via Logs:**
```bash
docker logs plex-lifecycle | grep -i schedule

# Expected output:
# ✓ Scheduler module loaded successfully
# ✓ Scheduled analysis configured: weekly on mon at 03:00
# Scheduled analysis thread started successfully
```

### Check Next Run Time

**Via API:**
```bash
curl http://localhost:8765/api/schedule/status
```

Response:
```json
{
  "enabled": true,
  "available": true,
  "running": true,
  "next_run": "2026-01-13T03:00:00",
  "config": {
    "enabled": true,
    "time": "03:00",
    "days": "weekly",
    "day_of_week": "mon"
  }
}
```

---

## 🔍 How It Works

### Execution Flow

1. **Schedule Time Arrives**
   - Scheduler wakes up at configured time
   - Checks if analysis is already running (skips if yes)
   - Loads configuration

2. **Verify Configuration**
   - Checks if scheduling is still enabled
   - Validates configuration

3. **Run Analysis**
   - Starts analysis in background thread
   - Same as manual analysis
   - Logs all activity

4. **Complete**
   - Reports generated in `/reports`
   - Ready for manual review and deletion

### What Gets Executed

**Scheduled:**
- ✅ Library scanning
- ✅ Rule application
- ✅ Duplicate detection
- ✅ Continuing series check
- ✅ Report generation

**NOT Scheduled (Manual Only):**
- ❌ Deletion execution
- ❌ File removal
- ❌ Report cleanup

**Why?** Safety! Deletion requires explicit user confirmation.

---

## 🛡️ Safety Features

### Built-in Protections

1. **Skip if Running**
   - Won't start if analysis already in progress
   - Prevents overlapping analyses

2. **Error Isolation**
   - Scheduler errors don't crash application
   - Manual analysis always works

3. **Configuration Checks**
   - Verifies config before running
   - Disables gracefully if misconfigured

4. **Comprehensive Logging**
   - All scheduler activity logged
   - Easy troubleshooting

---

## 🐛 Troubleshooting

### Scheduler Not Running

**Check if module is loaded:**
```bash
docker logs plex-lifecycle | grep "Scheduler module"

# Expected:
# ✓ Scheduler module loaded successfully

# If error:
# ⚠ Scheduler module not available: ...
```

**Solution:** Rebuild container
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Scheduled Analysis Not Executing

**Check configuration:**
```bash
# View current config
cat config/config.yaml | grep -A 6 "schedule:"

# Verify enabled: true
```

**Check logs:**
```bash
docker logs plex-lifecycle | grep -i "scheduled"

# Look for:
# - "Scheduled analysis started"
# - "Scheduled analysis skipped" (if already running)
# - Error messages
```

**Verify schedule:**
```bash
# Check next run time
curl http://localhost:8765/api/schedule/status | jq .next_run

# Returns: "2026-01-13T03:00:00"
```

### Analysis Runs But Reports Not Generated

**This is a config issue, not scheduler issue!**

Check:
1. Plex credentials correct?
2. Libraries configured?
3. Check analysis logs for errors

### Time Zone Issues

Scheduler uses **container time zone** (default: UTC).

**To change time zone:**

Edit `docker-compose.yml`:
```yaml
services:
  plex-lifecycle:
    environment:
      - TZ=Europe/Amsterdam  # Your timezone
```

Restart:
```bash
docker-compose restart
```

---

## 📝 Best Practices

### Recommended Schedules

**For Active Libraries:**
- Weekly analysis
- Off-peak hours (e.g., 3:00 AM)
- Day with low server usage

**For Stable Libraries:**
- Monthly analysis
- Any time that's convenient
- 1st of month for easy tracking

**For Testing:**
- Daily analysis
- Check reports regularly
- Adjust rules based on results

### Resource Considerations

**Analysis is CPU/IO intensive:**
- Run during off-peak hours
- Avoid during Plex streaming times
- Consider server load

**Typical analysis time:**
- Small library (<500 items): 5-10 min
- Medium library (500-1000): 10-20 min
- Large library (1000+): 20-40 min

### Monitoring

**Check reports regularly:**
- Review flagged items
- Adjust rules if needed
- Delete items when ready

**Watch for patterns:**
- Same items flagged repeatedly?
- Rules too aggressive/conservative?
- Unexpected continuing series?

---

## 🔧 Advanced Configuration

### Multiple Schedules (Not Supported)

Currently, only one schedule is supported. For multiple schedules, you could:
- Use external cron (advanced)
- Run manual analyses as needed

### External Cron Integration

If you need more complex scheduling:

```bash
# External cron entry
0 3 * * 1 docker exec plex-lifecycle curl -X POST http://localhost:8765/api/analysis/start
```

**Note:** This bypasses scheduler module but works fine.

---

## 📊 Example Configurations

### Home User - Weekly Cleanup

```yaml
schedule:
  enabled: true
  time: "03:00"           # 3 AM
  days: "weekly"
  day_of_week: "mon"      # Monday morning
```

**Why:** Weekly keeps library clean, Monday gives you weekend viewing time.

### Power User - Daily Analysis

```yaml
schedule:
  enabled: true
  time: "04:00"           # 4 AM
  days: "daily"
```

**Why:** Active library, want tight control, don't mind daily reports.

### Casual User - Monthly Check

```yaml
schedule:
  enabled: true
  time: "02:00"           # 2 AM
  days: "monthly"
  day_of_month: 1         # 1st of month
```

**Why:** Stable library, don't add content often, monthly is enough.

---

## 🔄 Disabling Scheduler

### Temporary Disable (Keep Config)

**Via Web UI:**
1. Configuration tab
2. Uncheck "Enable Scheduled Analysis"
3. Save Configuration

**Via Config:**
```yaml
schedule:
  enabled: false
  # Other settings preserved
```

### Permanent Disable (Remove Module)

**Not recommended** - scheduler is safe and lightweight.

If you really want to remove it:
1. Remove APScheduler from requirements_docker.txt
2. Rebuild container: `docker-compose build --no-cache`

**Better:** Just disable it in config!

---

## ❓ FAQ

**Q: Will scheduled analysis delete files automatically?**
A: No! Scheduler only runs analysis. Deletion requires manual approval via Web UI.

**Q: What if analysis fails during scheduled run?**
A: Error is logged, scheduler continues, manual analysis still works. No harm done.

**Q: Can I force a scheduled analysis now?**
A: No, but you can run manual analysis which is the same thing!

**Q: Does scheduler affect manual analysis?**
A: No! Manual analysis works independently. Scheduler is just automation.

**Q: What time zone does scheduler use?**
A: Container time zone (default: UTC). Set TZ environment variable to change.

**Q: Can I have multiple schedules?**
A: No, only one schedule supported. Use external cron for complex schedules.

---

## 📞 Support

- **Not working?** Check logs: `docker logs plex-lifecycle | grep -i schedule`
- **Configuration help?** See [config.example.yaml](config.example.yaml)
- **General issues?** See [README.md#troubleshooting](README.md#-troubleshooting)

---

## 🎉 Summary

**Scheduler module provides:**
- ✅ Automatic analysis execution
- ✅ Flexible scheduling options
- ✅ Safe, isolated operation
- ✅ Easy enable/disable

**Remember:**
- Scheduler is **optional**
- Scheduler only runs **analysis**
- Deletion requires **manual approval**
- Manual analysis **always available**

**Enjoy automated Plex cleanup!** 🚀
