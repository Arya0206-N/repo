import imaplib
import email
from email.header import decode_header
import time
import threading
import os
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.imap_server = os.getenv("IMAP_SERVER")
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.mail = None
        self.running = False
        self.thread = None

    def connect(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email, self.password)
            self.mail.select("INBOX")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def fetch_emails(self):
        if not self.connect():
            return

        try:
            status, messages = self.mail.search(None, "UNSEEN")
            if status != "OK":
                return

            for num in messages[0].split():
                status, data = self.mail.fetch(num, "(RFC822)")
                if status != "OK":
                    continue

                msg = email.message_from_bytes(data[0][1])
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8")

                print(f"\nSubject: {subject}")
                print("-" * 50)

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        if content_type == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            print(f"Body:\n{body}")
                            self.send_template_response(num)
                else:
                    body = msg.get_payload(decode=True).decode()
                    print(f"Body:\n{body}")
                    self.send_template_response(num)

        except Exception as e:
            print(f"Error fetching emails: {e}")
        finally:
            if self.mail:
                self.mail.close()
                self.mail.logout()

    def send_template_response(self, email_id):
        # Template response implementation would go here
        print(f"[DEBUG] Would send template response to email {email_id}")

    def start_periodic_check(self):
        self.running = True
        self.thread = threading.Thread(target=self._periodic_check)
        self.thread.start()

    def _periodic_check(self):
        while self.running:
            self.fetch_emails()
            time.sleep(30)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

if __name__ == "__main__":
    service = EmailService()
    try:
        print("Starting email service...")
        service.start_periodic_check()
        input("Press Enter to stop...\n")
    finally:
        service.stop()
        print("Service stopped.")