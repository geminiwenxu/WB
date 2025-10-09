import email
from email import policy
from email.parser import BytesParser

def extract_mail_for_rag(file):
    """ Extract information from a Mail file """
    with open(file, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg["Subject"]
    sender = msg["From"]

    if msg.is_multipart():
        body = ""
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    document = f"From: {sender}\nSubject: {subject}\n{body}"

    return document