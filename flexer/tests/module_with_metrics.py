def test_ok(event, context):
    print("Running test script")
    return {'metrics': [{
        'metric': 'cpu-usage',
        'value': 99,
        'unit': 'percent',
        'time': '2017-01-12T18:30:42.034751Z'}
        ]}


def test_invalid(event, context):
    print("Running test script")
    return {'metrics': [{
        'metric': 'cpu-usage',
        'value': 99}
        ]}
