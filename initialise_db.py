import db.create_db as create_db

create_db.drop_tables()
create_db.create_tables()
create_db.insert_strategies()