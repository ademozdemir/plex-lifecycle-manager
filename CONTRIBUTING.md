# Contributing to Plex Lifecycle Manager

Thank you for considering contributing to Plex Lifecycle Manager! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)
- [Testing](#testing)

---

## Code of Conduct

Be respectful, constructive, and professional. This is a community project.

---

## How Can I Contribute?

### Reporting Bugs

**Before submitting a bug report:**
- Check existing issues
- Verify you're using the latest version
- Test with default configuration

**Include in your bug report:**
- Plex Lifecycle Manager version
- Docker version
- Plex Media Server version
- Configuration (without sensitive data!)
- Steps to reproduce
- Expected vs actual behavior
- Logs (`docker logs plex-lifecycle`)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
- Check if suggestion already exists
- Explain the problem you're solving
- Describe your proposed solution
- Consider backwards compatibility

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## Development Setup

### Prerequisites

- Docker & Docker Compose
- Python 3.12 (for local development)
- Plex Media Server (for testing)
- (Optional) Sonarr/Radarr

### Local Development

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/plex-lifecycle-manager.git
cd plex-lifecycle-manager

# Build and run
docker-compose up -d

# View logs
docker logs -f plex-lifecycle

# Access Web UI
http://localhost:8765
```

### File Structure

```
app/
├── smart_cleanup.py       # Main analysis engine
├── web_ui.py              # Flask web server & API
└── templates/
    └── index.html         # Web interface
```

See [PACKAGE_CONTENTS.md](PACKAGE_CONTENTS.md) for detailed file descriptions.

---

## Pull Request Process

### 1. Branch Naming

- Feature: `feature/description`
- Bug fix: `fix/description`
- Documentation: `docs/description`

Examples:
- `feature/email-notifications`
- `fix/timeout-large-tv-shows`
- `docs/improve-quickstart`

### 2. Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add email notification support"
- "Fix timeout for large TV show deletions"
- "Update README with scheduler documentation"

Bad:
- "Update code"
- "Fix bug"
- "Changes"
```

### 3. Code Changes

- Follow existing code style
- Add comments for complex logic
- Update documentation if needed
- Test thoroughly before submitting

### 4. Pull Request Description

Include:
- What problem does this solve?
- How does it solve it?
- Any breaking changes?
- Testing performed
- Screenshots (for UI changes)

### 5. Review Process

- Maintainers will review your PR
- Address feedback and requested changes
- Once approved, PR will be merged

---

## Coding Guidelines

### Python Code (smart_cleanup.py, web_ui.py)

**Style:**
- Follow PEP 8
- Use type hints where possible
- Keep functions focused and small
- Add docstrings to functions

**Example:**
```python
def analyze_item(item: MediaItem, rules: dict) -> bool:
    """
    Analyze a single media item against cleanup rules
    
    Args:
        item: MediaItem to analyze
        rules: Dict of cleanup rules
        
    Returns:
        bool: True if item should be deleted
    """
    # Implementation
    pass
```

**Error Handling:**
```python
# Always use try-except for external operations
try:
    plex_item = plex.fetchItem(item_id)
except Exception as e:
    logger.error(f"Failed to fetch item: {e}")
    return False
```

### JavaScript/HTML (index.html)

**Style:**
- Use `const` and `let`, not `var`
- Use template literals for strings
- Keep functions focused
- Add comments for complex logic

**Example:**
```javascript
async function loadReports() {
    try {
        const response = await fetch('/api/reports');
        const data = await response.json();
        // Process data
    } catch (error) {
        console.error('Failed to load reports:', error);
    }
}
```

### YAML Configuration

**Style:**
- Use 2-space indentation
- Add comments for all options
- Group related settings

**Example:**
```yaml
# Cleanup rules
rules:
  movies:
    unwatched_age_years: 5.0  # Delete if unwatched for 5 years
    watched_age_years: 2.0    # Delete if last viewed 2 years ago
```

---

## Testing

### Before Submitting PR

**1. Manual Testing:**
- Test with default configuration
- Test with custom configuration
- Test error scenarios
- Test edge cases

**2. Container Testing:**
```bash
# Rebuild container
docker-compose down
docker-compose build
docker-compose up -d

# Verify functionality
docker logs plex-lifecycle
```

**3. Safety Testing:**
- Test with non-important media first
- Verify backups are created
- Verify files are actually deleted
- Verify Plex updates correctly

### Test Checklist

- [ ] Container builds successfully
- [ ] Web UI loads correctly
- [ ] Configuration saves properly
- [ ] Analysis completes without errors
- [ ] Reports generate correctly
- [ ] Deletion works (test with 1-2 items!)
- [ ] Logs show no unexpected errors
- [ ] Documentation updated if needed

---

## Areas Needing Contribution

### High Priority

- [ ] Unit tests for smart_cleanup.py
- [ ] Integration tests for web_ui.py
- [ ] Email notification support
- [ ] Multi-user authentication
- [ ] More granular TV show rules

### Medium Priority

- [ ] Statistics dashboard
- [ ] Search functionality in reports
- [ ] Custom rule sets per library
- [ ] Improved duplicate detection
- [ ] Better error messages

### Low Priority

- [ ] Dark mode for Web UI
- [ ] Mobile app
- [ ] Plex plugin version
- [ ] Alternative database backends

---

## Documentation

### When to Update Documentation

**Update documentation if you:**
- Add new features
- Change existing behavior
- Add configuration options
- Fix important bugs
- Change API endpoints

### Documentation Files

- **README.md** - Main documentation
- **QUICKSTART.md** - Quick start guide
- **DEPLOYMENT.md** - Deployment guide
- **CHANGELOG.md** - Version history
- **config.example.yaml** - Configuration example

---

## Questions?

- **General questions:** GitHub Discussions
- **Bug reports:** GitHub Issues
- **Feature requests:** GitHub Issues
- **Security issues:** Email maintainer (if contact provided)

---

## Recognition

Contributors will be listed in:
- README.md credits section
- CHANGELOG.md for their contributions

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## Thank You!

Every contribution helps make this project better for everyone. Whether it's:
- Reporting a bug
- Suggesting a feature
- Improving documentation
- Submitting code

**Your contribution is valued!** 🙏

---

**Happy Contributing! 🚀**
