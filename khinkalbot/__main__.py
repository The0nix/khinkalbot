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
    from khinkalbot.bot import start_bot
    start_bot()
