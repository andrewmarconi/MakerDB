# Pull Request Process

## Before Submitting

Ensure your PR:

- [ ] Passes all tests (`uv run pytest` and `npm test`)
- [ ] Follows code style guidelines (run `ruff format` and `ruff check`)
- [ ] Includes tests for new functionality
- [ ] Updates documentation if needed
- [ ] Has a clear, descriptive title
- [ ] References related issues

## Creating a Pull Request

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

## Code Review

- Be patient - reviews may take a few days
- Respond to feedback promptly and professionally
- Make requested changes in new commits
- Once approved, a maintainer will merge your PR

## After Your PR is Merged

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
