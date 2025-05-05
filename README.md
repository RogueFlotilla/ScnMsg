# ScnMsg

## HTML Report Template (./HTML/report.html)
![Screenshot of the HTML color definitions for categories of detections.](./readme_images/html_coloring.png)
The HTML report contains several formatting blocks that define coloring for level or everety of the block being displayed. '.negative' is for items with no flagged alerts. 'neutral' is for alerts that may be flagged for consideration, but not necesarily dangerous or malicious. '.positive' ones have likel malicious intent behind the item, such as a file scanning positive for malware. '.informational' items are usually not of importance but displayed just for the readers awareness, such as an informational alert that there were no file attachments on the email under review. '.unknown' us usually assigned to items that could not be processed, either due to an error in the implementation of code, a down API, or some other issue.

## HTML Report Template (./HTML/report.html)

| The HTML report contains several formatting blocks that define coloring for severity levels: `.negative` (no flagged alerts), `.neutral` (potentially noteworthy but not malicious), `.positive` (likely malicious), `.informational` (general awareness), and `.unknown` (couldn't be processed due to error or failure). | ![Screenshot](./readme_images/html_coloring.png) |
|--------------------------------------------------|----------------------------------------------------------------------------------------------------|


## Work to be completed
- [ ] Implement sending of emails