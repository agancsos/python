# GMail Scanner

## Overview 
GMailScanner is a small program that helsp scan GMAIL email messages for spam and mallicious emails.
 
## Context
 
## Assumptions
* User has a valid GMail account.
* User has Python 3.8+ installed.
* User has the requirements installed.
* User may or may not have multiple accounts.
* User may or may not have spam and/or malicious emails.
* User may or may not have multiple folders in their mailbox.
* User has a configuration file.
 
## Requirements
* The program will provide the user with an option for continuous scanning.
* The program will provide the user with an option for a one-time scan.
* The program will perform all operations in the back-end other than configuration.
* The program will be able to run on Windows 10+.
* The program will be able to run on macOS 10.15+.
* The program will be able to run on Linux (kernel 3.5+).
 
## Existing Solution
NA

## Proposed Solution
Small, open source, and lightwight Python-based application simply for scanning.
 
## Alternative Solutions
 
## Cross-Team Impact
NA
 
# Design
## Flags
|Flag|Description|
|--|--|
|-f     | Full path to a configuration file.|
|-o     | Output format for ad-hoc runs.|
|-u     | User file override.|
|--dubug| Debug mode, no changes to GMail.|
|-d     | Run as a service.|
|-t     | Override for interval in seconds.|
|--purge| Confirm auto-delete.|

## Output Formats
|Format|Notes|
|--|--|
|JSON | Pipe to a file if the output should be saved or the console shouldn't be bloated.|
|HTML | Pipe to a file if the output should be saved or the console shouldn't be bloated.|
|LIST | This is default.  Simply prints a list or messages with their level capture.|

## Configuration
{ 
	"userFile":"", 
	"credentialsFile":"",
	"warningKeywords":[], 
	"severeKeywords":[], 
	"debugMode":"1",
	"intervalSeconds":"5"
}

## References
* https://developers.google.com/gmail/api/quickstart/python
