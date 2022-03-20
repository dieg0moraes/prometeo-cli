"""
This module provides the Prometeo CLI.
"""
# prometeo/prometeo.py

import typer

from typing import Optional
from pathlib import Path
from typing import Optional

from pmo import __app_name__, __version__
from controllers import prometeo_controller
from helpers import TablePrinter


app = typer.Typer()


def _username_callback(value: str):
    pass

def _password_callback(value: str):
    pass

def _provider_callback(value: str):
    pass


@app.command()
def login(
    username: str,
    provider: str,
    password: str
) -> None:
    """
    Login
    """
    typer.echo('Loggin in')
    prometeo_controller.login(provider, username, password)
    typer.echo('Logged in succesfully')



@app.command()
def logout() -> None:
    """
    Logout
    """
    typer.echo('Loggin out')
    prometeo_controller.logout()
    typer.echo('Logged out')


@app.command()
def accounts(
) -> None:
    """
    Get accounts
    """
    accounts = prometeo_controller.get_accounts()
    printer = TablePrinter()
    printer.print_accounts(accounts)

@app.command()
def movements(
    account: str = typer.Option(
        None,'--account', '-a'
    ),
    card: str = typer.Option(
        None, '--card', '-c'
    )
) -> None:
    """
    Get accounts
    """
    if account == None and card == None:
        raise typer.Exit('Must select one option')

    if account and card:
        raise typer.Exit('Must select only one option')

    if account and not card:
        movements = prometeo_controller.get_account_movements(account)

    if card and not account:
        movements = prometeo_controller.get_card_movements(card)

    printer = TablePrinter()
    printer.print_movements(movements[:10])


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return

