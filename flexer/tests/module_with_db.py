def test(event, context):
    coll = context.database("mydb").test_colletion
    return {'result': coll.find()}
