# Hunter

## Synopsis
This solution helps to lookup suspicious numbers, check if they're human or not, and report them accordingly.

## Context
As a Software Engineer and security enthusiast, this project was purely done out of research and to address the need to report a large number of scam calls.  The need for a truly free and open API was driven by the fact that this solution could potentially help others with their frustrations in the same struggle and as such fee-driven API's were not appropriate.  In fact, even though the open API used provides additional information, only the neccessary fields were extracted to respect PII and Privacy laws.  If reusing this solution for another, please follow the same ethical responsibilities and only extract the needed information.

## Assumptions
* There is a need to look up numbers.
* THere is a safe, free, and legal way to lookup numbers.
* There is a location where these numbers can be reported to.

## Requirements
* The solution will be able to scan through an input file.
* The solution will be able to lookup numbers at a trusted source.
* The solution will be able to report numbers to a trusted source.
* **The solution will and must respect PII and Privacy laws.**

## Implementation Details
The solution is driven by two main functions, wrapped in a helper class.

### extract_owner_info
This function uses a third-party service, which is offered free for basic information.  However, even with the basic information, a significant amount of PII details are provided, so as such, we only extract information related to the carier provider and if the number is associated to a VOIP service.
 
### report_number
This function simply report the number to a central database to inform them that this number should be flagged and blocked.

### Flags
|Flag                         | Description                                                                             |
|--|--|
|-f                           | Full path to a flat-file list of numbers.                                               |
|--numbers                    | Comma-separated list of numbers to scan and report.                                     |

## Examples
```bash
# Input file
python3 $HUNTER_BASE/hunter.py -f suspect_numbers.txt

# Command-Line
python3 $HUNTER_BASE/hunter.py --numbers 1234567890,0987654321
```

## References
* [ReversePhoneLookup](https://www.reversephonelookup.com/)
* [Federal Trade Commission](https://www.donotcall.gov/)

