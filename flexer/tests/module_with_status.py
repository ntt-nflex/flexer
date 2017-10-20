def test_ok(event, context):
    print("Running test script")
    return {'status': [
        {
            'level': '0',
            'source': 'nflex-connector',
            'reason': 'vm is running',
            'time': '2017-01-12T18:30:42.034751Z'
        },
        {
            'level': '1',
            'source': 'nflex-connector',
            'reason': 'vm is running',
            'time': '2017-01-12T18:30:42.034751Z'
        },
        {
            'level': '2',
            'source': 'nflex-connector',
            'reason': 'vm is running',
            'time': '2017-01-12T18:30:42.034751Z'
        },
    ]}


def test_missing_level(event, context):
    print("Running test script")
    return {'status': [
        {
            'source': 'nflex-connector',
            'reason': 'vm is running',
            'time': '2017-01-12T18:30:42.034751Z'
        },
    ]}


def test_missing_time(event, context):
    print("Running test script")
    return {'status': [
        {
            'level': '0',
            'source': 'nflex-connector',
            'reason': 'vm is running'
        },
    ]}


def test_invalid_level(event, context):
    print("Running test script")
    return {'status': [
        {
            'level': '3',
            'source': 'nflex-connector',
            'reason': 'vm is running',
            'time': '2017-01-12T18:30:42.034751Z'
        },
    ]}
