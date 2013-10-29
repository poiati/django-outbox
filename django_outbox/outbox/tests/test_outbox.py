import shutil
import re
from os import path, listdir
from time import sleep
from datetime import datetime

from django.test import TestCase
from django.core import mail
from django.conf import settings

from expecter import expect

from outbox.outbox import Outbox


class OutboxTestMixin(object):

    def setUp(self):
        settings.EMAIL_BACKEND = \
                'django.core.mail.backends.filebased.EmailBackend'

        self._clearmails()

        mail.send_mail(
                'Look at Foo!', 
                'Here is my Foo.', 
                'sender@example.com',
                ['foo@example.com'])

        self.outbox = Outbox()

    def _clearmails(self):
        if path.exists(settings.EMAIL_FILE_PATH):
            shutil.rmtree(settings.EMAIL_FILE_PATH)


class OutboxAllTest(OutboxTestMixin, TestCase):

    def setUp(self):
        super(OutboxAllTest, self).setUp()

        # Need this beacuse the mail filename is based on the current
        # timestamp, without this the first mail will be overriden
        sleep(1)

        mail.send_mail(
                'Look at Bar!', 
                'Here is my Bar.', 
                'sender@example.com',
                ['bar@example.com'])

    def test_fetch_all_sent_mails(self):
        mails = self.outbox.all()

        expect(len(mails)) == 2

    def test_mail_data(self):
        mails = self.outbox.all()
        mail = mails[0]
        
        expect(mail.id).contains(datetime.strftime(datetime.now(), '%Y%m%d'))
        expect(mail.subject) == 'Look at Foo!'
        expect(mail.to) == 'foo@example.com'
        expect(mail.from_address) == 'sender@example.com'
        expect(mail.body) == 'Here is my Foo.\n'


class OutboxGetTest(OutboxTestMixin, TestCase):

    def test_get_a_specific_email(self):
        mail = self.outbox.get(self._get_mail_id())

        expect(mail) != None

    def _get_mail_id(self):
        maildirectory = settings.EMAIL_FILE_PATH
        return path.join(maildirectory, listdir(maildirectory)[0])
