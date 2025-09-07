# 📚 Documentation Maintenance Guide

**[🇺🇸 English](DOCUMENTATION_GUIDE.md) | [🇷🇺 Русский](DOCUMENTATION_GUIDE.ru.md)**

## 🌍 Bilingual Documentation Structure

This project maintains documentation in two languages:
- **English** (primary) - for international audience
- **Russian** - for Russian-speaking users

## 📋 File Naming Convention

| Type | English | Russian | Purpose |
|------|---------|---------|---------|
| Main README | `README.md` | `README.ru.md` | Primary documentation |
| Quick Start | `QUICK_START.md` | `QUICK_START.ru.md` | Getting started guide |
| Changelog | `CHANGELOG.en.md` | `CHANGELOG.md` | Version history |
| Other docs | `FILENAME.en.md` | `FILENAME.md` or `FILENAME.ru.md` | Additional documentation |

## ✏️ Updating Documentation

### When adding new content:

1. **Update English version first** (primary language)
2. **Translate to Russian** maintaining the same structure
3. **Add language switcher** at the top of each file:
   ```markdown
   **[🇺🇸 English](FILENAME.md) | [🇷🇺 Русский](FILENAME.ru.md)**
   ```
4. **Update documentation index** files

### Language switcher template:
```markdown
**[🇺🇸 English](FILENAME.md) | [🇷🇺 Русский](FILENAME.ru.md)**
```

## 📂 Documentation Structure

```
📚 Documentation Files/
├── 📄 README.md (English - primary)
├── 📄 README.ru.md (Russian)
├── 🚀 QUICK_START.md (English)
├── 🚀 QUICK_START.ru.md (Russian)  
├── 📋 CHANGELOG.en.md (English)
├── 📋 CHANGELOG.md (Russian - exception)
├── 🔧 REFACTORING_SUMMARY.en.md (English)
├── 🔧 REFACTORING_SUMMARY.md (Russian)
├── 👨‍💻 CLAUDE.md (Technical - English only)
├── 📚 DOCUMENTATION_INDEX.md (English)
├── 📚 DOCUMENTATION_INDEX.ru.md (Russian)
├── 📖 DOCUMENTATION_GUIDE.md (This file - English)
└── 📖 DOCUMENTATION_GUIDE.ru.md (Russian version)
```

## 🔄 Maintenance Checklist

When updating any documentation:

- [ ] Update content in both languages
- [ ] Verify all internal links work
- [ ] Check language switcher links
- [ ] Update version information if needed
- [ ] Update documentation index if new files added
- [ ] Test all code examples
- [ ] Verify image links and references

## 🎯 Best Practices

1. **Keep structure identical** between language versions
2. **Use same heading hierarchy** in both versions
3. **Translate technical terms consistently**
4. **Keep code examples identical** in both languages
5. **Update both versions simultaneously** when possible
6. **Use emojis consistently** across languages
7. **Test all links** after updates

## 🚨 Common Issues

- **Broken links**: Always use relative paths
- **Missing translations**: Use translation tools but verify manually  
- **Inconsistent formatting**: Follow markdown standards
- **Outdated content**: Regular review and updates needed

## 📧 Translation Guidelines

- Technical terms: Keep in English when appropriate (e.g., "Docker", "Python")
- Commands: Keep identical across languages
- File paths: Keep identical across languages  
- URLs: Keep identical across languages
- Code: Keep identical across languages

---

*Follow this guide to maintain consistent bilingual documentation* 🌍