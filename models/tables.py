from sqlalchemy import Table, Column, Identity, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, BigInteger, Integer
from config.db import meta, engine

attendees = Table("attendees", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("mispar_ishi", Integer, unique=True),
                    Column("tehudat_zehut", Integer, unique=True),
                    Column("full_name", String(255)),
                    Column("arrived", Boolean)
                )

def create():
    meta.create_all(engine)

