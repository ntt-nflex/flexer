import resource


def test(event, context):
    print "Starting Up"

    data = []
    x = 99999999
    for i in xrange(0, x):
        data.append(i)
        if i % 10000 == 0:
            print i, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    print "done"
    return ["foo"]
