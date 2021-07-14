import logging
import smtplib
import ssl
from io import StringIO
from typing import Union

import boto3
import pysftp

from src.bridges.interfaces.egress_protocol_interface import EgressProtocolInterface
from src.domain.mail_builder import Mail, AttachmentFile, SMTP
from src.utils.encoder import convert_into_bytearray, convert_into_stringio
from src.utils.log_helper import LogHelper


class MailProtocol(EgressProtocolInterface):

    def __init__(self, smtp: SMTP, subject: str, sender: str, recipients: str, message: str):
        self.mail = Mail(subject=subject, message=message, recipients=recipients, sender=sender)
        self.smtp = smtp

    def build_engine(self):
        server = smtplib.SMTP(self.smtp.smtp_server, self.smtp.smtp_port)
        context = ssl.create_default_context()
        server.starttls(context=context)
        server.login(self.smtp.smtp_username, self.smtp.smtp_password)
        return server

    def send(self, filename=None, data: Union[bytes, StringIO] = None):
        if filename is None or data is None:
            return

        if data is not None and filename is not None:
            if hasattr(data, 'read'):
                print("data is stringIO")
                data = convert_into_bytearray(data)
            self.mail.build_attachment(AttachmentFile(filename=filename, file=data))

        server = self.build_engine()
        server.send_message(self.mail.build_message())
        server.close()


class SftpProtocol(EgressProtocolInterface):

    def __init__(self, host: str, username: str, password: str, port: int, relative_path: str = "/",
                 cnopts=pysftp.CnOpts()):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.relative_path = relative_path
        self.cnopts = cnopts
        LogHelper.log(__name__,
                      f"..[SftpProtocol] initialize..[host] {self.host}, [username] {self.username}, [relative_path] {self.relative_path}",
                      logging.DEBUG)

    def build_engine(self):
        return pysftp.Connection(host=self.host, username=self.username, password=self.password, port=self.port,
                                 cnopts=self.cnopts, default_path=self.relative_path)

    def send(self, filename=None, data: Union[bytes, StringIO] = None):
        if filename is None or data is None:
            return

        if not hasattr(data, 'read'):
            data = convert_into_stringio(data)

        LogHelper.log(__name__, f"..[SftpProtocol] send..[filename] {filename}")
        with self.build_engine() as sftp:
            data.seek(0)
            sftp.putfo(data, filename)

        LogHelper.log(__name__, f"..[SftpProtocol] send successfully..[filename] {filename}")


class S3Protocol(EgressProtocolInterface):

    def __init__(self, bucket: str, relative_path: str, aws_key: str, aws_secret: str,
                 aws_region: str = "ap-southeast-1"):
        self.aws_key = aws_key
        self.aws_secret = aws_secret
        self.aws_region = aws_region
        self.bucket = bucket
        self.relative_path = relative_path
        LogHelper.log(__name__,
                      f"..[S3Protocol] initialize..[bucket] {self.bucket}, [relative_path] {self.relative_path}",
                      logging.DEBUG)

    def build_engine(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret,
            region_name=self.aws_region
        )

    def send(self, filename=None, data: Union[bytes, StringIO] = None):
        if filename is None or data is None:
            return

        LogHelper.log(__name__, f"..[S3Protocol] send..[filename] {filename}")

        if hasattr(data, 'read'):
            print("data is stringIO")
            data = convert_into_bytearray(data)

        print(f"data {data}")
        self.build_engine().put_object(Bucket=self.bucket,
                                       Key=f"%s/%s" % (self.relative_path, filename), Body=data,
                                       CacheControl="no-cache")
        LogHelper.log(__name__, f"..[S3Protocol] send successfully..[filename] {filename}")
