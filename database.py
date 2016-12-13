from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+mysqlconnector://tools:YPrn3Uy8OX61DQlFjinb'
        '@localhost/cl_scrape')
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                        autoflush=False,
                                        bind=engine))

def init_db();
    metadata.create_all(bind=engine)
