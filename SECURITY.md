
# Security Policy

## Purpose

The Microsoft Sentinel Attack Range is designed to create intentionally vulnerable environments for security testing, detection development, and security training. This document outlines security considerations and responsible use guidelines.

## ⚠️ Important Security Warnings

### Intentionally Vulnerable Environment

This project:
- **Creates vulnerable systems by design**
- **Disables security controls** (Windows Defender, etc.)
- **Simulates real attack techniques**
- **Generates malicious-looking network traffic**

### Safe Usage Guidelines

#### ✅ DO:
- **Use only in isolated lab environments**
- **Deploy in dedicated Azure subscriptions**
- **Ensure proper network isolation**
- **Clean up resources after testing**
- **Follow your organization's security policies**
- **Use for legitimate security training/testing only**

#### ❌ DON'T:
- **Connect to production networks**
- **Use production credentials**
- **Deploy in shared environments**
- **Leave resources running unnecessarily**
- **Use for unauthorized testing**
- **Expose attack range to public internet unnecessarily**

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project (not the intentionally vulnerable lab environments), please report it responsibly:

### For Project Security Issues

1. **Do not open public issues** for security vulnerabilities
2. **Email the maintainer** directly at: `[Your Contact Email]`
3. **Include detailed information**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fixes (if any)

### What to Report

Please report:
- **Authentication bypasses** in the deployment scripts
- **Credential exposure** in configuration files
- **Unintended data exposure** in logs or outputs
- **Code injection vulnerabilities** in scripts
- **Insecure defaults** that could affect real environments

### What NOT to Report

Do not report:
- **Intentional vulnerabilities** in the lab VMs
- **Disabled security controls** (this is by design)
- **Attack simulation artifacts** (these are expected)
- **Network scanning** results from the attack tools

## Response Timeline

- **Initial response**: Within 48 hours
- **Detailed assessment**: Within 1 week
- **Fix development**: Depends on severity and complexity
- **Public disclosure**: After fix is available and tested

## Security Best Practices for Users

### Azure Environment Security

1. **Use dedicated subscriptions** for attack range deployments
2. **Enable Azure Security Center** on your subscription
3. **Configure network security groups** appropriately
4. **Monitor costs** to prevent unexpected charges
5. **Set up resource locks** on critical resources

### Network Security

1. **Deploy in isolated VNets**
2. **Use appropriate IP allow-lists**
3. **Monitor network traffic** for unexpected patterns
4. **Implement network logging**
5. **Review NSG rules regularly**

### Credential Management

1. **Use strong, unique passwords**
2. **Store credentials securely**
3. **Rotate credentials regularly**
4. **Use Azure Key Vault** when possible
5. **Don't commit credentials** to version control

### Monitoring and Logging

1. **Enable Azure Monitor**
2. **Configure Microsoft Sentinel** properly
3. **Set up appropriate alerts**
4. **Review logs regularly**
5. **Understand normal vs suspicious activity**

## Compliance Considerations

### Legal Compliance

- **Ensure authorization** before testing
- **Follow local laws** and regulations
- **Respect terms of service** for cloud providers
- **Document your testing** appropriately

### Organizational Compliance

- **Get proper approvals** before deployment
- **Follow change management** processes
- **Coordinate with security teams**
- **Respect budget constraints**

## Emergency Procedures

### If Compromise is Suspected

1. **Immediately isolate** the affected resources
2. **Notify your security team**
3. **Document the incident**
4. **Preserve evidence** if required
5. **Follow your incident response** procedures

### Resource Cleanup

If you need to quickly destroy all resources:

```bash
# Emergency cleanup
python attack-range.py destroy

# Or via Terraform directly
terraform -chdir=terraform destroy -auto-approve
```

## Educational Use

This project is intended for:
- **Security education and training**
- **Detection rule development**
- **Security tool testing**
- **Research purposes**

## Disclaimer

The maintainers of this project:
- **Are not responsible** for misuse of this software
- **Provide no warranty** of any kind
- **Recommend consulting** with security professionals
- **Encourage responsible** use only

## Additional Resources

- [Azure Security Best Practices](https://docs.microsoft.com/en-us/azure/security/)
- [Microsoft Sentinel Documentation](https://docs.microsoft.com/en-us/azure/sentinel/)
- [MITRE ATT&CK Framework](https://attack.mitre.org/)

---

**Remember**: With great power comes great responsibility. Use this tool ethically and responsibly. 🛡️
