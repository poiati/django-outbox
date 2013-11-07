import shutil
import re
from os import path, listdir
from time import sleep
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from expecter import expect

from django_outbox.outbox import Outbox


class OutboxTestMixin(object):

    def setUp(self):
        settings.EMAIL_BACKEND = \
                'django.core.mail.backends.filebased.EmailBackend'

        self._clearmails()

        self.outbox = Outbox()

    def _clearmails(self):
        if path.exists(settings.EMAIL_FILE_PATH):
            shutil.rmtree(settings.EMAIL_FILE_PATH)

    def _send_mail(self, subject='Look at Foo!'):
        sleep(1)

        mail.send_mail(
                subject, 
                'Here is my Foo.', 
                'sender@example.com',
                ['foo@example.com'])

    def _assert_mail_data(self, mail):
        expect(mail.id).contains(datetime.strftime(datetime.now(), '%Y%m%d'))
        expect(mail.subject) == 'Look at Foo!'
        expect(mail.to) == 'foo@example.com'
        expect(mail.from_address) == 'sender@example.com'
        expect(mail.body) == {'text/plain': 'Here is my Foo.\n'}
        expect(mail.content_type) == 'text/plain'


class OutboxAllTest(OutboxTestMixin, TestCase):

    def test_fetch_all_sent_mails(self):
        self._send_mail()
        self._send_mail('Look at Bar!')

        mails = self.outbox.all()

        expect(len(mails)) == 2

    def test_mail_order_is_from_the_most_recent_to_the_oldest(self):
        self._send_mail()
        self._send_mail('Look at Bar!')
        self._send_mail('Look at Qux!')

        mails = self.outbox.all()

        expect([mail.subject for mail in mails]) == [
                'Look at Qux!', 'Look at Bar!', 'Look at Foo!']

    def test_mail_data(self):
        self._send_mail()

        mails = self.outbox.all()
        mail = mails[0]
        
        self._assert_mail_data(mail)


class OutboxGetTest(OutboxTestMixin, TestCase):

    def test_get_a_specific_email(self):
        self._send_mail()

        mail = self.outbox.get(self._get_mail_id())

        self._assert_mail_data(mail)

    def test_multipart_email(self):
        subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p>'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        mail = self.outbox.get(self._get_mail_id())

        expect(mail.id).contains(datetime.strftime(datetime.now(), '%Y%m%d'))
        expect(mail.subject) == subject
        expect(mail.to) == to
        expect(mail.from_address) == from_email
        expect(mail.content_type) == 'multipart/alternative'
        expect(mail.body) == {
                'text/plain': text_content, 
                'text/html': html_content}

    def _get_mail_id(self):
        maildirectory = settings.EMAIL_FILE_PATH
        return path.join(maildirectory, listdir(maildirectory)[0])
