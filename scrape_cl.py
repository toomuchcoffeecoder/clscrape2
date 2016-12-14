from pprint import pprint

from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, DateTime

from cl_scrape2 import CLScrape
from settings import connection_str

engine = create_engine(connection_str)

metadata = MetaData()
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
metadata.create_all(engine)


if __name__ == '__main__':
    conn = engine.connect()
    ins = cl_ad.insert()
    scraper = CLScrape('computer gigs')
    pprint(scraper.sections)
    for site in scraper.get_sites('US'):
        # if site['city'] != 'san francisco bay area': continue
        pprint(site)
        for e in scraper.parse_ads(scraper.get_ads(site)):
            print(e)
            try:
                # if link_key is allready present pass
                conn.execute(ins, state=e['state'], city=e['city'],
                        title=e['title'], description=e['description'], 
                        link=e['link'], link_key=e['link_key'],
                        date_str=e['date_str'], dt=e['dt'])
            except exc.IntegrityError:
                pass

