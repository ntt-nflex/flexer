from datetime import datetime


def get(event, context):
    payload = {
        'name': 'metric-name',
        'unit': 'B',
        'label': {
            'en': {
                'text': 'Description of the metric',
                'specialisations': ['(%s)']
            }
        },
        'downsampling-func': 'sum',
        'aggregation-func': 'mean',
        'specialisation-func': 'max',
    }
    resp = context.api.post('/metric-definitions', payload)
    print(resp.status_code, resp.text)

    data = {
        'resource_id': 'resource-UUID',
        'metrics': [{
            'metric': 'metric-name',
            'unit': 'B',
            'value': float(42),
            'time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        }]
    }
    resp = context.api.post('/metrics', data)
    print(resp.status_code, resp.text)
