# Libraries Configuration Guide

**How Plex Lifecycle Manager detects and uses your libraries**

---

## 🔍 Overview

Plex Lifecycle Manager needs to know which Plex libraries to analyze. There are two ways to configure this:

1. **Automatic Detection (Recommended)** - Configure via Web UI
2. **Manual Configuration** - Edit config.yaml directly

---

## ✅ Method 1: Automatic Detection (Recommended)

### How It Works

When you save configuration in the Web UI:
1. Tool connects to your Plex server
2. Retrieves all available libraries
3. Auto-detects library types (movie/show)
4. Saves to config.yaml automatically

### Steps

```
1. Open Web UI: http://YOUR-SERVER:8765
2. Configuration tab
3. Enter Plex URL and Token
4. Click "Save Configuration"
5. Libraries are auto-detected!
```

**That's it!** No manual configuration needed.

---

## 🔧 Method 2: Manual Configuration

### When to Use

- Web UI auto-detection fails
- You want to exclude certain libraries
- You want custom rule mappings
- Advanced use cases

### Finding Library IDs

**Option A: Via Plex Web App**
1. Open Plex Web App
2. Go to a library
3. Look at URL: `https://app.plex.tv/desktop/#!/server/.../section/3`
4. The number after `/section/` is the library ID (e.g., 3)

**Option B: Via API**
```bash
# Replace with your details
curl "http://YOUR-PLEX-IP:32400/library/sections?X-Plex-Token=YOUR_TOKEN"

# Look for <Directory key="X"> where X is the ID
```

### Configuration Format

Edit `config/config.yaml`:

```yaml
libraries:
  - id: 1                    # Plex library ID
    name: "Movies"           # Library name (for display)
    type: "movie"            # Type: "movie" or "show"
    rules: "movies"          # Which rule set to use
  
  - id: 3
    name: "TV Shows"
    type: "show"
    rules: "tv_shows"
  
  - id: 5
    name: "Anime"
    type: "show"
    rules: "anime"           # Can use different rules
```

---

## 📝 Understanding Fields

### `id` (Required)
- Plex library ID (integer)
- Find via Plex Web App URL or API
- **Different for each Plex server!**

### `name` (Required)
- Display name for the library
- Used in reports and logs
- Can be anything, doesn't have to match Plex

### `type` (Required)
- `"movie"` - For movie libraries
- `"show"` - For TV show libraries
- Must match actual library type in Plex

### `rules` (Required)
- Which rule set to apply (see rules section in config)
- Common values:
  - `"movies"` - Standard movie rules
  - `"kids_movies"` - Movies for kids (shorter retention)
  - `"tv_shows"` - Standard TV show rules
  - `"kids_series"` - TV shows for kids
  - `"anime"` - Anime-specific rules
- Can create custom rule sets

---

## 🎯 Common Configurations

### Basic Setup (2 Libraries)
```yaml
libraries:
  - id: 1
    name: "Movies"
    type: "movie"
    rules: "movies"
  
  - id: 2
    name: "TV Shows"
    type: "show"
    rules: "tv_shows"
```

### With Kids Content (4 Libraries)
```yaml
libraries:
  - id: 1
    name: "Movies"
    type: "movie"
    rules: "movies"
  
  - id: 2
    name: "Kids Movies"
    type: "movie"
    rules: "kids_movies"      # Different rules for kids
  
  - id: 3
    name: "TV Shows"
    type: "show"
    rules: "tv_shows"
  
  - id: 4
    name: "Kids Shows"
    type: "show"
    rules: "kids_series"
```

### With Anime (Separate Rules)
```yaml
libraries:
  - id: 1
    name: "Movies"
    type: "movie"
    rules: "movies"
  
  - id: 2
    name: "TV Shows"
    type: "show"
    rules: "tv_shows"
  
  - id: 5
    name: "Anime"
    type: "show"
    rules: "anime"            # Different rules for anime
```

---

## ⚠️ Common Issues

### "Error: 'libraries'" During Analysis

**Cause:** Libraries section missing or empty

**Fix:**
```yaml
# Make sure you have at least one library:
libraries:
  - id: 1
    name: "Movies"
    type: "movie"
    rules: "movies"
```

### "Library Not Found" Error

**Cause:** Library ID doesn't exist in Plex

**Fix:**
1. Verify library ID in Plex Web App URL
2. Check Plex server is accessible
3. Verify Plex token is correct

### Analysis Runs But No Results

**Cause:** Wrong library type (e.g., type: "movie" for a TV show library)

**Fix:**
- Verify library type in Plex
- Update config.yaml to match
- Restart container

### Auto-Detection Not Working

**Cause:** Plex connection issue or permissions

**Fix:**
1. Verify Plex URL is correct
2. Verify Plex token has permissions
3. Check Plex server is running
4. Try manual configuration

---

## 🔍 Verifying Configuration

### Check Current Libraries

```bash
# View current config
cat /path/to/plex-lifecycle/config/config.yaml | grep -A 20 "libraries:"
```

### Test Connection

```bash
# Check if Plex is accessible
curl "http://YOUR-PLEX-IP:32400/library/sections?X-Plex-Token=YOUR_TOKEN"
```

### Check Logs

```bash
# View analysis logs
docker logs plex-lifecycle | grep -i library

# Should show:
# Scanning library: Movies (1)
# Scanning library: TV Shows (3)
```

---

## 🎓 Advanced Topics

### Custom Rule Sets

Create your own rule sets in config.yaml:

```yaml
rules:
  # Custom rule for documentaries
  documentaries:
    unwatched_age_years: 10.0    # Keep longer
    watched_age_years: 5.0
    low_rating_threshold: 4.0    # Higher threshold

libraries:
  - id: 7
    name: "Documentaries"
    type: "movie"
    rules: "documentaries"       # Use custom rules
```

### Excluding Libraries

Simply don't add them to the libraries list!

If auto-detected, remove them from config.yaml after first run.

### Multiple Instances

Each Plex server needs its own config.yaml with different library IDs.

---

## 📝 Best Practices

1. **Start with auto-detection** - Easiest and most reliable
2. **Use descriptive names** - Helps in reports and logs
3. **Match rule sets to content** - Kids content needs different rules
4. **Test with one library first** - Verify setup before adding all
5. **Document custom rules** - Add comments in config.yaml

---

## 🆘 Getting Help

### If Auto-Detection Fails:
1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Verify Plex credentials
3. Check logs: `docker logs plex-lifecycle`
4. Try manual configuration

### If Manual Configuration Fails:
1. Verify library IDs are correct
2. Check library types match Plex
3. Ensure rules section exists
4. Restart container after changes

---

## 💡 Examples From Real Users

### Example 1: Simple Home Setup
```yaml
libraries:
  - id: 1
    name: "Movies"
    type: "movie"
    rules: "movies"
  
  - id: 2
    name: "Shows"
    type: "show"
    rules: "tv_shows"
```

### Example 2: Family Server
```yaml
libraries:
  - id: 1
    name: "Adult Movies"
    type: "movie"
    rules: "movies"
  
  - id: 2
    name: "Kids Movies"
    type: "movie"
    rules: "kids_movies"
  
  - id: 3
    name: "TV Series"
    type: "show"
    rules: "tv_shows"
  
  - id: 4
    name: "Kids Shows"
    type: "show"
    rules: "kids_series"
```

### Example 3: Media Enthusiast
```yaml
libraries:
  - id: 1
    name: "Movies"
    type: "movie"
    rules: "movies"
  
  - id: 2
    name: "4K Movies"
    type: "movie"
    rules: "movies"           # Same rules, different library
  
  - id: 3
    name: "TV Shows"
    type: "show"
    rules: "tv_shows"
  
  - id: 4
    name: "Anime Series"
    type: "show"
    rules: "anime"
  
  - id: 5
    name: "Anime Movies"
    type: "movie"
    rules: "movies"
```

---

**Questions? Check [DOCUMENTATION.md](DOCUMENTATION.md) or open a GitHub issue!**
