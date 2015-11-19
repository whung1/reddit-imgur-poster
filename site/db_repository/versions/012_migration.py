from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
reddit__user = Table('reddit__user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('access_token', VARCHAR(length=255)),
    Column('refresh_token', VARCHAR(length=255)),
    Column('last_refresh', DATETIME),
    Column('user_id', INTEGER),
    Column('username', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['reddit__user'].columns['last_refresh'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['reddit__user'].columns['last_refresh'].create()
