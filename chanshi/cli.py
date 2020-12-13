import os
import sys

import IPython
from IPython.terminal.ipapp import load_default_config

import click
from alembic import command, config
from chanshi.app import app


@click.group('fastapi')
def fastapi():
    pass


@fastapi.command()
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
def shell(ipython_args):
    config = load_default_config()

    config.TerminalInteractiveShell.banner1 = '''Python %s on %s
IPython: %s
App: %s''' % (sys.version,
              sys.platform,
              IPython.__version__,
              app.name)

    IPython.start_ipython(
        argv=ipython_args,
        config=config,
    )


@fastapi.group('db')
def db():
    pass


def init_config(d):
    conf = config.Config(os.path.join(d, 'alembic.ini'))
    conf.set_main_option('script_location', d)
    conf.config_file_name = os.path.join(d, 'alembic.ini')
    return conf


@db.command()
@click.option('-d', '--directory', help='directory of migrations file', default='./migrations')
def init(directory):
    click.echo(f"Init database Migrate File at {directory}")
    path = os.path.abspath(directory)
    if os.path.exists(path):
        # if os.path.getsize(path) > 0:
        #     click.echo(f"Path {path} already exists and not empty")
        #     return
        if not os.path.isdir(path):
            click.echo(f"Path {path} is not a folder")
            return
    os.makedirs(path, exist_ok=True)
    conf = config.Config()
    conf.set_main_option('script_location', path)
    conf.config_file_name = os.path.join(directory, 'alembic.ini')
    command.init(conf, directory)


@db.command()
@click.option('-m', '--message', help="String message to apply to the revision", default='False', type=str)
@click.option('-d', '--directory', help='directory of migrations file', default='./migrations')
def migrate(message, directory):
    conf = init_config(directory)
    command.revision(conf, message, autogenerate=True)


@db.command()
@click.option('-t', '--tag', help="Arbitrary 'tag' name - can be used by custom env.py scripts", default=None)
@click.option('-d', '--directory', help='directory of migrations file', default='./migrations')
@click.option('--sql', help="Don't emit SQL to database - dump to standard output instead", default=False, type=bool)
def upgrade(tag, directory, sql):
    conf = init_config(directory)
    command.upgrade(conf, 'head', sql=sql, tag=tag)
