def test_ok(event, context):
    print "Running test script"
    return {'logs': [{
        'message': 'test',
        'severity': 'info',
        'service': 'beer-distribution',
        'time': '2017-01-12T18:30:42.034751Z'}
        ]}


def test_invalid(event, context):
    print "Running test script"
    return {'logs': [{
        'message': 'test'}
        ]}
