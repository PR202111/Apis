from .database import Base
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey
from sqlalchemy.orm import Relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
class Post(Base):
    __tablename__ = "post"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,server_default="TRUE",nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)

    owner = Relationship("User")



class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key=True)