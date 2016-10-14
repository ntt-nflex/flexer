"""This is an example implementation of a "get_metrics" handler
for cmp-connectors. For the purpose of this example, python generators are
generating fake metrics
"""

import datetime as dt
import itertools
import math


def get_metrics(event, context):
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

    except Exception as e:
        raise Exception("Missing \"%s\" from the event" % e)

    client = NTTTrainingClient(username=username,
                               password=password,
                               region=region)

    metrics = client.get_metrics(provider_id=provider_id,
                                 start_date=start_date,
                                 end_date=end_date)
    context.log("Collected %d metrics from Prototype provider" % len(metrics))
    cmp_metrics = build_cmp_metrics(context, metrics)
    context.log("Built %d CMP metrics" % len(cmp_metrics))

    return post_metrics(context=context,
                        resource_id=resource_id,
                        metrics=cmp_metrics)


"""
Guidelines:

Send metrics to CMP in base units, e.g. B, s, B/s, Hz, percent etc
Use binary units (div 1024) for memory, ram and volumes related metrics) and
SI units (div 1000) for everything else (disks, networks, etc)
"""

METRIC_MAPPING = {
    "Disk Reads per second": {
        "metric": "disk-reads",
        "unit": "B/s",
    },
    "Disk Writes per second": {
        "metric": "disk-writes",
        "unit": "B/s",
    },
    "Network Rx kB/s": {
        "metric": "network-in",
        "unit": "B/s",
        "conversion": lambda x: float(x) * 1000,
    },
    "Network Tx kB/s": {
        "metric": "network-out",
        "unit": "B/s",
        "conversion": lambda x: float(x) * 1000,
    },
    "Memory Usage kB": {
        "metric": "memory-in-use",
        "unit": "B",
        "conversion": lambda x: float(x) * 1024,
    },
    "Memory Usage Percent": {
        "metric": "memory-usage",
        "unit": "pecent",
    },
    "CPU Usage Percent": {
        "metric": "cpu-usage",
        "unit": "percent",
    },
    "CPU Usage MHz": {
        "metric": "cpu-in-use",
        "unit": "Hz",
        "conversion": lambda x: float(x) * 1000 * 1000,
    },
}


# GENERATE SOME DATA
radians = [math.radians(i) for i in range(0, 181)]


def sin_gen(offset, x=1, y=0):
    values = [round(math.sin(rad*x + y) * 10 + offset, 2) for rad in radians]
    return itertools.cycle(values)


def rect_sin_gen(offset, x=1, y=0):
    def rect(x):
        if math.fabs(round(x, 2)) > 0.5:
            return 0.0
        elif math.fabs(round(x, 2)) == 0.5:
            return 0.5
        elif math.fabs(round(x, 2)) < 0.5:
            return 1.0

    values = [round(rect(math.sin(rad*x + y)) * 200 + offset, 2)
              for rad in radians]
    return itertools.cycle(values)


# INFINITE GENERATORS
cpu_usage_percent = sin_gen(50)
cpu_usage_mhz = rect_sin_gen(2000)
mem_usage_percent = sin_gen(50, 3, 3)
mem_usage_kb = rect_sin_gen(250000, 3, 3)
net_rx = sin_gen(200, 14, 2)
net_tx = sin_gen(15, 34, 2)
disk_reads = sin_gen(512000, 3, 15)
disk_writes = sin_gen(128000, 3, 12)


class NTTTrainingClient(object):
    """Fake provider client that generates metrics.

    It uses the metrics generators above to generate fake data
    """

    def __init__(self, *args, **kwargs):
        """The arguments depend on the format of the provider credentials"""
        self.provider = 'ntt-training'

    def get_metrics(self, provider_id, start_date, end_date):
        """Query the provider for metric data and return it"""
        start = dt.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        end = dt.datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        return {
            "Disk Reads per second": self._generate_points(disk_reads,
                                                           start,
                                                           end),
            "Disk Writes per second": self._generate_points(disk_writes,
                                                            start,
                                                            end),
            "Memory Usage kB": self._generate_points(mem_usage_kb,
                                                     start,
                                                     end),
            "Memory Usage Percent": self._generate_points(mem_usage_percent,
                                                          start,
                                                          end),
            "Network Rx kB/s": self._generate_points(net_rx,
                                                     start,
                                                     end),
            "Network Tx kB/s": self._generate_points(net_tx,
                                                     start,
                                                     end),
            "CPU Usage MHz": self._generate_points(cpu_usage_mhz,
                                                   start,
                                                   end),
            "CPU Usage Percent": self._generate_points(cpu_usage_percent,
                                                       start,
                                                       end),
        }

    def _generate_points(self, iterator, start, end):
        points = []
        t = start
        while t <= end:
            points.append({
                "value": next(iterator),
                "time": t.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            })
            t += dt.timedelta(minutes=1)

        return points


def build_cmp_metrics(context, metrics):
    """Convert the provider metrics into a CMP-friendly metrics"""
    cmp_metrics = []
    for metric_name, points in metrics.iteritems():
        try:
            cmp_metric = METRIC_MAPPING[metric_name]

        except KeyError:
            context.log("No metric mapping found for \"%s\"" % metric_name,
                        severity="ERROR")
            continue

        for point in points:
            if 'conversion' in cmp_metric:
                value = cmp_metric["conversion"](point["value"])
            else:
                value = float(point["value"])

            cmp_metrics.append({
                "metric": cmp_metric["metric"],
                "unit": cmp_metric["unit"],
                "time": point["time"],
                "value": value,
            })

    return cmp_metrics


def post_metrics(context, resource_id, metrics):
    """Send the metrics to CMP"""
    data = {
        "resource_id": resource_id,
        "monitoring_system": "ntt-training",
        "metrics": metrics,
    }
    try:
        response = context.api.post(path="/metrics", data=data)
        response.raise_for_status()
        return response.json()

    except Exception as err:
        context.log("Error sending metrics to CMP: %s" % err,
                    severity="ERROR")
