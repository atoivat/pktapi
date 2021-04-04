from sqlalchemy import Column, Integer, ARRAY, String, String
from core.database import Base


class PokemonData(Base):
    __tablename__ = "pokemon_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    types = Column(ARRAY(String))
    description = Column(String)
    weight = Column(Integer)
    sprite = Column(String)