from pprint import pprint
import dateparser
from sqlalchemy import *

# connect to db
engine = create_engine('mysql+mysqlconnector://tools:YPrn3Uy8OX61DQlFjinb'
        '@localhost/cl_scrape')

# create table
metadata = MetaData()
cl_ad = Table('cl_ad', metadata,
        Column('ad_id', Integer, primary_key=True),
        Column('title', String(255), nullable=False),
        Column('description', Text(), nullable=False),
        Column('ad_dtime', DateTime(timezone=True), nullable=False)
)
metadata.create_all(engine)

# list tables
for e in metadata.sorted_tables:
    print(e.name)

ins = cl_ad.insert()
print(str(ins))
dt_string = '2016-12-07T04:48:49-06:00'
title = 'Free puppies'
description = 'Poky puppies a whole bushel full'

dt = dateparser.parse(dt_string,
        settings={'RETURN_AS_TIMEZONE_AWARE': True})
ins = cl_ad.insert().values(title=title, description=description,
        ad_dtime=dt)

pprint(ins.compile().params)
conn = engine.connect()
result = conn.execute(ins)
print('primary key = {}'.format(result.inserted_primary_key))

s = select([cl_ad])
result = conn.execute(s)
for row in result:
    print(row)

