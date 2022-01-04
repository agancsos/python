# Indeed Scraper

## Synopsis
The purpose of these tool is simply to be able to batch search the Indeed database.

## Requirements
* The tool will allow searching via keywords.
* The tool will allow searching via job location.
* The tool will allow searching via job experience.
* The tool will allow searching via remote options.
* The tool will return all results as a single set.
* The tool will offer an option to search only for companies.

## Assumptions
* Indeed may or may not have a REST API.
* Indeed content can be scraped withing standard DOM elements.
* Search results may or may not having multiple pages.

## Implementation Details
The tools is implemented using 3 core packages as well as 2 custom classes.

### Packages
Other than a few minor packages, the main ones are as follows.

#### requests_html
Used to make the actual web requests.

#### scrapy
Used for the initial XML extraction of the DOM elements.

#### xml.etree.ElementTree 
Used for the remaining parsing, specifically for the IndeedEntry class.

### Classes
#### IndeedEntry
A class simply used to extract usable information from the DOM objects.

#### IndeedScraper
Main class used to invoke the REST requests and cache the entries.  This class leverages the threading package so that none of the operations are blocking.  The class also checks for unique company names if specified on the command-line.

One thing to mention while implementing this class is that during manual testing, if limit is set to -1, the Indeed system sends out alerts, so don't try to remove the limit by setting this parameter to -1.  Remember, the purpose is to help developers batch out their job search, not to break the Indeed servers.

### Flags
|Flag             | Description|
|--|--|
| -b      | Base endpoint if need to override.                                          |
| -p      | Dorking files base path. Can be a single file.                              |
| -c      | Only collect unique companies.                                              |
| -l      | Batch size. Default=50; -1 not allowed; set to 9999 to ensure full results. |

### Example
#### Dork
```json
{"keywords":"software engineer", "location":"remote", "experience":"entry_level"}
```

#### Command
```bash
python3 tools/indeed_crawler/indeed_crawler.py -p dorks/indeed/
```

## Final thoughts
* Compared to other job searches, Indeed is more developer sentric in that it doesn't require a login.  This allows job seekers to make their hunt more efficient by being able to build out scripts like this one, please don't change it.
* I'm curious why the REST API seems complex, in that it uses the same flows as Google does, while scraping the DOM elements seem to be more efficient.  If it's the money-maker or offers additional functionality, I get it, but just a thought.
* If on the far chance that this tools helps someone land their dream job, please post your success story.

## References
* https://developer.indeed.com/
* https://docs.scrapy.org/en/latest/topics/selectors.html

