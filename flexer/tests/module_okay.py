def test_with_no_logs(event, context):
    return 42


def test_with_logs(event, context):
    print "This goes to stdout"
    return 42


def test_with_exception(event, context):
    print "Before the exception"
    a, b = 'nospace'.split()
