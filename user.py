from sqlalchemy import Column, Integer, String, true

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=true)
    image_url = Column(String)
    nickname = Column(String)