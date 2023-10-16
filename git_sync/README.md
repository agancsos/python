# GitSync

## Synopsis
GitSync is a lightweight  utility that helps sync multiple Git repositories distributed on several remote systems.

## Assumptions
* There is a need to sync multiple repostiroes across multiple systems.
* Alternative solutions are limited or too robust for the needs.
* Python 3 is installed.
* The git CLI is installed on the remote systems.
* YAML and Parmiko Python dependencies are installed.
* A base git directory exists in the target user's profile.
* Usernames and passwords will be provided in an inventory file.
* Passwords will be base64 encoded.
* Inventory files may or may not be YAML or JSON.

## Requirements
* The utility will be able to read YAML and JSON files.
* The utility will be able to telnet to remote hosts.
* The utility will be able to SSH connect to remote hosts.
* The utility will be able to fetch the base git directory.
* The utility will be able to sync repositories in the base git directory.

## Implementation details
The utility is implemented as a Python CLI that takes in the required fields via command-line parameters.  Upon invoking the utility, we ensure that the inventory file exists and is valid.  Then we load in the inventory details then start to enumerate through the provided list of hosts.  We first test if the host is reachable by trying to connect via telnet (socket) and if successful, we continued to build out the SSH client.  Once we have the SSH client, we first lookup the base 'git' directory and then list the available repositories under the base directory.  We then try to pull the repository and close the SSH client.

### Flags
| Flag           | Description                                                       |
|--|--|
| -f             | Full path to the inventory file (YAML or JSON).                   |
| -h             | Comma-separated list of hosts (must exist in the inventory file). |
| --ttl          | Timeout for the socket test as well as the SSH client.            |

### YAML Inventory
```yaml
---
hosts:
  "192.168.1.123":
    "username": ""
    "pat": "base64(<username>:<password>)"
```

### JSON Inventory
```json
{
	"hosts": {
		"192.168.1.123": {
			"username": "",
			"pat": "base64(<username>:<password>)"
		}
	}
}
```

## References

