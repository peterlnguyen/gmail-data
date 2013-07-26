import email, getpass, imaplib, os
from datetime import date, timedelta
from credentials import *
from MLStripper import *

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

# helper for retrieving email body content
def extract_body(payload):
	if isinstance(payload, str):
		return payload
	else:
		return '\n'.join([extract_body(part.get_payload()) for part in payload])

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
		body = strip_tags(body_html)	

		print(body) + "\n"

finally:
	try:
		m.close()
	except:
		pass
	m.logout()
