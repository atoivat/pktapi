from core.database import Base, engine

from core.schemas import Pokemon, PokemonData, Trainer

Base.metadata.create_all(bind=engine)