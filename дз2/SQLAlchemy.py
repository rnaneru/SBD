from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text, insert, select, update, delete, exc


# С помощью SQLAlchemy Core создайте подключение к PostgreSQL.

server_engine = create_engine(
    'postgresql://postgres:pwd@localhost:5432/postgres',
    isolation_level='AUTOCOMMIT'
)

with server_engine.connect() as conn:
    exists = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'test'")).first() is not None

    if not exists:
        conn.execute(text('CREATE DATABASE test'))
        print ('Database "test" created')
    else:
        print ('Database "test" already exists')

server_engine.dispose()


engine = create_engine(
    'postgresql://postgres:pwd@localhost:5432/test'
)


# Создание таблицы

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('email', String, unique=True),
    Column('age', Integer)
)

metadata.create_all(engine)


# Реализация CRUD с обработкой ошибок

def create_user(name: str, email: str, age: int) -> int | None:
    insert_query = (insert(users)
                    .values(name=name, age=age, email=email)
                    .returning(users.c.id)
                    )
    try:
        with engine.connect() as connection:
            result = connection.execute(insert_query)
            connection.commit()
            user_id = result.first()[0]
            print(f'created user {user_id}')
            return user_id
    except exc.SQLAlchemyError as error:
        print (f'Error creating user: {error}')
        return None
    except Exception as error:
        print (f'Unknown error: {error}')
        return None


def get_user(user_id: int) -> list | None:
    select_query = (select(users)
                    .where(users.c.id == user_id)
                    )
    result_list = []
    try:
        with engine.connect() as connection:
            result = connection.execute(select_query)
            result_list_raw = result.mappings().first()
            if result_list_raw is None:
                print (f'User {user_id} not found')
                return None
            for row in result_list_raw:
                result_list.append(dict(row))
            print (f'found {len(result_list)} user(s), return first: {result_list[0]}')
            return result_list[0]
    except exc.SQLAlchemyError as error:
        print (f'Error finding user: {error}')
        return None
    except Exception as error:
        print (f'Unknown error: {error}')
        return None


def update_user_email(user_id: int, new_email: str) -> int | None:
    update_query = (update(users)
                    .where(users.c.id == user_id)
                    .values(email=new_email)
                    )
    try:
        with engine.connect() as connection:
            result = connection.execute(update_query)
            connection.commit()
            print (f'updated {result.rowcount} users')
            return result.rowcount
    except exc.SQLAlchemyError as error:
        print (f'Error updating user: {error}')
        return None
    except Exception as error:
        print (f'Unknown error: {error}')
        return None


def delete_user(user_id: int) -> int | None:
    delete_query = (delete(users)
                    .where(users.c.id == user_id)
                    )
    try:
        with engine.connect() as connection:
            result = connection.execute(delete_query)
            connection.commit()
            if result.rowcount:
                print (f'deleted {result.rowcount} users')
            return result.rowcount
    except exc.SQLAlchemyError as error:
        print (f'Error deleting user: {error}')
        return None
    except Exception as error:
        print (f'Unknown error: {error}')
        return None
