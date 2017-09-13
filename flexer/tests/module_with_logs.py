def test_ok(event, context):
    print("Running test script")
    return {'logs': [{
        'message': 'test',
        'severity': 'INFO',
        'service': 'beer-distribution',
        'time': '2017-01-12T18:30:42.034751Z'}
        ]}


def test_invalid(event, context):
    print("Running test script")
    return {'logs': [{
        'message': 'test'}
        ]}


def test_invalid_severity_value(event, context):
    print("Running test script")
    return {'logs': [{
        'message': 'test',
        'severity': 'HIGH',
        'service': 'beer-distribution',
        'time': '2017-01-12T18:30:42.034751Z'}
        ]}
