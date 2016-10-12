import click
import json


def load_config(cfg_file):
    try:
        cfg = read_json_file(cfg_file)
        cfg["cmp_url"]
        cfg["cmp_username"]
        cfg["cmp_password"]
        return cfg

    except KeyError as err:
        raise click.ClickException(
            "Failed to parse the flexer config file: "
            "the %s key is missing!" % str(err)
        )

    except ValueError as err:
        raise click.ClickException(
            "Failed to parse the flexer config file: "
            "make sure it's a valid JSON object"
        )

    except IOError as err:
        raise click.ClickException(
            "The flexer config file is not found: "
            "make sure `flexer config` is run"
        )


# I/O
def read_module(module):
    try:
        with open(module) as f:
            return f.read()

    except IOError as err:
        raise click.ClickException("cannot read file %s: %s" % module, err)


def write_json_file(file_name, data):
    with open(file_name) as f:
        return json.dump(data, f, indent=4)


def read_json_file(file_name):
    with open(file_name) as f:
        return json.load(f)


# aux
def print_modules(modules):
    thead = '{:36}   {:30.30}   {:50.50}   {:15}   {:5}'
    click.echo(thead.format(
        'ID', 'NAME', 'DESCRIPTION', 'EVENT_SOURCE', 'FILE_TYPE'
    ))
    trow = ('{id:36}   {name:30.30}   {description:50.50}   '
            '{event_source:15}   {file_type:5}')
    if len(modules) > 50:
        click.echo_via_pager("\n".join([
            trow.format(**module) for module in modules
        ]))

    else:
        for module in modules:
            click.echo(trow.format(**module))


def print_result(result, pretty):
    if pretty:
        # pprint is overrated
        result = json.dumps(json.loads(result), indent=4)

    click.echo(result)
