# Changelog

All notable changes to Plex Lifecycle Manager will be documented in this file.

## [2.0.0] - 2026-01-06

### Major Release - Execute Mode V2

#### Added
- **Execute Mode V2** - Complete deletion workflow
  - Movie pre-selection (auto-flagged items)
  - TV show manual review (user must select)
  - Continuing series protection (Sonarr integration)
  - Batch deletion with confirmation
  - Real-time progress tracking
  - Complete file and folder cleanup
  
- **Web UI Enhancements**
  - Modern, responsive interface
  - Pagination support (20/50/100/All items per page)
  - Filter by Movies/TV Shows/All
  - Selection controls (Select All Movies, Select All Visible, Deselect All)
  - Visual badges (Continuing Series, Manual Review, NL Audio)
  - Type "DELETE" confirmation for safety
  
- **Report Management**
  - Cleanup old reports feature
  - Keep last N reports (configurable)
  - Automatic backup cleanup (keeps last 10)
  - Delete JSON, HTML, CSV reports together
  
- **Enhanced Deletion**
  - Increased timeout (120s) for large TV shows
  - Automatic folder cleanup after file deletion
  - Season folder removal for TV shows
  - Complete metadata cleanup (.nfo, .jpg, etc.)
  - Sonarr/Radarr unmonitoring before deletion
  
- **TV Show Logic**
  - Continuing series detection via Sonarr
  - Three TV show rules:
    - Unwatched age (never watched)
    - Fully watched age (completed shows)
    - Partially watched age (abandoned shows)
  - Manual review required for all TV shows
  - Continuing series cannot be deleted
  
- **Dutch Audio Priority** (Optional)
  - Configurable NL audio prioritization
  - Can be disabled for non-Dutch users
  - Prefers Dutch audio over quality when enabled
  - Quality-based selection when disabled

#### Changed
- Complete UI redesign with modern styling
- Improved error handling and logging
- Better type consistency (String vs Number) throughout
- Enhanced duplicate detection logic
- Streamlined configuration interface

#### Fixed
- Checkbox selection type mismatch bug
- Continuing series visibility in reports
- Delete execution "items not found" error
- Folder cleanup not removing empty directories
- TV shows not appearing in reports (missing rules)
- Dragon Ball Super timeout error (112 episodes)
- Various JavaScript type coercion issues

---

## [1.0.0] - Initial Release

### Added
- Basic analysis engine
- Duplicate detection
- Movie cleanup rules
- HTML/CSV/JSON report generation
- Plex integration
- Sonarr/Radarr integration
- Docker deployment
- Configuration management

---

## Development Notes

### Known Limitations
- No scheduler (manual execution required)
- No multi-user support
- Title matching may fail if names differ in Sonarr/Radarr
- Backup contains metadata only, not media files
- No undo functionality

### Future Considerations
- Scheduled analysis (cron job)
- Multi-user authentication
- More granular TV show rules
- Custom rule sets per library
- Email notifications
- Statistics dashboard
- Search functionality in reports

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible changes
- MINOR version for added functionality
- PATCH version for bug fixes

---

## Migration Notes

### From 1.x to 2.0
1. Backup your `config/config.yaml`
2. Pull new code
3. Rebuild container: `docker-compose build`
4. Start container: `docker-compose up -d`
5. Configuration is preserved automatically
6. New TV show rules will be added to config
7. Old reports remain compatible

### Configuration Changes in 2.0
- Added `tv_shows` rules section
- Added `kids_series` rules section
- Added `anime` rules section
- Added `execution` section
- No breaking changes to existing movie rules

---

## Credits

Developed for personal use managing a Plex library with Dutch audio priority.

Special focus on:
- Safety (manual TV review, confirmations, backups)
- Flexibility (configurable rules, filtering, selection)
- Quality (NL audio priority, duplicate detection)
- Usability (modern UI, clear workflows)
