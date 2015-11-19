from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
reddit__user = Table('reddit__user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('access_token', String(length=255)),
    Column('refresh_token', String(length=255)),
    Column('last_refresh', DateTime),
    Column('user_id', Integer),
)

imgur__user = Table('imgur__user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('access_token', String(length=255)),
    Column('refresh_token', String(length=255)),
    Column('last_refresh', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['reddit__user'].columns['username'].create()
    post_meta.tables['imgur__user'].columns['username'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['reddit__user'].columns['username'].drop()
    post_meta.tables['imgur__user'].columns['username'].drop()
