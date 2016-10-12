import click
import requests.exceptions
import sys
import os

from flexer import CmpClient, NflexClient
from flexer.config import CONFIG_FILE
from flexer.utils import load_config, print_modules, print_result
import flexer.commands

sys.path.append(os.getcwd())

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
EVENT_SOURCES = [
    "cmp-connector",
    "cmp-resource-notification",
    "api-hook",
    "timer",
    "test",
    "service-catalog",
]


class Context(object):
    """The context holds the nflex client"""

    def __init__(self):
        self.credentials = load_config(CONFIG_FILE)
        self.cmp = CmpClient(url=self.credentials['cmp_url'],
                             auth=(self.credentials['cmp_username'],
                                   self.credentials['cmp_password']))
        self.nflex = NflexClient(self.cmp)


pass_context = click.make_pass_decorator(Context, ensure=True)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """flexer manages your nFlex scripts from the terminal."""
    pass


@cli.command()
def config():
    """Configure the CMP URL and credentials."""
    flexer.commands.config()


@cli.command()
@pass_context
def list(ctx):
    """List all nFlex modules."""
    try:
        modules = ctx.nflex.list()
        print_modules(modules)

    except requests.exceptions.RequestException as err:
        e = "request failed [code %d] - %s" % (err.response.status_code,
                                               err.response.text)
        raise click.ClickException(
            "Failed to fetch nFlex modules: %s" % e
        )


@cli.command()
@click.argument('module_id')
@pass_context
def download(ctx, module_id):
    """Download a nFlex module."""
    try:
        ctx.nflex.download(module_id)
        click.echo('Module %s downloaded in the current directory' % module_id)

    except requests.exceptions.RequestException as err:
        e = "request failed [code %d] - %s" % (err.response.status_code,
                                               err.response.text)
        raise click.ClickException(
            "Failed to download nFlex module: %s" % e
        )


@cli.command()
@click.option('--zip',
              type=click.Path(exists=True, resolve_path=True),
              help="Upload a zip file")
@click.argument('module_id')
@pass_context
def update(ctx, module_id, zip):
    """Update the source code of an existing nFlex module."""
    try:
        ctx.nflex.update(module_id, zip)
        click.echo("Module %s successfuly updated" % module_id)

    except requests.exceptions.RequestException as err:
        e = "request failed [code %d] - %s" % (err.response.status_code,
                                               err.response.text)
        raise click.ClickException(
            "Failed to update nFlex module: %s" % e
        )


@cli.command()
@click.option('--name',
              required=True,
              help="The name of the module")
@click.option('--description',
              required=False,
              help="A short description of the module")
@click.option('--event-source',
              required=True,
              type=click.Choice(EVENT_SOURCES),
              help="The event source for the module")
@click.option('--sync',
              default=False,
              is_flag=True,
              help='Sync the module globally (only for "cmp-connector")')
@click.option('--zip',
              type=click.Path(exists=True, resolve_path=True),
              help="Upload a zip file")
@pass_context
def upload(ctx,
           zip,
           sync,
           event_source,
           description,
           name):
    """Upload a new module to nFlex."""
    try:
        module = ctx.nflex.upload(name,
                                  description,
                                  event_source,
                                  sync,
                                  zip)
        click.echo("Module created with ID %s" % module['id'])

    except requests.exceptions.RequestException as err:
        e = "request failed [code %d] - %s" % (err.response.status_code,
                                               err.response.text)
        raise click.ClickException(
            "Failed to upload nFlex module: %s" % e
        )


@cli.command()
@click.option('--pretty',
              default=False,
              is_flag=True,
              help='Pretty print the execution result')
@click.option('--event',
              required=True,
              help="The event to run the module with")
@click.argument('handler')
@pass_context
def run(ctx, handler, event, pretty):
    """Run an nFlex module locally."""
    result = flexer.commands.run(handler, event, ctx.cmp)
    print_result(result, pretty)
