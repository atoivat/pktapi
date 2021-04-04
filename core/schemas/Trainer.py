from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from core.database import Base

class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)


    team = relationship("Pokemon", back_populates="trainer")