---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''

---

## Bug Description

A clear and concise description of what the bug is.

## Environment Information

**Operating System:**
- [ ] Windows 10/11
- [ ] macOS
- [ ] Linux (specify distribution): 

**Tool Versions:**
- Python: 
- Terraform: 
- Ansible: 
- Azure CLI: 

**Azure Environment:**
- Region: 
- Subscription Type: 
- Resource Group: 

## Steps to Reproduce

1. Go to '...'
2. Click on '....'
3. Run command '....'
4. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Error Messages

```
Paste any error messages here
```

## Log Files

Please attach or paste relevant log files:

### Terraform Logs
```
Paste terraform output here
```

### Ansible Logs
```
Paste ansible output here
```

### Python/Attack Range Logs
```
Paste python script output here
```

## Configuration Files

Please share relevant configuration (remove any sensitive information):

### terraform.tfvars (sanitized)
```hcl
# Remove sensitive values
prefix = "attack-range"
location = "uksouth"
# ... other non-sensitive config
```

### attack-range.yml (sanitized)
```yaml
# Remove sensitive values
range_name: azure-attack-range
location: uksouth
# ... other non-sensitive config
```

## Screenshots

If applicable, add screenshots to help explain your problem.

## Workaround

If you found a workaround, please describe it here.

## Impact

How severe is this issue?
- [ ] Critical - Cannot use the tool at all
- [ ] High - Major functionality broken
- [ ] Medium - Some features don't work
- [ ] Low - Minor inconvenience

## Additional Context

Add any other context about the problem here.

## Related Issues

Are there any related issues? Link them here.

## Checklist

- [ ] I have searched existing issues to ensure this is not a duplicate
- [ ] I have included all relevant error messages
- [ ] I have removed any sensitive information from logs/configs
- [ ] I have tested this in an isolated environment
- [ ] I am using the latest version of the project
