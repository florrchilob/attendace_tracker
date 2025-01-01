from sqlalchemy import Table, Column, Identity
from sqlalchemy.sql.sqltypes import String, Boolean, BigInteger, DateTime
from config.db import meta, engine

attendees = Table("attendees", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("mispar_ishi", String(255), unique=True),
                    Column("tehudat_zehut", String(10), unique=True),
                    Column("full_name", String(255)),
                    Column("arrived", Boolean),
                    Column("date_arrived", DateTime)
                )

def create():
    meta.create_all(engine)

