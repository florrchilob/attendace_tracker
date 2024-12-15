from sqlalchemy import Table, Column, Identity, ForeignKey
from sqlalchemy.sql.sqltypes import String, Boolean, BigInteger
from config.db import meta, engine

attendees = Table("attendees", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("mispar_hishi", BigInteger),
                    Column("full_name", String),
                    Column("arrived", Boolean)
                )

def create():
    meta.create_all(engine)

