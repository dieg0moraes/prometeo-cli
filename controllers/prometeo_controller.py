import os
import typer
import prometeo

from getpass import getpass
from datetime import datetime

from client.prometeo_client import PrometeoClient
from helpers import SessionHandler, Profiler


PROMETEO_SESSION = 'PROMETEO_SESSION'


session = SessionHandler()


def login(environment: str, provider: str, interactive = False) -> None:
    profiler = Profiler()

    try:
        if session.exists_session():
            confirm = typer.confirm('You have a session stored, want to login in a new one?')

            if confirm == False:
                raise typer.Exit('Session already started')

            session.end_session()

        if interactive:
            provider = typer.prompt('Provider')
            username = typer.prompt('Username')
            password = getpass()
        else:
            username, password = profiler.get_credentials(provider)

        api_key = profiler.get_configuration(environment)
        client = PrometeoClient(api_key)
        session_key = client.login(provider, username, password)
        session.create_session(session_key)

    except (prometeo.exceptions.WrongCredentialsError, KeyError) as e:
        raise typer.Exit('Wrong credentials')

    except prometeo.exceptions.UnauthorizedError as e:
        raise typer.Exit('Unknown provider')



def logout() -> None:
    try:
        banking_session = client.banking.get_session(
                session.retrieve_session()
        )
        banking_session.logout()
        session.end_session()

    except FileNotFoundError as e:
        raise typer.Exit('Session already terminated')


def get_accounts():
    try:
        banking_session = client.banking.get_session(
                session.retrieve_session()
        )
        return banking_session.get_accounts()

    except prometeo.exceptions.InvalidSessionKeyError as e:
        session.end_session()
        raise typer.Exit('Invalid session please login again')

    except FileNotFoundError as e:
        raise typer.Exit('Session already terminated')


def get_account_movements(account, start_date, end_date):
    accounts = get_accounts()
    account = next(acc for acc in accounts if acc.number == account)
    return account.get_movements(start_date, end_date)


def get_cards():
    banking_session = client.banking.get_session(
            session.retrieve_session()
    )
    return banking_session.get_credit_cards()


def get_card_movements(card_id, start_date, end_date, currency):
    cards = get_cards()
    card = next(ca for ca in cards if ca.id == card_id)
    return card.get_movements(currency, start_date, end_date)


def get_providers():
    banking = client.banking
    return banking.get_providers()
