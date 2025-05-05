# ScnMsg

## HTML Report Template (./HTML/report.html)
| Code Image *(click to enlarge)* | Description |
|-------------------------------|-------------|
| ![Screenshot](./readme_images/html_coloring.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | The HTML report contains several formatting blocks that define coloring for severity levels: `.negative` (no flagged alerts), `.neutral` (potentially noteworthy but not malicious), `.positive` (likely malicious), `.informational` (general awareness), and `.unknown` (ex. couldn't be processed due to error or failure). |
| ![Screenshot](./readme_images/html_top_report.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | This section of the HTML report template defines the structure for the top of the email analysis report. It displays the header of the report, email details such as sender, subject, and the received date, and the AI-generated analysis for the email body contents. Template placeholders can be seen here where the Jinja2 engine is creating the report by filling in variable placeholders such as {{ sender }} or {{ category_reasoning }} |
| ![Screenshot](./readme_images/html_file_blocks.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | The template uses a for block in order to generate a separate section for each file attachment included in the email being analyzed. For example, an email with one attachment will have only one block, while an email with six attachments would have six blocks, each with their cooresponding informatino from the analysis by Virus Total. If there are no attachments, and information block is created using an if statement to let the report reader know. |


## Work to be completed
- [ ] Implement sending of emails