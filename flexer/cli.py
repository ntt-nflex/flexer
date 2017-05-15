import click
import requests.exceptions
import sys
import os

from flexer import CmpClient, NflexClient
from flexer.config import CONFIG_FILE
from flexer.module_template import ModuleTemplate
from flexer.utils import load_config, print_modules, print_result
import flexer.commands

sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "lib"))

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
}
EVENT_SOURCES = [
    "alert-notification",
    "api-hook",
    "cmp-connector",
    "cmp-connector.alerts",
    "cmp-connector.credentials",
    "cmp-connector.logs",
    "cmp-connector.metrics",
    "cmp-connector.resources",
    "cmp-connector.spend",
    "cmp-connector.tickets",
    "cmp-resource-notification",
    "monitor",
    "service-catalog",
    "storage-notification",
    "test",
    "timer",
    "workflow",
]


class Context(object):
    """The context holds the nflex client"""

    def __init__(self):
        self.credentials = load_config(CONFIG_FILE)
        self.cmp = CmpClient(url=self.credentials['cmp_url'],
                             auth=(self.credentials['cmp_api_key'],
                                   self.credentials['cmp_api_secret']))
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
        raise click.ClickException(
            "Failed to fetch nFlex modules: %s" % err
        )


@cli.command(name='new')
@click.option('--name',
              required=True,
              help="A name for the new module")
@click.option('--event-source',
              required=True,
              type=click.Choice(EVENT_SOURCES),
              help="The event source for the module")
@pass_context
def new_module(ctx, name, event_source):
    """
    Create a new nFlex module.
    """

    module_type = ModuleTemplate.get_module_type(event_source)
    click.echo(
        'Creating a new {} module...'.format(module_type)
    )

    template_dir = os.path.join(
        os.path.dirname(__file__),
        "templates",
        module_type
    )
    try:
        os.stat(template_dir)
    except OSError as error:
        if error.errno == 2:  # No such file or directory
            click.echo('Cannot find template directory "%s".' % template_dir)

            return

        raise

    template = ModuleTemplate(template_dir, event_source)
    template.apply(
        ctx.cmp,
        name,
        os.getcwd()
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
        raise click.ClickException(
            "Failed to download nFlex module: %s" % err
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
        raise click.ClickException(
            "Failed to update nFlex module: %s" % err
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
        raise click.ClickException(
            "Failed to upload nFlex module: %s" % err
        )


@cli.command()
@click.option('--pretty',
              default=False,
              is_flag=True,
              help='Pretty print the execution result')
@click.option('--config',
              required=False,
              help="The config to run the module with")
@click.option('--event',
              required=True,
              help="The event to run the module with")
@click.argument('handler')
@pass_context
def run(ctx, handler, event, config, pretty):
    """Run an nFlex module locally."""
    result = flexer.commands.run(handler, event, config, ctx.cmp)
    print_result(result, pretty)


@cli.command()
@click.option('--pretty',
              default=False,
              is_flag=True,
              help='Pretty print the execution result')
@click.option('--async',
              default=False,
              is_flag=True,
              help="Whether to run the module asynchronously or not")
@click.option('--event',
              required=True,
              help="The event to run the module with")
@click.option('--handler',
              required=True,
              help="The handler to execute inside the module")
@click.argument('module_id')
@pass_context
def execute(ctx, module_id, handler, event, async, pretty):
    """Run an nFlex module remotely."""
    try:
        result = ctx.nflex.execute(module_id, handler, async, event)
    except requests.exceptions.RequestException as err:
        raise click.ClickException(
            "Failed to execute nFlex module: %s" % err
        )

    print_result(result, pretty)


@cli.command()
@click.option('-z', '--zip',
              default="connector.zip",
              type=click.Path(resolve_path=True),
              help="Output zip file name")
@click.argument(
    'd',
    default=".",
    type=click.Path(exists=True, resolve_path=True, file_okay=False)
)
@pass_context
def build(ctx, d, zip):
    """Build an nFlex module from the content of a directory."""
    click.echo("Building module from %s ..." % d)
    click.echo("Installing dependencies...")
    flexer.commands.install_deps(d)
    click.echo("Archiving everything under %s as %s" % (d, zip))
    flexer.commands.build_zip(d, zip)
