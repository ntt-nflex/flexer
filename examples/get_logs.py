"""This is an example implementation of a "get_logs" handler
for cmp-connectors. For the purpose of this example, a python generator is
generating fake logs
"""

import datetime as dt
import itertools


def get_logs(event, context):
    # mock the credentials for now, they're usually inside the event
    # e.g. credentials = event['credentials']
    credentials = {
        "username": "usr",
        "password": "pass",
        "region": "eu"
    }
    try:
        username = credentials["username"]
        password = credentials["password"]
        region = credentials["region"]  # Provider region of the resource
        provider_id = event["provider_id"]  # Provider ID of the resource
        resource_id = event["resource_id"]  # CMP ID of the resource
        start_date = event["start_date"]
        end_date = event["end_date"]

    except KeyError as e:
        raise Exception("Missing \"%s\" from the event" % e)

    client = NTTTrainingClient(username=username,
                               password=password,
                               region=region)

    logs = client.get_logs(provider_id=provider_id,
                           start_date=start_date,
                           end_date=end_date)
    context.log("Collected %d logs from Prototype provider" % len(logs))

    cmp_logs = build_cmp_logs(context, resource_id, logs)
    context.log("Built %d CMP logs" % len(cmp_logs))

    return post_logs(context=context, data=cmp_logs)


ADJECTIVES = [
    "bad", "terrible", "awful", "sinister", "despicable",
    "good", "great", "groovy", "wonderful", "marvelous",
    "weird", "mysterious", "unexpected", "worrying",
]


def logs_generator(adjectives):
    values = ["Something %s happened" % adj for adj in adjectives]
    return itertools.cycle(values)


logs = logs_generator(adjectives=ADJECTIVES)


class NTTTrainingClient(object):
    """Fake provider client that generates logs.

    It uses the logs generator above to generate fake data
    """

    def __init__(self, *args, **kwargs):
        """The arguments depend on the format of the provider credentials"""
        self.provider = 'ntt-training'

    def get_logs(self, provider_id, start_date, end_date):
        """Query the provider for log data and return it"""
        start = dt.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end = dt.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        return self._generate_logs(logs, start, end)

    def _generate_logs(self, iterator, start, end):
        logs = []
        t = start
        while t <= end:
            logs.append({
                "message": next(iterator),
                "level": "INFO",
                "time": t.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            })
            t += dt.timedelta(minutes=1)

        return logs


def build_cmp_logs(context, resource_id, logs):
    """Convert the provider logs into a CMP-friendly format"""
    cmp_logs = []
    for log in logs:
        cmp_logs.append({
            "service": "nflex.cmp-adapter.ntt-training",
            "resource_id": resource_id,
            "severity": log["level"],
            "timestamp": log["time"],
            "message": log["message"],
        })

    return cmp_logs


def post_logs(context, data):
    """Send the logs to CMP"""
    try:
        response = context.api.post(path="/logs", data=data)
        response.raise_for_status()
        return response.json()

    except Exception as err:
        context.log("Error sending logs to CMP: %s" % err,
                    severity="ERROR")
