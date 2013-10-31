import shutil
import re
from os import path, listdir
from time import sleep
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.conf import settings

from expecter import expect

from django_outbox.outbox import Outbox


class OutboxTestMixin(object):

    def setUp(self):
        settings.EMAIL_BACKEND = \
                'django.core.mail.backends.filebased.EmailBackend'

        self._clearmails()
        self._send_mail()

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
        expect(mail.body) == 'Here is my Foo.\n'


class OutboxAllTest(OutboxTestMixin, TestCase):

    def test_fetch_all_sent_mails(self):
        self._send_mail('Look at Bar!')

        mails = self.outbox.all()

        expect(len(mails)) == 2

    def test_mail_order_is_from_the_most_recent_to_the_oldest(self):
        self._send_mail('Look at Bar!')
        self._send_mail('Look at Qux!')

        mails = self.outbox.all()

        expect([mail.subject for mail in mails]) == [
                'Look at Qux!', 'Look at Bar!', 'Look at Foo!']

    def test_mail_data(self):
        mails = self.outbox.all()
        mail = mails[0]
        
        self._assert_mail_data(mail)


class OutboxGetTest(OutboxTestMixin, TestCase):

    def test_get_a_specific_email(self):
        mail = self.outbox.get(self._get_mail_id())

        self._assert_mail_data(mail)

    def _get_mail_id(self):
        maildirectory = settings.EMAIL_FILE_PATH
        return path.join(maildirectory, listdir(maildirectory)[0])
