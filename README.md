This script will scan through email and pull the top bigrams and trigrams, storing them in a database to occasionally topically classify and generate a report or two.

Uses:
- Rename "credentials.example.py" to "credentials.py" and fill in credentials.  Gmail users with two-step verification need to enter the generated application key instead of their password.
- Run "make build" to pull daily emails from gmail (in the 24 hour period starting from yesterday's midnight).  The timeframe can be adjusted in "gmail.py".
- Set chron jobs to automate the process daily, weekly, or however long you wish: http://www.thesitewizard.com/general/set-cron-job.shtml




