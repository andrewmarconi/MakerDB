# Security Policy

## Supported Versions

We take security seriously and aim to provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < 1.0   | :x:                |

**Note:** As MakerDB is currently in active development (pre-1.0), we recommend always using the latest version from the `main` branch.

## Reporting a Vulnerability

We appreciate your efforts to responsibly disclose security vulnerabilities. Please follow these guidelines:

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **GitHub Security Advisories** (Preferred): Navigate to the [Security tab](https://github.com/andrewmarconi/MakerDB/security/advisories) and click "Report a vulnerability"
2. **Email**: Contact the project maintainers directly (check the repository for current maintainer contact information)

### What to Include

Please include the following information in your report:

- Type of vulnerability (e.g., SQL injection, XSS, authentication bypass)
- Full path(s) of affected source file(s)
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: We will acknowledge receipt of your vulnerability report within 3 business days
- **Status Updates**: We will provide regular updates on our progress at least every 7 days
- **Resolution**: We aim to resolve critical vulnerabilities within 30 days of initial report

### What to Expect

- We will work with you to understand and validate the vulnerability
- Once confirmed, we will develop and test a fix
- We will publicly disclose the vulnerability after a fix is available
- We will credit you in the security advisory (unless you prefer to remain anonymous)

## Security Update Policy

When a security vulnerability is fixed:

1. A security advisory will be published on GitHub
2. The fix will be released in a new version
3. Release notes will include details about the vulnerability and remediation steps
4. Users will be encouraged to update via repository notifications

## Scope

### In Scope

The following are within scope for security vulnerability reports:

- Backend API vulnerabilities (FastAPI/Django)
- Authentication and authorization bypass
- SQL injection, XSS, CSRF
- Data exposure or leakage
- Dependency vulnerabilities with exploitable impact
- Docker configuration issues leading to security risks

### Out of Scope

The following are generally not accepted:

- Vulnerabilities in third-party dependencies without proof of exploitability in MakerDB
- Social engineering attacks
- Physical security issues
- Denial of Service (DoS) attacks
- Issues in development/test configurations (not affecting production deployments)
- Vulnerabilities requiring unlikely user interaction

## Security Best Practices for Deployment

As a self-hosted application, security also depends on proper deployment. We recommend:

- Keep all dependencies up to date (use Dependabot alerts)
- Use strong, unique passwords for database and Django `SECRET_KEY`
- Enable HTTPS/TLS for all production deployments
- Regularly backup your database
- Run PostgreSQL and the application with minimal required privileges
- Keep Docker images up to date
- Review and monitor application logs regularly

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Questions?

If you have questions about this security policy, please open a GitHub discussion or contact the maintainers.
