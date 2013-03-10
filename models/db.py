def getDb():
    '''
        returns a test DAL object when user agent is unittest; otherwise default
    '''
    
    db_name = "uvs" # default
    
    # use another database for unit tests (in tests directory) so that it doesn't
    # mess up current database
    if (request.env.http_user_agent == 'unittest'):
        db_name = 'unittest'
    
    uri = "sqlite://{0}.sqlite".format(db_name)
    return DAL(uri, lazy_tables=True)


db = getDb()

db.define_table('User',
    Field('username', notnull=True, unique=True),
    Field('password', notnull=True),
    Field('name'),
    Field('email'))

db.define_table('Group',
    Field('name', notnull=True))

db.define_table('Membership',
    Field('userID', 'reference User'),
    Field('groupID', 'reference Group'),
    Field('owner', 'boolean'))

db.define_table('Session',
    Field('name'),
    Field('sessionOwner', 'reference Group'),
    Field('timeCreated', 'datetime'),
    Field('type'),
    Field('password'),
    Field('startDate', 'date'),
    Field('endDate', 'date'))

db.define_table('Question',
    Field('sessionID', 'reference Session'),
    Field('questionText', 'text'),
    Field('code'))

db.define_table('MultipleChoice',
    Field('questionID', 'reference Question'),
    Field('choiceText', notnull=True),
    Field('Correct', 'boolean'))

db.define_table('SessionAnswer',
    Field('sessionID', 'reference Session'),
    Field('responder', 'reference User'),
    Field('submitTime', 'datetime'))

db.define_table('Answer',
    Field('sessionAnswerID', 'reference SessionAnswer'),
    Field('questionID', 'reference Question'),
    Field('answerText', 'text'))
