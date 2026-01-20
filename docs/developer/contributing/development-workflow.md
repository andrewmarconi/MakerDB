# Development Workflow

## Branch Naming Convention

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

## Making Changes

1. **Create a new branch**

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. **Make your changes**

   Follow the coding conventions for [Backend](../backend/coding-conventions.md) or [Frontend](../frontend/coding-conventions.md).

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
