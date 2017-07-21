def test_ok(event, context):
    print("Running test script")
    return {'metrics': [{
        'metric': 'cpu-usage',
        'value': 99,
        'unit': 'percent',
        'time': '2017-01-12T18:30:42.034751Z',
        'resource_id': '1237ab91-08eb-4164-8e68-67699c29cd4c'}
        ]}


def test_invalid(event, context):
    print("Running test script")
    return {'metrics': [{
        'metric': 'cpu-usage',
        'value': 99}
        ]}
