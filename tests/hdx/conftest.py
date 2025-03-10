"""Global fixtures"""
import smtplib
from os.path import join

import pytest

from hdx.utilities.downloader import Download


@pytest.fixture(scope="session")
def fixturesfolder():
    return join("tests", "fixtures")


@pytest.fixture(scope="session")
def configfolder(fixturesfolder):
    return join(fixturesfolder, "config")


@pytest.fixture(scope="function")
def mocksmtp(monkeypatch):
    class MockSMTPBase:
        type = None

        def __init__(self, **kwargs):
            self.initargs = kwargs

        def login(self, username, password):
            self.username = username
            self.password = password

        def sendmail(self, sender, recipients, msg, **kwargs):
            self.sender = sender
            self.recipients = recipients
            self.msg = msg
            self.send_args = kwargs

        @staticmethod
        def quit():
            pass

    class MockSMTPSSL(MockSMTPBase):
        type = "smtpssl"

    class MockLMTP(MockSMTPBase):
        type = "lmtp"

    class MockSMTP(MockSMTPBase):
        type = "smtp"

    monkeypatch.setattr(smtplib, "SMTP_SSL", MockSMTPSSL)
    monkeypatch.setattr(smtplib, "LMTP", MockLMTP)
    monkeypatch.setattr(smtplib, "SMTP", MockSMTP)


@pytest.fixture(scope="function")
def downloaders():
    custom_user_agent = "custom"
    extra_params_dict = {"key1": "val1"}
    custom_configs = {
        "test": {
            "user_agent": custom_user_agent,
            "basic_auth": "dXNlcjpwYXNz",
            "extra_params_dict": extra_params_dict,
        },
        "test2": {
            "user_agent": "lalala",
        },
    }
    user_agent = "test"
    Download.generate_downloaders(custom_configs, user_agent=user_agent)
    return user_agent, custom_user_agent, extra_params_dict
