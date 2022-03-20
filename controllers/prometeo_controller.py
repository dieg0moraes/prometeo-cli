import os

from datetime import datetime
from client.prometeo_client import PrometeoClient
from helpers import SessionHandler
from pmo.config import PROMETEO_API_KEY


PROMETEO_SESSION = 'PROMETEO_SESSION'

client = PrometeoClient(PROMETEO_API_KEY)
session = SessionHandler()

def login(provider: str, username: str, password: str) -> None:
    if session.exists_session():
        raise Exception('you have a session started')

    session_key = client.login(provider, username, password)
    session.create_session(session_key)


def logout() -> None:
    banking_session = client.banking.get_session(
            session.retrieve_session()
    )
    banking_session.logout()
    session.end_session()


def get_accounts():
    client = PrometeoClient(PROMETEO_API_KEY)
    banking_session = client.banking.get_session(
            session.retrieve_session()
    )
    return banking_session.get_accounts()

def get_account_movements(account):
    accounts = get_accounts()
    account = next(acc for acc in accounts if acc.number == account)
    return account.get_movements(
            datetime(2019, 2, 1), datetime(2019, 4, 1))

