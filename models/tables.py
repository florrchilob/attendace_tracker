from sqlalchemy import Table, Column, Identity, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Date, Boolean, Time, BigInteger, DateTime
from config.db import meta, engine

meetings = Table("meetings", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("sub_account_id", BigInteger, ForeignKey("sub_accounts.id")),
                    Column("day", Date),
                    Column("since", Time),
                    Column("until", Time),
                    Column("people_amount", Integer),
                    Column("confirmed", Boolean),
                    Column("licensed_now", Boolean),
                    Column("license_id", BigInteger, ForeignKey("admin_accounts_x_licenses.id")),
                    Column("admin_account_id", BigInteger, ForeignKey("admin_accounts.id")),
                )

sub_accounts = Table("sub_accounts", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("mail", String(255), unique=True),
                    Column("password", String(255)),
                    Column("name", String(255)),
                    Column("mispar_ishi", BigInteger, unique=True),
                    Column("telephone", Integer),
                    Column("account_type", Integer),
                    Column("validated", Boolean),
                    Column("authorized", Boolean),
                    Column("token", String(255)),
                    Column("refresh_token", String(255)),
                    Column("token_expiration", DateTime)
                )

admin_accounts = Table("admin_accounts", meta,
                        Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                        Column("name", String(255)),
                        Column("account_id", String(255)),
                        Column("client_id", String(255)),
                        Column("client_secret", String(255))
                    )

licenses = Table ("licenses", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("zooms_name", Integer),
                    Column("amount_people", Integer),
                )


admin_accounts_x_licenses = Table ("admin_accounts_x_licenses", meta,
                    Column("id", BigInteger, Identity(start=1, cycle=True), primary_key=True),
                    Column("license_id", BigInteger, ForeignKey("licenses.id")),
                    Column("admin_account_id", BigInteger, ForeignKey("admin_accounts.id")),
                    Column("amount_licenses", Integer)
                )

def create():
    meta.create_all(engine)

