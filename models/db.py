
def getDb():
    '''
        returns a test DAL object when user agent is unittest; otherwise default
    '''
    
    db_name = "db" # default
    
    # use another database for unittest so that it doesn't mess up current database
    if (request.env.http_user_agent == 'unittest'):
        db_name = 'unittest'
    
    uri = "sqlite://{0}.sqlite".format(db_name)
    return DAL(uri, lazy_tables=True)


db = getDb()

db.define_table('polls',
    Field('title'))

db.define_table('pollChoices',
    Field('pid', 'reference polls'),
    Field('content'))

db.define_table('userChose',
    Field('cid', 'reference pollChoices'))
