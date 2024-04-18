import os
import imaplib
import email
from email.header import decode_header

username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

imap = imaplib.IMAP4_SSL("imap.gmail.com")

imap.login(username, password)

imap.select("INBOX")

status, messages = imap.search(None, "ALL")
messages = messages[0].split(b' ')
message_count = 0

print(f"Cleaning inbox now, starting count of messages deleted: ")

for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject = decode_header(msg["Subject"])
            if isinstance(subject, bytes):
                subject = subject.decode()
            message_count += 1
            print(f"{message_count}")

    imap.store(mail, "+FLAGS", "//Deleted")
    print(f"Total emails deleted: {message_count}")

imap.expunge()

imap.close()

imap.logout()


