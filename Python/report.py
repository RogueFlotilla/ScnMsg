import jinja2
# import os
# import datetime

def generate_report(email, category, category_reasoning, category_color, category_recommendation, attachment_results, filename):
  # Define data
  email_data = {
    'sender': email.from_,
    'subject': email.subject.encode('ascii', 'ignore').decode('ascii'),
    'received_date': email.date.strftime("%m/%d/%Y, %H:%M:%S"),
    'category': category,
    'category_color': category_color,
    'category_reasoning': category_reasoning,
    'category_recommendation': category_recommendation,
    'attachments': attachment_results
  }

  # Set up the Jinja2 environment and load the template
  template_loader = jinja2.FileSystemLoader(searchpath="./")  # Current directory
  template_env = jinja2.Environment(loader=template_loader)

  # Load the HTML template
  template = template_env.get_template("HTML/report.html")

  # Render the template with the data
  html_report = template.render(
    sender=email_data['sender'],
    subject=email_data['subject'],
    received_date=email_data['received_date'],
    category=email_data['category'],
    category_color=email_data['category_color'],
    category_reasoning=email_data['category_reasoning'],
    category_recommendation=email_data['category_recommendation'],
    attachments=email_data['attachments']
  )

  # Save the  HTML report to a file
  with open(filename, "w") as file:
    file.write(html_report)