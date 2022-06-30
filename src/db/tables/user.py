from sqlalchemy import Boolean, Column, Integer, String
from src.db import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primart_key=True, index=True, unique=True, autoincrement=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)