from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column (Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    age = Column(Integer)

    posts = relationship(
        'Post', back_populates='author', cascade='all, delete-orphan'
        )


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column (Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, unique=True)

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    author = relationship(
        'User', back_populates='posts'
    )

