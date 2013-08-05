import email, getpass, imaplib, os, re
from datetime import date, timedelta
from credentials import *
from MLStripper import *
from bs4 import BeautifulSoup
import nltk
from nltk.collocations import *

from sklearn.feature_extraction.text import CountVectorizer

detach_dir = './attachments' # directory where to save attachments (default: current)

# connecting to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(EMAIL, PHRASE)
m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
# use m.list() to get all the mailboxes

# configure date
yesterday = (date.today() - timedelta(1)).strftime("%d-%B-%Y")
search_criteria = '(SINCE ' + yesterday + ')'

resp, items = m.search(None, search_criteria) # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id

###

def visible(element):
  if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
    return False
  elif re.match('<!--.*-->', (element).encode('utf-8')):
    return False
  return True

###

# helper for retrieving email body content
def extract_body(payload):
  if isinstance(payload, str):
    return payload
  else:
    return '\n'.join([extract_body(part.get_payload()) for part in payload])

fdist = None

try:
  for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
    email_body = data[0][1] # getting the mail content
    mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

    #Check if any attachments at all
    if mail.get_content_maintype() != 'multipart':
      continue

    print "From: " + mail["From"]
    print "Subject: " + mail["Subject"]
    print "Date: " + mail["Date"] + "\n"

    payload = mail.get_payload()
    body_html = extract_body(payload)

    # strip css and javascript
    body = ''.join(BeautifulSoup(body_html).findAll(text=lambda text: 
    text.parent.name != "script" and 
    text.parent.name != "style"))

    # tokenize and get gram count
    tokens = nltk.word_tokenize(body)

    bgs = nltk.bigrams(tokens)

    fdist = nltk.FreqDist(bgs)
    for k, v in fdist.items():
      if v > 10: print k, v         

    #print n_grams + "\n"


finally:
  try:
    m.close()
  except:
    pass
  m.logout()
