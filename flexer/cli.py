import click
import requests.exceptions
import sys
import os

from flexer import CmpClient, NflexClient, __version__
from flexer.config import CONFIG_FILE
from flexer.module_template import ModuleTemplate
from flexer.utils import (
    load_config,
    print_cmp_logs,
    print_module,
    print_modules,
    print_result,
    prep_err_msg,
)
import flexer.commands

sys.path = [os.getcwd(), os.path.join(os.getcwd(), "lib")] + sys.path

flexer.commands.assert_config_exists()

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
    "cmp-connector.status",
    "cmp-connector.tickets",
    "cmp-resource-notification",
    "monitor",
    "resource-action",
    "rest-api",
    "service-catalog",
    "storage-notification",
    "test",
    "timer",
    "workflow",
]
LANGUAGES = [
    "go",
    "javascript",
    "python",
    "python3",
]


def list_regions():
    return load_config(CONFIG_FILE)["regions"].keys()


class Context(object):
    """The context holds the nflex client"""

    def __init__(self):
        self.config = load_config(CONFIG_FILE)

    def list_regions(self):
        return self.config["regions"].keys()


pass_context = click.make_pass_decorator(Context, ensure=True)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version %s' % __version__)
    ctx.exit()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--auth',
              default="default",
              type=click.Choice(list_regions()),
              help="Connect to a specific CMP region.")
@click.option('--version',
              required=False,
              is_flag=True,
              default=False,
              is_eager=True,
              callback=print_version,
              expose_value=False,
              help="Show the version and exit.")
@pass_context
def cli(ctx, auth):
    """flexer manages your nFlex scripts from the terminal."""
    cfg = ctx.config["regions"][auth]
    verify_ssl = ctx.config.get("verify_ssl", False)
    if "verify_ssl" in cfg:
        verify_ssl = cfg["verify_ssl"]

    ctx.cmp = CmpClient(url=cfg['cmp_url'],
                        auth=(cfg['cmp_api_key'], cfg['cmp_api_secret']),
                        verify_ssl=verify_ssl)
    ctx.nflex = NflexClient(ctx.cmp)


@cli.group(invoke_without_command=True)
@click.pass_context
def config(ctx):
    """Configure the Flexer tool.

    The config file will be stored as ~/.flexer.yaml and you can manually
    modify it to you liking.

    \b
    Description of the configuration options:
    verify_ssl (bool): Disable SSL cert verification
    regions (map): Configuration options for one or more CMP regions. The
        default entry should be always present

    The "verify_ssl" option can be set per region, overriding the global value.
    """
    if ctx.invoked_subcommand is None:
        flexer.commands.config()


@config.command(name="add-region")
@click.option('--secret',
              metavar='SECRET',
              required=True,
              help="The CMP API secret of the region.")
@click.option('--key',
              metavar='KEY',
              required=True,
              help="The CMP API key of the region.")
@click.option('--url',
              metavar='URL',
              required=True,
              help="The CMP URL of the region.")
@click.option('--name',
              metavar='NAME',
              required=True,
              help="The name of the region to add.")
def add_region(name, url, key, secret):
    """Add a new region to the flexer config."""
    flexer.commands.add_config_region(name, url, key, secret)


@cli.command()
@pass_context
def list(ctx):
    """List all nFlex modules."""
    try:
        modules = ctx.nflex.list()
        print_modules(modules)

    except requests.exceptions.RequestException as e:
        raise click.ClickException(
            "Failed to fetch nFlex modules: %s" % prep_err_msg(e)
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
    """Create a new nFlex module."""

    module_type = ModuleTemplate.get_module_type(event_source)
    click.echo('Creating a new {} module...'.format(module_type), err=True)

    template_dir = os.path.join(
        os.path.dirname(__file__),
        "templates",
        module_type
    )
    try:
        os.stat(template_dir)
    except OSError as error:
        if error.errno == 2:  # No such file or directory
            click.echo('Cannot find template directory "%s".' % template_dir,
                       err=True)
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
def get(ctx, module_id):
    """Get an nFlex module.

    If the module type is inline and the source_code is more than 50
    characters long, the source_code field won't be displayed.
    """
    try:
        result = ctx.nflex.get(module_id)
        if len(result["source_code"]) > 50:
            result["source_code"] = "*** REDACTED ***"

        print_module(result)

    except requests.exceptions.RequestException as e:
        raise click.ClickException(
            "Failed to delete nFlex module: %s" % prep_err_msg(e)
        )


@cli.command()
@click.argument('module_id')
@pass_context
def download(ctx, module_id):
    """Download an nFlex module.

    If the module type is inline, the source_code will be saved as "main.py"
    in the current working directory, otherwise the contents of the zip file
    will be extracted there.
    """
    try:
        ctx.nflex.download(module_id)
        click.echo('Module %s downloaded in the current directory' % module_id,
                   err=True)

    except requests.exceptions.RequestException as e:
        raise click.ClickException(
            "Failed to download nFlex module: %s" % prep_err_msg(e)
        )


@cli.command()
@click.option('--zip',
              type=click.Path(exists=True, resolve_path=True),
              help="Upload a zip file")
@click.option('--language',
              type=click.Choice(LANGUAGES),
              help="The programming language of your choice")
@click.argument('module_id')
@click.option('--description',
              required=False,
              help="A short description of the module")
@pass_context
def update(ctx, module_id, zip, language, description):
    """Update an existing module.

    Update the "source_code" or the "description" of an nFlex module.
    """
    try:
        ctx.nflex.update(module_id, zip, language, description=description)
        click.echo("Module %s successfully updated" % module_id, err=True)

    except requests.exceptions.RequestException as e:
        raise click.ClickException(
            "Failed to update nFlex module: %s" % prep_err_msg(e)
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
@click.option('--language',
              required=True,
              type=click.Choice(LANGUAGES),
              default="python",
              help="The programming language of your choice")
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
           language,
           event_source,
           description,
           name):
    """Upload a new module to nFlex."""
    try:
        module = ctx.nflex.upload(name,
                                  description,
                                  event_source,
                                  language,
                                  sync,
                                  zip)
        click.echo("Module created with ID %s" % module['id'], err=True)

    except requests.exceptions.RequestException as e:
        raise click.ClickException(
            "Failed to upload nFlex module: %s" % prep_err_msg(e)
        )


@cli.command()
@click.argument('module_id')
@pass_context
def delete(ctx, module_id):
    """Delete an nFlex module."""
    try:
        response = ctx.nflex.delete(module_id)
        if response.status_code == 204:
            click.echo("Module %s successfully deleted" % module_id)

    except requests.exceptions.RequestException as err:
        raise click.ClickException(
            "Failed to delete nFlex module: %s" % err
        )


@cli.command()
@click.argument('module_id')
@pass_context
def logs(ctx, module_id):
    """Get logs for an nFlex module.

    Query the CMP logs API and fetch all nFlex module logs for the last 24h.
    """
    try:
        logs = ctx.nflex.logs(module_id)
        print_cmp_logs(logs.get("hits", []))

    except requests.exceptions.RequestException as err:
        raise click.ClickException(
            "Failed to fetch nFlex logs: %s" % err
        )


@cli.command()
@click.option('--pretty', is_flag=True, help="DEPRECATED")
@click.option('--config',
              metavar="CONFIG",
              required=False,
              help="The config to run the module with")
@click.option('--secrets',
              required=False,
              help="The secrets to run the module with")
@click.option('--event-source',
              required=False,
              type=click.Choice(EVENT_SOURCES),
              help="The event source for the module")
@click.option('--event',
              metavar="EVENT",
              required=True,
              help="The event to run the module with")
@click.argument('handler')
@pass_context
def run(ctx, handler, event_source, event, config, secrets, pretty):
    """Run an nFlex module locally.

    The command will try to find a "main.py" file in the current working
    directory and execute the HANDLER, passing EVENT as a parameter and
    attaching the CONFIG to the context parameter of the HANDLER.
    EVENT and CONFIG must be valid JSON dictionaries

    HANDLER must be the handler name, i.e. "get_resources", "test_method", etc.

    Any output of the script will be printed on stderr and the return value
    of the HANDLER will be printed as JSON on stdout.
    """
    if pretty:
        click.echo("warn: --pretty is deprecated", err=True)

    result = flexer.commands.run(handler, event_source, event, config, secrets,
                                 ctx.cmp)
    print_result(result)


@cli.command()
@click.option('--pretty', is_flag=True, help="DEPRECATED")
@click.option('--async',
              default=False,
              is_flag=True,
              help="Whether to run the module asynchronously or not")
@click.option('--event',
              metavar="EVENT",
              required=True,
              help="The event to run the module with")
@click.option('--handler',
              metavar="HANDLER",
              required=True,
              help="The handler to execute inside the module")
@click.argument('module_id')
@pass_context
def execute(ctx, module_id, handler, event, is_async, pretty):
    """Run an nFlex module remotely.

    Call the CMP API to trigger a module execution remotely. EVENT must be a
    valid JSON dictionary.

    HANDLER must be the handler name, i.e. "get_resources", "test_method", etc.

    The value of the module execution will be printed as JSON on stdout.
    """
    if pretty:
        click.echo("warn: --pretty is deprecated", err=True)

    try:
        result = ctx.nflex.execute(module_id, handler, is_async, event)
    except requests.exceptions.RequestException as err:
        raise click.ClickException(
            "Failed to execute nFlex module: %s" % err
        )

    print_result(result)


@cli.command()
@click.option('-e', '--exclude',
              multiple=True,
              type=click.Path(resolve_path=False),
              help="Exclude directory from the build")
@click.option('-z', '--zip',
              metavar="ZIP",
              default="/tmp/module.zip",
              type=click.Path(resolve_path=True),
              help="Output zip file name")
@click.argument(
    'directory',
    default=".",
    type=click.Path(exists=True, resolve_path=True, file_okay=False)
)
@pass_context
def build(ctx, directory, zip, exclude):
    """Build an nFlex module from a directory.

    This command will look up DIRECTORY for any requirements-*.txt files
    and install all dependencies under DIRECTORY/lib. It will then create
    a zip file with the contents of DIRECTORY and save it as ZIP. You can
    use the --exclude option to skip directories when building the zip file.
    The zip file can be then used to create/update an nFlex module.
    """
    click.echo("Building module from %s ..." % directory, err=True)
    flexer.commands.install_deps(directory)
    flexer.commands.build_zip(directory, zip, [i for i in exclude])


@cli.command()
@click.option('--keywords', '-k',
              required=False,
              help="Keywords to pass to pytest")
@click.option('-v', '--verbose',
              default=False,
              is_flag=True,
              help='Display verbose output from the test execution')
@pass_context
def test(ctx, verbose, keywords):
    """Run the flexer base tests against a module.

    Run a very basic set of tests for a CMP connector. The tests are available
    under connector_tests/ directory in the flexer repo. Upon execution,
    the command will try to find a "main.py" file in the current working
    directory and execute the "get_resources", "get_credentials" and
    "get_metrics" handlers in that file. The "get_metrics" tests are optional
    and will be skipped if the "get_metrics" handler is not defined in the
    "main.py" file.

    The event passed to the handlers contains only provider credentials
    and those are picked up from the environment. Which environment variables
    are looked up is defined in a "config.yaml" file. The file should be either
    in the current working directory or its path should be passed as a
    CONFIG_YAML environment variable. In that config.yaml file, there must be
    a "credentials_keys" list which defines which environment variables should
    be looked up when building the credentials dictionary

    \b
    Example:
        With a config.yaml file that looks like this:
        ```
        name: Provider Name
        type: provider_name
        credentials_keys:
            - provider_usename
            - provider_password
        expected_resources:
            - server
        ```
        an event like this will be passed to the hanlders when executing tests
        {
            "credentials": {
                "provider_username": <PROVIDER_USERNAME>,
                "provider_password" <PROVIDER_PASSWORD>,
            }
        }
        Then the tests will assert that at least one resource of type server
        is in the return value of the get_resources handler
    """

    result = flexer.commands.test(
        verbose=verbose,
        keywords=keywords,
        cmp_client=ctx.cmp,
    )
    if len(result.failures) + len(result.errors) > 0:
        exit(1)
