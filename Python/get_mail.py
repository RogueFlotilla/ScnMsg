# Dependencies
from operator import itemgetter
from imap_tools import MailBox
import os
import pickle
import configparser

import analyze_mail

def load_email_settings():
  # Create a ConfigParser instance
  config = configparser.ConfigParser()

  # Read Settings File
  config.read('settings.cfg')

  # Access the settings
  mail_username = config.get('EmailSettings', 'email')
  mail_password = config.get('EmailSettings', 'password')
  imap_server = config.get('EmailSettings', 'imap_server')
  smtp_server = config.get('EmailSettings', 'smtp_server')

  return (mail_username, mail_password, imap_server, smtp_server)

def download_mail_from_server(mail_username, mail_password, imap_server, smtp_server):
  # Create directory for emails (if needed)
  global save_path
  global sent_path
  global reports_path
  save_path = os.path.expanduser(f'~/ScnMsg/{mail_username}/received')
  sent_path = os.path.expanduser(f'~/ScnMsg/{mail_username}/sent')
  reports_path = os.path.expanduser(f'~/ScnMsg/{mail_username}/reports')
  os.makedirs(save_path, exist_ok=True)
  os.makedirs(sent_path, exist_ok=True)
  os.makedirs(reports_path, exist_ok=True)

  # Save unread emails to directory as pickle objects and begin scan
  with MailBox(imap_server).login(mail_username, mail_password, "INBOX") as mailbox:
    for message in mailbox.fetch(reverse=True, mark_seen=False):
      # Create email message object
      try:
        with open(f'{save_path}/email_{message.uid}_{message.date.strftime("%Y%m%d_%H%M%S")}.pkl', 'wb') as file:
          pickle.dump(message, file)
      except:
        print("Error getting emails from server and saving to files.")
      # Generate report
      try:
        analyze_mail.scan_message(message)
      except:
        print("Error generating report for email.")

def create_summary_of_emails(mail_username):
  # Create empty list for emails
  received_mail = []

  # Create directory for emails (if needed)
  save_path = os.path.expanduser(f'~/ScnMsg/{mail_username}/received')
  os.makedirs(save_path, exist_ok=True)

  # Create summary list of emails in inbox by looping through email files
  for filename in os.listdir(save_path):
    filepath = os.path.join(save_path, filename)
    try:
      with open(filepath, 'rb') as file:
        # open file
        currentEmail = pickle.load(file)
        # extract summary information
        sender = currentEmail.from_
        subject = currentEmail.subject
        date = currentEmail.date.strftime("%m/%d/%Y %H:%M:%S")
        #currentDate = currentEmail.date.strftime("%a, %B %d, %Y")
        # build dictionary for the email
        reports_path = os.path.expanduser('~/ScnMsg/sir_clicks_everything@fastmail.com/reports')
        filename = f"{reports_path}/email_{currentEmail.uid}_{currentEmail.date.strftime('%Y%m%d_%H%M%S')}.html"
        currentMail = {
          "sender": sender,
          "subject": subject,
          "date": date,
          "report_path": filename
        }
        # append dictionary to list
        received_mail.append(currentMail)
    except:
      print(f"Error with {filename} when building summary list of emails.")
    
  # Sort emails as traditionally viewed (newest first)
  newest_mail = sorted(received_mail, key=itemgetter('date'), reverse=True)

  # Sort emails as traditionally viewed (oldest first)
  oldest_mail = sorted(received_mail, key=itemgetter('date'))

  return (newest_mail, oldest_mail)

# Load an email
def load_email(sender, subject, date):
  for filename in os.listdir(save_path):
    filepath = os.path.join(save_path, filename)
    try:
      with open(filepath, 'rb') as file:
        # open file
        currentEmail = pickle.load(file)
        # extract summary information
        if (
          currentEmail.from_ == sender and 
          currentEmail.subject == subject and 
          currentEmail.date.strftime("%m/%d/%Y %H:%M:%S") == date):
          return currentEmail
    except:
      print("error")
        
if __name__ == "__main__":
  # Load email settings
  mail_username, mail_password, imap_server, smtp_server = load_email_settings()
  
  # Download emails from server and save as pickle objects
  download_mail_from_server(mail_username, mail_password, imap_server, smtp_server)

  # Create summary of emails for table
  newest_mail, oldest_mail = create_summary_of_emails(mail_username)
