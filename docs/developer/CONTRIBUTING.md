# Contributing to MakerDB

Thank you for your interest in contributing to MakerDB! This document provides guidelines and workflows for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Making Changes](#making-changes)
- [Testing Guidelines](#testing-guidelines)
- [Code Review Process](#code-review-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Documentation](#documentation)
- [Communication](#communication)

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive criticism
- Prioritize the community's best interests
- Show empathy towards other community members

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- **Git** - Version control
- **Python 3.12+** - For backend development
- **Node.js 18+** - For frontend development
- **Docker** - For PostgreSQL database
- **uv** - Python package manager
- **A GitHub account** - For submitting pull requests

### Initial Setup

1. **Fork the repository**

   Click the "Fork" button on the GitHub repository page.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR_USERNAME/MakerDB.git
   cd MakerDB
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/andrewmarconi/MakerDB.git
   ```

4. **Set up the development environment**

   Follow the setup instructions in the [README](../../README.md):

   ```bash
   # Backend
   uv sync
   docker compose up -d
   uv run python backend/manage.py migrate

   # Frontend
   cd frontend
   npm install
   ```

5. **Verify your setup**

   ```bash
   # Backend tests
   uv run pytest

   # Frontend tests
   cd frontend
   npm test
   ```

## Development Workflow

### Branch Naming Convention

Use descriptive branch names with the following prefixes:

- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Adding or updating tests
- `chore/` - Maintenance tasks

Examples:
- `feat/add-inventory-search`
- `fix/part-deletion-bug`
- `docs/update-api-reference`
- `refactor/optimize-database-queries`

### Making Changes

1. **Create a new branch**

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**

   Follow the coding conventions for [Backend](BACKEND.md) or [Frontend](FRONTEND.md).

3. **Test your changes**

   ```bash
   # Backend
   uv run pytest
   uv run ruff check backend
   uv run ruff format backend

   # Frontend
   cd frontend
   npm test
   npm run dev  # Manual testing
   ```

4. **Commit your changes**

   Write clear, descriptive commit messages following this format:

   ```
   type: Brief description (50 chars or less)

   More detailed explanation if needed. Wrap at 72 characters.
   Explain the problem this commit solves and why you chose
   this particular solution.

   Closes #123  (if applicable)
   ```

   Commit types:
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation changes
   - `refactor`: Code refactoring
   - `test`: Adding tests
   - `chore`: Maintenance
   - `style`: Formatting changes

   Example:
   ```
   feat: Add inventory search with filters

   Implement search functionality for the inventory page with
   filters for part name, category, and stock status. Includes
   pagination for large result sets.

   Closes #45
   ```

5. **Keep your branch up to date**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

6. **Push your changes**

   ```bash
   git push origin feat/your-feature-name
   ```

## Pull Request Process

### Before Submitting

Ensure your PR:

- [ ] Passes all tests (`uv run pytest` and `npm test`)
- [ ] Follows code style guidelines (run `ruff format` and `ruff check`)
- [ ] Includes tests for new functionality
- [ ] Updates documentation if needed
- [ ] Has a clear, descriptive title
- [ ] References related issues

### Creating a Pull Request

1. **Push your branch** to your fork on GitHub

2. **Create the PR** on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

3. **PR Description Template**

   ```markdown
   ## Description
   Brief description of what this PR does.

   ## Type of Change
   - [ ] Bug fix (non-breaking change which fixes an issue)
   - [ ] New feature (non-breaking change which adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update

   ## Related Issues
   Closes #XX
   Related to #YY

   ## Changes Made
   - List the specific changes
   - One per line
   - Be descriptive

   ## Testing
   How has this been tested?
   - [ ] Unit tests
   - [ ] Integration tests
   - [ ] Manual testing

   ## Screenshots (if applicable)
   Add screenshots to help explain your changes.

   ## Checklist
   - [ ] My code follows the project's style guidelines
   - [ ] I have performed a self-review of my code
   - [ ] I have commented my code, particularly in hard-to-understand areas
   - [ ] I have made corresponding changes to the documentation
   - [ ] My changes generate no new warnings
   - [ ] I have added tests that prove my fix is effective or that my feature works
   - [ ] New and existing unit tests pass locally with my changes
   ```

### Code Review

- Be patient - reviews may take a few days
- Respond to feedback promptly and professionally
- Make requested changes in new commits
- Once approved, a maintainer will merge your PR

### After Your PR is Merged

1. **Delete your branch**

   ```bash
   git branch -d feat/your-feature-name
   git push origin --delete feat/your-feature-name
   ```

2. **Update your local main**

   ```bash
   git checkout main
   git pull upstream main
   ```

## Testing Guidelines

### Backend Testing

All backend changes should include appropriate tests:

```python
# backend/tests/test_feature.py
import pytest
from parts.models import Part

@pytest.mark.django_db
class TestNewFeature:
    def test_feature_works(self):
        # Arrange
        part = Part.objects.create(name="Test Part")

        # Act
        result = part.some_method()

        # Assert
        assert result == expected_value
```

**Test Coverage Requirements:**
- New features must have tests
- Bug fixes should include regression tests
- Aim for >80% code coverage

### Frontend Testing

Frontend changes should include component and unit tests:

```typescript
// app/components/NewComponent.test.ts
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import NewComponent from './NewComponent.vue'

describe('NewComponent', () => {
  it('renders correctly', () => {
    const wrapper = mount(NewComponent, {
      props: { title: 'Test' }
    })
    expect(wrapper.text()).toContain('Test')
  })
})
```

### Running Tests Locally

Always run tests before submitting a PR:

```bash
# Backend
uv run pytest -v

# Frontend
cd frontend
npm test

# Run both
uv run pytest && cd frontend && npm test
```

## Reporting Bugs

### Before Submitting a Bug Report

- Check the [existing issues](../../issues) to avoid duplicates
- Test with the latest version of main
- Collect information about your environment

### Bug Report Template

Create an issue with the following information:

```markdown
## Bug Description
A clear and concise description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Screenshots
If applicable, add screenshots.

## Environment
- OS: [e.g., macOS 13.0]
- Browser: [e.g., Chrome 120]
- Python version: [e.g., 3.12.1]
- Node version: [e.g., 20.10.0]

## Additional Context
Any other context about the problem.

## Possible Solution
If you have an idea how to fix it.
```

## Suggesting Features

### Feature Request Template

```markdown
## Feature Description
A clear and concise description of the feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How do you envision this feature working?

## Alternatives Considered
What other solutions have you considered?

## Additional Context
Any mockups, examples, or references.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### Feature Discussion

- Features should be discussed in issues before implementation
- Large features may require a design document
- Maintainers will provide feedback and direction

## Documentation

### Documentation Changes

Documentation improvements are always welcome:

- Fix typos and improve clarity
- Add examples and tutorials
- Update outdated information
- Translate documentation

### Documentation Structure

- **README.md** - Project overview and quick start
- **docs/developer/** - Developer documentation
  - `BACKEND.md` - Backend development guide
  - `FRONTEND.md` - Frontend development guide
  - `CONTRIBUTING.md` - This file
- **CLAUDE.md** - AI assistant development guide
- **Code comments** - Complex logic and APIs

### Writing Good Documentation

- Use clear, concise language
- Include code examples
- Provide context for why, not just what
- Keep it up to date with code changes
- Use proper markdown formatting

## Communication

### Getting Help

- **GitHub Issues** - Bug reports and feature requests
- **GitHub Discussions** - Questions and general discussion (if enabled)
- **Pull Request Comments** - Code-specific discussions

### Best Practices

- Search before asking - your question may already be answered
- Be specific and provide context
- Share error messages and logs
- Be patient and respectful
- Help others when you can

## Development Best Practices

### Code Quality

- **Write clean code** - Follow the project's style guides
- **Keep it simple** - Avoid over-engineering
- **DRY principle** - Don't repeat yourself
- **Single responsibility** - Functions/components should do one thing well
- **Meaningful names** - Use descriptive variable and function names

### Performance

- **Avoid N+1 queries** - Use `select_related()` and `prefetch_related()`
- **Optimize database queries** - Add indexes where needed
- **Lazy loading** - Load data when needed
- **Caching** - Cache expensive operations when appropriate

### Security

- **Never commit secrets** - No API keys, passwords, or tokens
- **Validate input** - Always validate and sanitize user input
- **Use parameterized queries** - Prevent SQL injection
- **Follow Django/FastAPI security best practices**

### Accessibility

- **Semantic HTML** - Use appropriate HTML elements
- **ARIA labels** - Add labels for screen readers
- **Keyboard navigation** - Ensure all features work with keyboard
- **Color contrast** - Maintain sufficient contrast ratios

## Version Control Best Practices

### Commit Guidelines

- Make small, focused commits
- Write meaningful commit messages
- Commit working code
- Don't commit commented-out code
- Don't commit debugging statements

### Branch Management

- Keep branches short-lived
- Merge or close stale branches
- Rebase on main frequently
- Delete merged branches

## Project Structure Guidelines

### Backend

- Place models in `models.py`
- Place API endpoints in `router.py`
- Place Pydantic schemas in `schemas.py`
- Follow existing app structure

### Frontend

- Components in `app/components/`
- Pages in `app/pages/` (file-based routing)
- Composables in `app/composables/`
- Utils in `app/utils/`

## Release Process

(This section will be updated as the release process is formalized)

### Semantic Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

## Recognition

Contributors will be recognized in:

- Git commit history
- Release notes
- Project contributors page (when available)

Thank you for contributing to MakerDB! 🎉

---

**Questions?** Feel free to ask in issues or pull request comments.
