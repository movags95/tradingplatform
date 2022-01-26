import create_tables_db, insert_strategies

create_tables_db.drop_tables()
create_tables_db.create_tables()
insert_strategies.insert_strategies()