# Continuity System for Project Development

This document outlines our system for maintaining continuity across development sessions.

## Session End Protocol

At the end of each development session, we'll create a continuity note with the following structure:

```
--- CONTINUITY NOTE ---
Current Status: [Brief description of what was just completed]
Branch: [Current git branch]
Last File Modified: [Path to last file we worked on]

Next Files Needed:
- [File path 1]
- [File path 2]
- [File path 3]

Next Task: [Clear description of the next task to implement]

Additional Context: [Any other relevant information]
```

## Session Start Protocol

When starting a new development session:

1. Share the files listed in the previous continuity note
2. Mention "Continuing from previous session" to provide context
3. Reference the current branch and last task completed

## Project Structure Reference

For quick reference, our project follows this structure:

```
fitness_food_app/
├── app.py                  # Main application file
├── auth/                   # Authentication module
├── nutrition/              # Nutrition tracking module
├── recipes/                # Recipe management module
├── social/                 # Social features module
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── utils/                  # Shared utilities
├── .github/workflows/      # GitHub Actions workflows
└── [future: frontend/]     # Frontend application
```

## Active Tasks Tracking

Current active tasks:
1. ✅ GitHub Actions setup for CI/CD
2. 🔄 Frontend integration planning
3. ⏳ User onboarding optimization
4. ⏳ Analytics and reporting dashboards

## Git Workflow

We're using the following Git workflow:
- `main` - Stable production code
- Feature branches for new development (e.g., `feature/github-actions`)

## Updating Status

After completing a significant task:
1. Update PROJECT_STATUS.md
2. Create a commit with a descriptive message
3. Note the commit in the continuity document