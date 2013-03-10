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
    return DAL(uri, lazy_tables=True, check_reserved=['all'])


db = getDb()

db.define_table('uvsUser',
    Field('username', notnull=True, unique=True),
    Field('password', notnull=True),
    Field('name'),
    Field('email'))

db.define_table('uvsGroup',
    Field('name', notnull=True))

db.define_table('Membership',
    Field('userID', 'reference uvsUser'),
    Field('groupID', 'reference uvsGroup'),
    Field('uvsOwner', 'boolean'))

db.define_table('uvsSession',
    Field('name'),
    Field('sessionOwner', 'reference uvsGroup'),
    Field('timeCreated', 'datetime', default=request.now),
    Field('uvsType'),
    Field('password'),
    Field('startDate', 'date'),
    Field('endDate', 'date'))

db.define_table('Question',
    Field('sessionID', 'reference uvsSession'),
    Field('questionText', 'text'),
    Field('code'))

db.define_table('MultipleChoice',
    Field('questionID', 'reference Question'),
    Field('choiceText', notnull=True),
    Field('Correct', 'boolean'))

db.define_table('SessionAnswer',
    Field('sessionID', 'reference uvsSession'),
    Field('responder', 'reference uvsUser'),
    Field('submitTime', 'datetime', default=request.now))

db.define_table('Answer',
    Field('sessionAnswerID', 'reference SessionAnswer'),
    Field('questionID', 'reference Question'),
    Field('answerText', 'text'))
