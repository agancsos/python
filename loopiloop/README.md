# LoopiLoop

## Synopsis
LoopiLoop is a failure tool to test how teams react to a cyber event where sudoe is disabled and possible alerts are being raised.

## Assumptions
* A malicious actor has console access to the target system.
* The root password is changed.
* Sudoers access is removed.
* A crash occurs right after boot.
* A restart occurs for each crash.
* Alerts may or may not be raised.
* The tool will run after gaining root access.
* The tool will be used for training, educational, and testing purposes ONLY.
* The tool will not be able to recovery the original root password due to hashing.

## Requirements
* The tool will reset the root password.
* The tool will disable all non-root sudoers.
* The tool will configure a post-boot crash.
* The tool will configure a restart on a crash.

## Implementation Details
Implementation of this exploit-antidote security tool is done via a Python script that's designed to be run as root.  Upon invocation, we first ensure that the user running the script is indeed root.  We then extract core parameters and invoke the target payload.  

When the exploit is ran, depending if debug is disabled, will change the root password using a POpen process and the standard passwd command.  We then move forward in disabling (comment-out) all non-root entries in the sudoers file if it exists.  Next, we configure a restart on kernel panic if it's not enabled already and then create/enable the service that causes the crash.

When the antitode is ran, depending if debug is disabled, will attempt to re-enable non-root sudoers entries.  We then attempt to disable and remove the service.

In both cases, we also attempt to clear the command history to reduce the paper trail.

### Flags
| Flag                  | Description                                                           |
|--|--|
| --debug               | Prevent any system changes.                                           |
| --op                  | Determines which phase will be invoked. (exploit or antidote).        | 

## References
* https://unix.stackexchange.com/questions/66197/how-to-cause-kernel-panic-with-a-single-command

