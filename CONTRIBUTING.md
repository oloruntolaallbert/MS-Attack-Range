# Contributing to MS-Attack-Range

Thank you for your interest in contributing to the Microsoft Sentinel Attack Range project! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue templates** provided
3. **Provide detailed information** including:
   - Environment details (OS, Azure region, etc.)
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages or logs

### Suggesting Features

1. **Open a feature request** using the provided template
2. **Describe the use case** and why it would be valuable
3. **Consider security implications** for any new attack techniques

### Code Contributions

#### Prerequisites

- Python 3.7+
- Terraform 1.0+
- Ansible 2.9+
- Azure CLI
- Git

#### Getting Started

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ms-attack-range.git
   cd ms-attack-range
   ```

3. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up your development environment**:
   ```bash
   ./Setup.sh
   source attack_range_env/bin/activate
   ```

#### Making Changes

1. **Follow the existing code style**
2. **Test your changes thoroughly**
3. **Update documentation** if needed
4. **Add appropriate comments** for complex logic

#### Submitting Changes

1. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

2. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Testing performed

### Adding New Attack Techniques

When adding new MITRE ATT&CK techniques:

1. **Follow the existing playbook structure**
2. **Add proper MITRE technique mappings**
3. **Include appropriate logging and detection artifacts**
4. **Test on both Windows and Linux when applicable**
5. **Update the README with new technique information**

### Security Guidelines

⚠️ **IMPORTANT SECURITY CONSIDERATIONS**

- **Never commit real credentials** or sensitive information
- **Test only in isolated environments**
- **Document security implications** of new features
- **Follow responsible disclosure** for any vulnerabilities found

### Code Review Process

1. All contributions require review by project maintainers
2. We may request changes or improvements
3. Once approved, we'll merge your contribution
4. Your contribution will be acknowledged in the project

### Development Environment

#### Testing Infrastructure Changes

1. **Use a test Azure subscription**
2. **Clean up resources** after testing
3. **Document any manual steps** required

#### Testing Attack Simulations

1. **Ensure attacks generate expected logs**
2. **Verify Microsoft Sentinel detection rules trigger**
3. **Test cleanup procedures**

### Documentation

- Update relevant documentation for any changes
- Use clear, concise language
- Include examples where helpful
- Keep the README.md up to date

### Community

- Be respectful and professional
- Help others in issues and discussions
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md)

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Review existing issues and pull requests
- Check the project documentation

Thank you for helping make this project better! 🛡️

---

**Note**: This project creates intentionally vulnerable environments for security testing. Always follow security best practices and use only in isolated lab environments.
