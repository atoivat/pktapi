from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String)
    level = Column(Integer)
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    data_id = Column(Integer, ForeignKey("pokemon_data.id"))

    trainer = relationship("Trainer", back_populates="team")

    data = relationship("PokemonData")