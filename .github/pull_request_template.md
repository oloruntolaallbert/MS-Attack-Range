## Description

Please provide a clear and concise description of your changes.

## Type of Change

Please delete options that are not relevant and check the box that applies:

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📚 Documentation update
- [ ] 🔧 Infrastructure/build changes
- [ ] 🎯 New attack technique/simulation
- [ ] 🛡️ Security improvement

## Related Issues

Fixes # (issue number)
Related to # (issue number)

## Changes Made

Please describe the changes you've made:

### Infrastructure Changes
- [ ] Terraform configuration updates
- [ ] Azure resource modifications
- [ ] Network configuration changes

### Attack Simulations
- [ ] New MITRE ATT&CK technique added
- [ ] Modified existing attack playbook
- [ ] Updated Atomic Red Team tests

### Detection Rules
- [ ] New Microsoft Sentinel analytics rules
- [ ] Updated existing detection logic
- [ ] Modified data collection rules

### Documentation
- [ ] README updates
- [ ] Code comments added/improved
- [ ] New troubleshooting guides

## Testing Performed

Please describe the testing you've performed:

### Infrastructure Testing
- [ ] Terraform plan/apply successful
- [ ] Resources deploy correctly
- [ ] Cleanup works properly
- [ ] Network connectivity verified

### Attack Simulation Testing
- [ ] Attack techniques execute successfully
- [ ] Expected logs are generated
- [ ] Microsoft Sentinel detections trigger
- [ ] No unintended side effects

### Security Testing
- [ ] No credentials exposed
- [ ] Proper isolation maintained
- [ ] Security controls working as expected

## Test Environment

- **Azure Region**: 
- **Subscription Type**: 
- **Operating System**: 
- **Tool Versions**:
  - Terraform: 
  - Ansible: 
  - Python: 

## Checklist

Please check all boxes that apply:

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation

### Security
- [ ] No sensitive information (credentials, keys, etc.) is included
- [ ] Changes maintain proper security isolation
- [ ] New attack techniques are properly documented
- [ ] Security implications are clearly stated

### Testing
- [ ] My changes generate the expected security events
- [ ] I have tested the cleanup procedures
- [ ] New features have been tested thoroughly
- [ ] Existing functionality is not broken

### Documentation
- [ ] I have updated relevant documentation
- [ ] MITRE ATT&CK technique mappings are accurate
- [ ] Installation/usage instructions are current

## Breaking Changes

If this is a breaking change, please describe:
- What functionality is affected
- Migration steps for users
- Backwards compatibility considerations

## Screenshots/Logs

If applicable, add screenshots or relevant log excerpts to help explain your changes:

## Additional Notes

Any additional information or context about the changes:

## Security Considerations

Please describe any security implications of your changes:

- [ ] Changes maintain lab environment isolation
- [ ] No production security risks introduced
- [ ] Proper warnings added for new attack techniques

---

**Note**: By submitting this pull request, I confirm that:
- This contribution is made under the project's open source license
- I have the right to make this contribution
- I understand this project creates intentionally vulnerable environments for testing purposes only
