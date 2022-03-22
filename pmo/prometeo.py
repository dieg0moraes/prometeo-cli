"""
This module provides the Prometeo CLI.
"""
# prometeo/prometeo.py

import typer

from datetime import datetime
from typing import Optional
from pathlib import Path
from typing import Optional

from pmo import __app_name__, __version__
from controllers import prometeo_controller
from helpers import TablePrinter, Profiler


app = typer.Typer()

def date_callback(value):
    if value is None:
        raise typer.BadParameter('Date cannot be null')
    return value


def validate_movements_params(card, account):
    if account == None and card == None:
        raise typer.Exit('Must select one option')

    if account and card:
        raise typer.Exit('Must select only one option')


@app.command()
def login(
    env: str = typer.Option(None, envvar='PROMETEO_ENVIRONMENT'),
    provider: str = typer.Option(None, envvar='PROMETEO_PROVIDER'),
    interactive: bool = typer.Option(False)
) -> None:
    """
    Start a banking session
    """
    typer.echo('Loggin in')

    if env is None:
        raise typer.Exit('Must set an PROMETEO_ENVIRONMENT as envvar')

    if interactive:
        prometeo_controller.login(env, provider, interactive)
        raise typer.Exit('logged in succesfully')

    if provider is None:
        raise typer.Exit('You must specify a provider to login with --provider')

    if env is None:
        raise typer.Exit('You must specify an environment to use with --env')

    prometeo_controller.login(env, provider, interactive)

    raise typer.Exit('Logged in succesfully')



@app.command()
def logout() -> None:
    """
    Logout
    """
    typer.echo('Loggin out')
    prometeo_controller.logout()
    typer.echo('Logged out')


@app.command()
def accounts() -> None:
    """
    Get accounts
    """
    accounts = prometeo_controller.get_accounts()
    printer = TablePrinter()
    printer.print_accounts(accounts)

@app.command()
def cards() -> None:
    """
    Get credit cards
    """
    cards = prometeo_controller.get_cards()
    printer = TablePrinter()
    printer.print_cards(cards)


@app.command()
def movements(
    account: str = typer.Option(
        None,'--account', '-a'
    ),
    card: str = typer.Option(
        None, '--card', '-c'
    ),
    start_date: datetime = typer.Option(
        None, formats=["%Y-%m-%d"], callback=date_callback
    ),
    end_date: datetime = typer.Option(
        None, formats=["%Y-%m-%d"], callback=date_callback
    ),
    currency: str = typer.Option(
        None, '--currency', '-cu'
    )
) -> None:
    """
    Get movements
    """
    validate_movements_params(card, account)

    if account and not card:
        movements = prometeo_controller.get_account_movements(account, start_date, end_date)

    if card and not account:
        if not currency:
            raise typer.Exit('Must enter currency')
        movements = prometeo_controller.get_card_movements(card, start_date, end_date, currency)

    printer = TablePrinter()
    printer.print_movements(movements)


@app.command()
def providers():
    providers = prometeo_controller.get_providers()
    printer = TablePrinter()
    printer.print_providers(providers)


@app.command()
def config():
    providers = prometeo_controller.get_providers()
    printer = TablePrinter()
    printer.print_providers(providers)


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
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    profiler = Profiler()
    profiler.initialize()
    return

