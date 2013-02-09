db = DAL("sqlite://db.sqlite", lazy_tables=True)

db.define_table('polls',
    Field('title'))

db.define_table('pollChoices',
    Field('pid', 'reference polls'),
    Field('content'))

db.define_table('userChose',
    Field('cid', 'reference pollChoices'))
