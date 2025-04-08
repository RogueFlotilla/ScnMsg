# Dependencies
from imap_tools import MailBox
import os
import pickle

# Credentials currenty hardcoded; NEED TO REMOVE
mail_username = "sir_clicks_everything@fastmail.com"
mail_password = "793a3y3e8u7j8n2k"

# Create directory for emails (if needed)
save_path = os.path.expanduser(f'~/ScanMsg/{mail_username}/received')
os.makedirs(save_path, exist_ok=True)

# Save unread emails to directory as pickle objects
with MailBox("imap.fastmail.com").login(mail_username, mail_password, "INBOX") as mailbox:
  for message in mailbox.fetch(reverse=True, mark_seen=False):
    # Create email message object
    try:
      with open(f'{save_path}/email_{message.uid}_{message.date.strftime("%Y%m%d_%H%M%S")}.pkl', 'wb') as file:
        pickle.dump(message, file)
    except:
      print("Error getting emails from server and saving to files.")

# Load pickle objects from firectory
for filename in os.listdir(save_path):
  filepath = os.path.join(save_path, filename)
  try:
    with open(filepath, 'rb') as file:
      print(pickle.load(file).subject)
  except:
    print("Error loading {filename} as pickle; check if file is email.")