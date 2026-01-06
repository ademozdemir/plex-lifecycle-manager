# Scheduler GUI Update - Deployment Instructions

**Version 2.1.0 - Scheduler GUI Added!**

---

## 🎉 What's New

### ✅ Schedule Configuration in Web UI!

**New Features:**
- 📅 **Schedule Tab in Configuration** - Enable/disable scheduled analysis
- ⏰ **Time Picker** - Choose when to run (24-hour format)
- 📆 **Frequency Options** - Daily, Weekly, or Monthly
- 📊 **Live Status Display** - See next scheduled run time
- 🎯 **Smart UI** - Shows/hides relevant fields based on frequency

**Location:** Configuration tab → Scroll down to "📅 Scheduled Analysis"

---

## 🚀 Deployment (Quick Update)

### **What You Need:**

**Only 1 file to update:**
- `index.html` (Web UI with scheduler GUI)

**APScheduler should already be installed from previous update!**

---

## 📋 Step-by-Step Deployment

### **Step 1: Upload Updated File**

**Via File Station:**
1. Download `index.html` from above
2. Open Synology File Station
3. Navigate to: `/volume1/docker/plex-lifecycle/app/templates/`
4. Backup current: Download `index.html` → Rename to `index.html.backup`
5. Upload new `index.html`

---

### **Step 2: Restart Container**

```bash
cd /volume1/docker/plex-lifecycle
sudo docker-compose restart
```

**Wait ~10 seconds for startup**

---

### **Step 3: Clear Browser Cache**

**Hard Refresh:**
- **Windows:** `Ctrl + Shift + R` or `Ctrl + F5`
- **Mac:** `Cmd + Shift + R`
- **Or:** Clear browser cache manually

---

### **Step 4: Verify Scheduler GUI**

1. Open Web UI: `http://192.168.178.61:8765`
2. Go to **Configuration** tab
3. Scroll down
4. You should see: **"📅 Scheduled Analysis"** section!

---

## 🎯 Using the Scheduler GUI

### **Enable Scheduled Analysis:**

1. **Configuration Tab** → Scroll to "📅 Scheduled Analysis"
2. ✅ **Check "Enable Scheduled Analysis"**
3. Settings appear below:
   - **Time:** Choose run time (e.g., 03:00)
   - **Frequency:** Daily/Weekly/Monthly
   - **Day:** Choose day (if Weekly/Monthly)
4. **Status box appears** showing schedule info
5. Click **"💾 Save Configuration"**
6. Confirmation shows schedule is enabled!

---

### **Schedule Examples:**

**Daily at 3 AM:**
```
✅ Enable Scheduled Analysis
Time: 03:00
Frequency: Daily
```

**Weekly Monday 3 AM:**
```
✅ Enable Scheduled Analysis
Time: 03:00
Frequency: Weekly
Day of Week: Monday
```

**Monthly 1st at 3 AM:**
```
✅ Enable Scheduled Analysis
Time: 03:00
Frequency: Monthly
Day of Month: 1
```

---

## 📊 Schedule Status Display

**After enabling, you'll see:**

```
📊 Schedule Status:
✅ Active: Weekly on Monday at 03:00
⏰ Next run: Monday, Jan 13, 2026 at 3:00:00 AM
```

**Updates automatically when you save!**

---

## 🔍 Verification

### **Check Scheduler is Working:**

```bash
# 1. Container logs
docker logs plex-lifecycle | grep -i schedule

# Should show:
# ✓ Scheduler module loaded successfully
# ✓ Scheduled analysis configured: weekly on mon at 03:00
# ✓ Scheduler started successfully

# 2. Check via API
curl http://192.168.178.61:8765/api/schedule/status

# Should return JSON with enabled: true
```

---

## 🎨 GUI Features

### **Smart UI:**
- Checkbox shows/hides settings
- Frequency changes relevant fields:
  - **Daily:** No day selection
  - **Weekly:** Day of week dropdown
  - **Monthly:** Day of month input
- Live status updates on save
- Clear error messages if API fails

### **Info Box:**
```
ℹ️ Automatic Analysis
Schedule automatic analysis to run at specific times. 
Analysis only - deletion still requires manual approval.
```

---

## ⚠️ Important Notes

### **Scheduler Behavior:**

1. **Analysis Only**
   - Scheduler runs analysis
   - Reports generated automatically
   - Deletion STILL requires manual approval

2. **Skip if Running**
   - Won't start if analysis already in progress
   - Logs show "skipped"

3. **Time Zone**
   - Uses container time (UTC by default)
   - Set `TZ` environment variable to change

---

## 🐛 Troubleshooting

### **"Schedule Status" Not Showing:**

**Solution:**
```bash
# Verify API is working
curl http://localhost:8765/api/schedule/status

# Should return JSON
# If error: Check web_ui.py has schedule endpoints
```

---

### **Changes Not Saving:**

**Check:**
1. Browser cache cleared? (Ctrl+Shift+R)
2. Check browser console (F12) for errors
3. Check logs: `docker logs plex-lifecycle`

---

### **Status Shows "Module Not Available":**

**Solution:**
```bash
# Install APScheduler
docker exec plex-lifecycle pip install APScheduler==3.10.4 --break-system-packages

# Restart
docker-compose restart
```

---

## ✅ Success Checklist

After deployment:
- [ ] index.html uploaded to `/app/templates/`
- [ ] Container restarted
- [ ] Browser cache cleared
- [ ] Configuration tab shows "📅 Scheduled Analysis"
- [ ] Can enable/disable scheduler
- [ ] Status displays correctly
- [ ] Save button shows confirmation with schedule info
- [ ] Logs confirm scheduler configuration

---

## 📸 What You'll See

### **Configuration Tab (Scrolled Down):**

```
┌────────────────────────────────────────────┐
│ Duplicate Detection                        │
│ ✅ Enable Duplicate Detection              │
├────────────────────────────────────────────┤
│                                            │
│ 📅 Scheduled Analysis                     │
│                                            │
│ ℹ️ Automatic Analysis                     │
│ Schedule automatic analysis...             │
│                                            │
│ ✅ Enable Scheduled Analysis               │
│                                            │
│   Time: [03:00]                           │
│   Frequency: [Weekly ▼]                   │
│   Day of Week: [Monday ▼]                 │
│                                            │
│   📊 Schedule Status:                     │
│   ✅ Active: Weekly on Monday at 03:00    │
│   ⏰ Next run: Monday, Jan 13...          │
│                                            │
│ [💾 Save Configuration]                    │
└────────────────────────────────────────────┘
```

---

## 🎉 Done!

You now have full GUI control over scheduled analysis!

- ✅ Visual configuration
- ✅ Live status updates
- ✅ Easy enable/disable
- ✅ Clear feedback

**Enjoy your automated Plex cleanup!** 🚀
