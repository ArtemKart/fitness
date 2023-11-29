from sqlalchemy import Column, Integer, String

from api.db.base_class import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String)
    password = Column(String, nullable=False)
