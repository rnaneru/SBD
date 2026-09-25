from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User, Post


engine = create_engine('postgresql://postgres:pwd@localhost:5432/test')
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = session_local()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_user(name:str, age:int, email:str) -> int:
    new_user = User(name=name, age=age, email=email)
    
    with get_db() as db:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print('User created:', new_user.id)
        return new_user.id


def create_post(title:str, content:str, user_id:int) -> int:
    new_post = Post(title=title, content=content, user_id=user_id)
    
    with get_db() as db:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        print(f'Post {new_post.id} created by User {user_id}')
        return new_post.id


def get_user_with_posts(user_id: int) -> User | None:
   
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
       
        if user:
            print(f'User {user.id}, posts: {len(user.posts)}')
            for post in user.posts:
                print('', post.content)
            return user
        else: 
            print(f'User {user_id} not found')
            return None

        
def delete_user_with_posts(user_id: int) -> None:
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            print(f'Deleted user {user_id} with it`s posts')
            return None
        else: 
            print(f'User {user_id} not found')
            return None


def clear_data() -> None:
    with get_db() as db:
        db.query(User).filter(User.email == 'eve@example.com').delete()
        db.commit()


if __name__ == '__main__':

    clear_data()
    user_id = create_user('Eve', 18, 'eve@example.com')
    create_post('1 post', 'Hello', user_id)
    create_post('2 post', 'World', user_id)
    create_post('3 post', '!', user_id)

    get_user_with_posts(user_id)
    delete_user_with_posts(user_id)
    get_user_with_posts(user_id)

