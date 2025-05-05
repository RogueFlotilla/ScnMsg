# Import Dependencies
from bs4 import BeautifulSoup
import hashlib
from io import BytesIO
import json
import os
import requests
import time
import vt

# Import my own Python packages
import report

global hash_scan_history
hash_scan_history = {}

def scan_message(email):
  reports_path = os.path.expanduser('~/ScnMsg/sir_clicks_everything@fastmail.com/reports')
  filename = f"{reports_path}/email_{email.uid}_{email.date.strftime('%Y%m%d_%H%M%S')}.html"
  if os.path.exists(filename):
    return  # Report already exists
  
  else:
    # Determine Category
    categories = ['Normal', 'Spam', 'Phishing', 'Scam', 'Fraud', 'Threat']

    reply = check_email_for_spam(email.text or BeautifulSoup(email.html, "html.parser").get_text())
    if reply.split('.')[0].strip() in categories:
      category = reply.split('.')[0].strip()
      category_reasoning = reply.split('.')[1].strip()
      if category == 'Normal':
        category_color = 'negative'
        category_recommendation = 'This email appears to be safe. No specific guidance suggested.'
      elif category == 'Spam':
        category_color = 'neutral'
        category_recommendation = 'This is unsolicited or irrelevant email, typically promotional.  You may want to ignore it.'
      elif category == 'Phishing':
        category_color = 'positive'
        category_recommendation = 'This email is trying to trick you into revealing sensitive details like your personal information. Do not click links or share any details.'
      elif category == 'Scam':
        category_color = 'positive'
        category_recommendation = 'This message is likely a deceptive scheme to steal money or personal information. Avoid responding and delete it.'
      elif category == 'Fraud':
        category_color = 'positive'
        category_recommendation = 'This email attempts to impersonate a person or organization to gain your trust. Report and delete it immediately.'
      elif category == 'Threat':
        category_color = 'positive'
        category_recommendation = 'This email may contain malware or direct threats. Do not open any attachments or engage with it.'
    else:
      category = 'Unsure'
      category_reasoning = 'Unable to return decision on suspected email purpose.'
      category_color = 'informational'
      category_recommendation = 'The program was unable to confidently determine the nature of this email. If it seems suspicious, avoid interacting and verify the sender.'

    # Check for malicious attachments
    attachment_results = []
    for attachment in email.attachments:
      stats, file_hash = virust_total_file_scan(attachment.payload)
      if stats['malicious'] > 0:
        result = 'Malicious'
        result_color = 'positive'
      elif stats['suspicious'] > 0:
        result = 'Suspicious'
        result_color = 'neutral'
      elif stats['undetected'] > 0:
        result = 'Likely Clean'
        result_color = 'negative'
      elif stats['harmless'] > 0:
        result = 'Harmless'
        result_color = 'negative'
      else:
        result = 'Unknown'
      file_results = {'filename':attachment.filename, 'filetype':attachment.content_type, 'result':result, 'result_color':result_color, 'category_recommendation':category_recommendation, 'sha256hash':file_hash}
      attachment_results.append(file_results)

    if len(attachment_results) == 0:
      attachment_results.append({'filename':'No Attachments', 'filetype':'', 'result':'', 'result_color':'informational', 'sha256hash':''})
    # Compile items to generate report
    report.generate_report(email, category, category_reasoning, category_color, category_recommendation, attachment_results, filename)
    
def check_email_for_spam(email_content):
  GROQ_API_KEY = "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"
  GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

  headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
  }

  data = {
    "model": "llama3-70b-8192",  # Or whatever model you prefer
    "messages": [
      {
        "role": "system",
        "content": "You are an email spam and threat detection assistant. Analyze the content of \
          the email provided, then only respond 'Normal', 'Spam', 'Phishing', 'Scam', 'Fraud', \
          'Threat'. Be pretty strict. We don't want spam. Then on the same line explain why you \
          made this decision."
      },
      {
        "role": "user",
        "content": f"Here is the email content:\n\n{email_content}"
      }
    ],
    "temperature": 0.2
  }

  response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
    
  if response.status_code == 200:
    result = response.json()
    reply = result['choices'][0]['message']['content']
    return reply.strip()
  else:
    print("Error:", response.status_code, response.text)
    return None

def virust_total_file_scan(payload):
  client = vt.Client("43dc3b818c4fb46b9a1082d6b49259fdac697f65b0cf6e7eb1efbf3af25202ec")
  
  # Get file scan results from SHA256 hash
  try:
    file_hash = hashlib.sha256(payload).hexdigest()

    # Check if hash has already been scanned
    if file_hash in hash_scan_history.keys():
      return (hash_scan_history[file_hash], file_hash)

    # Otherwise check hash against Virus Total
    analysis = client.get_object(f'/files/{file_hash}')
    time.sleep(15) # not required if using VT premium API key
  
  # If hash was not found, upload file to Virus Total and wait for scan results
  except:
    try:
      analysis = client.scan_file(BytesIO(payload), wait_for_completion=True)
      time.sleep(15) # not required if using VT premium API key
    except:
      print('file failed to scan')
  finally:
    client.close()
  
  # Save scan results to save time later if same hash is found
  hash_scan_history[file_hash] = analysis.last_analysis_stats

  return (analysis.last_analysis_stats, file_hash)

# if __name__ == "__main__":
  # for filename in os.listdir(save_path):
  #   filepath = os.path.join(save_path, filename)
  #   try:
  #     with open(filepath, 'rb') as file:
  #       # open file
  #       currentEmail = pickle.load(file)
  #   except:
  #     print('Error loading pickle file.')