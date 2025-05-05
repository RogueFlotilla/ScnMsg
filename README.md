# ScnMsg
## Introduction
The ScnMsg email client is a simple email client created using Python and some HTML with the goal to detect, reduce, and hopefully prevent malware execution, scams, and phishing attempts on the technology illiterate, cyber-unaware, and especially the elderly population that can be easily manipulated. The goal is to integrate features that will check emails against existing tools, such as Virus Total, and use AI to assess contents to provide a scoring mechanism to alert a user to potential risks through use of Groq API calls. Complex features seen in other email clients such as automatic replies, folder sorting, and advanced filtering rules will intentionally be left out since the target users for this software would likely not be the group to leverage those features and may make its use more complicated for the anticipated user.

## Explanation and Details
Coming soon to a README near you.

## Setup and Libraries
Coming soon to a README near you.

## Screenshots and Code Explanation
Coming soon to a README near you.

## Screenshots and Code Explanation
This section displays tables containing screenshots of key secitons of code code with descriptions of the functionality being performed for each package (file) of the program.

### HTML Report Template (./HTML/report.html)
| Code Image *(click to enlarge)* | Description |
|-------------------------------|-------------|
| ![Screenshot of HTML coloring blocks](./readme_images/html_coloring.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | Some of the class attributes are formatting blocks that define coloring for severity levels: `.negative` (no flagged alerts), `.neutral` (potentially noteworthy but not malicious), `.positive` (likely malicious), `.informational` (general awareness), and `.unknown` (ex. couldn't be processed due to error or failure). The severity levels are passed to placeholders as variables when creating the report allowing the blocks colors to be defined based on the analysis results. <br> <br> the class attribures are applied dynamically within the code to allow different coloring based on the results of the analysis, such as a file returned by Virus Total as likely being malware showing as red, or a potential spam email showing as yellow (not likely malicious, but might want to be ignored). |
| ![Screenshot of HTML code for top sections of report](./readme_images/html_top_report.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | This section of the HTML report template defines the structure for the top of the email analysis report. It displays the header of the report, email details such as sender, subject, and the received date, and the AI-generated analysis for the email body contents. Template placeholders can be seen here where the Jinja2 engine is creating the report by filling in variable placeholders such as {{ sender }} or {{ category_reasoning }} |
| ![Screenshot of the HTML code block for creating variables numbers of file blocks](./readme_images/html_file_blocks.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | A '{ % for % } statement is used to generate separate sections for each file attachment in the email. For example, an email with one attachment will have only one block, while an email with six attachments will have six blocks, each with their cooresponding information from the analysis by Virus Total. An '{ % if % }' statement is used to dynamically generate a link to the associated Virus Total page for the file that was analyzed, or if there are no attachments an information block is created using anto let the report reader know nothing was attached. |
| ![Screenshot of the HTML footer code and a date script](./readme_images/html_file_blocks.png)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | The footer of the report contains copyright and license details. There is also a script that contains code generating a date for the time the report was created to be used in the header. Both of these detail not only create a professional looking report, but provide important information to the reader. |

## Future Improvements
- [ ] Implement sending of emails