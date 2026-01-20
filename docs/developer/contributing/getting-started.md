# Getting Started

## Prerequisites

Before contributing, ensure you have:

- **Git** - Version control
- **Python 3.12+** - For backend development
- **Node.js 18+** - For frontend development
- **Docker** - For PostgreSQL database
- **uv** - Python package manager
- **A GitHub account** - For submitting pull requests

## Initial Setup

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

   Follow the setup instructions in the [README](../../../README.md):

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
