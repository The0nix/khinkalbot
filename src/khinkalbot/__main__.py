import logging

import click

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
def init():
    from khinkalbot.db import init as init_db
    init_db()


@cli.command()
def start():
    from khinkalbot.bot import start as start_bot
    start_bot()


@cli.command()
def admin():
    from khinkalbot.db.admin.app import start as start_admin
    start_admin()
