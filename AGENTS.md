# Agent Guidelines for leo-obsidian

This is an Obsidian vault repository containing Agent Skills, notes, and utility scripts.

## Repository Structure

```
00 Inbox/        - Capture zone for new ideas
01 Base/         - Base files for knowledge mapping
02 Map/          - MOC (Map of Content) files
03 Source/       - Reference materials and articles
04 Person/       - Person profiles
05 Journal/      - Daily notes
06 Note/         - Permanent notes
10 Attachment/   - Attached media files
11 Template/     - Obsidian templates
12 AI Chat/      - AI conversation logs
13 Skills/       - Agent Skills (SKILL.md files + scripts)
14 Actions/      - Action-specific skills
.obsidian/       - Obsidian plugins, themes, config
```

### File Naming
- Markdown files: `Title Case with Spaces.md` or `kebab-case.md`
- SKILL directories: `kebab-case-name/`
- Scripts: `snake_case.py` or `kebab-case.sh`

### Notes Structure
- **Inbox**: Quick captures, no formatting needed
- **Base**: Base files with `.base` extension for knowledge mapping
- **Journal**: Date format `YYYY-MM-DD.md`
- **Notes**: Descriptive titles, can use Chinese

### Actions
Each action skill should include:
1. Clear role definition
2. Task objectives
3. Visual guidelines (if applicable)
4. Technical constraints
5. Output format specifications

## Testing
No formal test framework. Manual testing:
- Run scripts with sample inputs
- Verify output format matches SKILL.md specifications
- Check error handling edge cases
