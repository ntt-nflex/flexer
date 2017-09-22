def good_spend1(event, context):
    return {
        'amount': 11,
        'currency': 'GBP',
        'items': [
            {
                'amount': 1.0,
                'remote_id': '13',
                'resource_type': 'servers'
            }
        ],
        'spend_date': '2018-12-04'
    }


def good_spend2(event, context):
    return {
        'amount': [
            {'remote_id': 'abcd', 'amount': 123.2}
        ],
        'currency': 'GBP',
        'items': [
            {
                'amount': 1.0,
                'remote_id': '13',
                'resource_type': 'servers'
            }
        ],
        'spend_date': '2018-12-04'
    }


def good_spend3(event, context):
    return {
        'amount_accumulative': 12.2,
        'currency': 'GBP',
        'items': [
            {
                'amount': 1.0,
                'remote_id': '13',
                'resource_type': 'servers'
            }
        ],
        'spend_date': '2018-12-04'
    }



def bad_spend1(event, context):
    return {
        'amount': 12.2,
        'items': [
            {
                'ok': 'nop'
            }
        ],
    }


def bad_spend2(event, context):
    return {
        'amount': 12.2,
        'items': [],
        'currency': 'USD'
    }


def bad_spend3(event, context):
    return {
        'amount': 12.2,
        'items': [],
        'spend_date': '2017-09-21'
    }


def bad_spend4(event, context):
    return {
        'amount': '12.2',
        'items': [],
        'spend_date': '2017-09-21',
        'currency': 'xyz'
    }
