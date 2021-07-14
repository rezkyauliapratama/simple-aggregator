from abc import ABC, abstractmethod
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, Optional

from pydantic import BaseModel


class AttachmentFile(BaseModel):
    filename: str
    file: Union[list, str, bytes]


class SMTP(BaseModel):
    smtp_server: str
    smtp_port: str
    smtp_username: str
    smtp_password: str


class MailBuilder(ABC):

    @abstractmethod
    def build_attachment(self, attachment_files: AttachmentFile): pass

    @abstractmethod
    def build_message(self, mime: str = 'html') -> MIMEMultipart: pass


class Mail(MailBuilder):

    def build_message(self, mime: str = 'html') -> MIMEMultipart:
        message = MIMEMultipart()
        message["Subject"] = self.subject
        message["From"] = self.sender
        message["To"] = self.recipients
        msg = MIMEText(self.message, mime)
        message.attach(msg)

        if self.attachment_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(self.attachment_file.file)

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {self.attachment_file.filename}",
            )
            message.attach(part)

        return message

    def __init__(self, subject: str, message: str, recipients: str, sender: str):
        self.attachment_file: Optional[AttachmentFile] = None
        self.message: str = message
        self.subject = subject
        self.recipients = recipients
        self.sender = sender

    def build_attachment(self, attachment_files: AttachmentFile):
        self.attachment_file = attachment_files
