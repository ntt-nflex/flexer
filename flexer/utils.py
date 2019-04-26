from datetime import datetime
import click
import json
import os
import yaml


def load_config(cfg_file):
    cfg = read_yaml_file(cfg_file)

    # Validate the config file
    try:
        where = ""
        cfg["regions"]
        where = " from regions"
        cfg["regions"]["default"]
        for r, c in cfg["regions"].items():
            where = " from regions.{}".format(r)
            c["cmp_url"]
            c["cmp_api_key"]
            c["cmp_api_secret"]

    except KeyError as err:
        raise click.ClickException(
            "Failed to parse the flexer config file: "
            "the {} key is missing{}!".format(str(err), where)
        )

    return cfg


# I/O
def read_module(module):
    try:
        with open(module) as f:
            return f.read()

    except IOError as err:
        raise click.ClickException(
            "cannot read file {}: {}".format(module, err)
        )


def read_yaml_file(file_name):
    with open(file_name) as f:
        return yaml.safe_load(f)


def write_yaml_file(file_name, data):
    with open(file_name, "w") as f:
        return yaml.dump(data, f, default_flow_style=False)


# aux
def print_module(module):
    click.echo(json.dumps(module, indent=4, sort_keys=True), err=True)


def print_modules(modules):
    trow = (u'{id:36}   {name:30.30}   {description:30.30}    '
            '{user_name:30.30}    {event_source:35}   {file_type:9}   '
            '{language:10}')
    click.echo(trow.format(**{
        'id': 'ID',
        'name': 'NAME',
        'description': 'DESCRIPTION',
        'user_name': 'OWNER',
        'event_source': 'EVENT_SOURCE',
        'file_type': 'FILE_TYPE',
        'language': 'LANGUAGE',
    }), err=True)
    for module in modules:
        click.echo(trow.format(**module), err=True)


def print_result(result):
    logs = result.get("logs")
    if logs:
        click.echo(logs, err=True)

    value = result.get("value")
    error = result.get("error")
    if value:
        click.echo(json.dumps(value, indent=4, sort_keys=True))

    elif error:
        click.echo(json.dumps(error, indent=4, sort_keys=True))


def print_cmp_logs(logs):
    for log in logs:
        timestamp = (datetime
                     .strptime(log["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
                     .replace(microsecond=0)
                     .isoformat() + "Z")
        stats = ""
        if len(log["extra"]):
            mem = log["extra"].get("memory-usage")
            if mem:
                mem = "{}MB".format(int(mem[:-1]) / (1024 * 1024))
            else:
                mem = "N/A"

            stats = " [{} {} {}]".format(
                "cpu-time={}".format(log["extra"].get("cpu-time", "N/A")),
                "duration={}".format(log["extra"].get("duration", "N/A")),
                "memory-usage={}".format(mem)
            )

        line = "{} [{:5}] {}{}".format(timestamp,
                                       log["severity"],
                                       log["message"],
                                       stats)
        click.echo(line, err=True)


def lookup_values(keys):
    if not keys:
        return {}

    return {key: os.getenv("AUTH_" + key.upper()) or os.getenv(key.upper())
            for key in keys}


def prep_err_msg(exc):
    msg = str(exc)
    if exc.response is not None and exc.response.status_code < 500:
        try:
            msg += "\n%s" % exc.response.json()["message"]
        except:
            pass
    return msg


