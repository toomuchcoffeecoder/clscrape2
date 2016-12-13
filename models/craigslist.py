from sqlalchemy import Table, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import mapper

from database import metadata, db_session


class ClAd(object):
    db_session.query_property()

    def __init__(self, ad_id, state, city, title,
                description, link, link_key,
                date_str, dt):
        self.ad_id = ad_id
        self.state = state
        self.city = city
        self.title = title
        self.description = description
        self.link = link
        self.link_key = link_key
        self.date_str = date_str
        self.dt = dt


cl_ad = Table('cl_ad', metadata,
        Column('ad_id', Integer, primary_key=True),
        Column('state', String(64)),
        Column('city', String(64)),
        Column('title', String(255)),
        Column('description', Text()),
        Column('link', String(255)),
        Column('link_key', String(25), primary_key=True),
        Column('date_str', String(128)),
        Column('dt', DateTime(timezone=True))
)

mapper(ClAd, cl_ad)


