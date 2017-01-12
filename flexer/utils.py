import click
import json


def load_config(cfg_file):
    try:
        cfg = read_json_file(cfg_file)
        cfg["cmp_url"]
        cfg["cmp_api_key"]
        cfg["cmp_api_secret"]
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
    trow = (u'{id:36}   {name:30.30}   {user_name:30.30}   '
            '{event_source:35}   {file_type:9}   {language:10}')
    click.echo(trow.format(**{
        'id': 'ID',
        'name': 'NAME',
        'user_name': 'OWNER',
        'event_source': 'EVENT_SOURCE',
        'file_type': 'FILE_TYPE',
        'language': 'LANGUAGE',
    }))
    for module in modules:
        click.echo(trow.format(**module))


def print_result(result, pretty):
    if pretty:
        # pprint is overrated
        result = json.dumps(json.loads(result), indent=4)

    click.echo(result)
