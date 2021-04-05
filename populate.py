from logging import exception
import requests as req

from core.database import SessionLocal
from core.schemas.PokemonData import PokemonData

""" Script to populate "pokemon_data" table on database with data from PokeAPI """


res = req.get("https://pokeapi.co/api/v2/pokemon?limit=151")
if res.status_code != 200:
    print("Failed to request from PokeAPI: status", res.status_code)

res = res.json()
pokemons = res["results"]

db = SessionLocal()

for pokemon in pokemons:
    poke_res = req.get(pokemon['url'])
    if poke_res.status_code != 200:
        print(f"Failed to request {pokemon['name'].capitalize()} data from PokeAPI: status", poke_res.status_code)
        break

    poke_info = poke_res.json()
    poke_species_res = req.get(f"https://pokeapi.co/api/v2/pokemon-species/{poke_info['id']}")
    if poke_res.status_code != 200:
        print(f"Failed to request {pokemon['name'].capitalize()}({poke_info['id']}) data from PokeAPI: status", poke_res.status_code)
        break
    poke_species = poke_species_res.json()
    

    pk_data = {
        "id": poke_info['id'],
        "name": pokemon['name'].capitalize(),
        "types": [
            poke_info['types'][0]['type']['name'].capitalize()
        ],
        "description": poke_species["flavor_text_entries"][0]["flavor_text"],
        "weight": poke_info['weight'],
        "sprite": poke_info['sprites']['front_default']
    }
    try:
        pk_data["types"].append(poke_info['types'][1]['type']['name'].capitalize())
    except:
        pass

    try:
        db_pkdata = PokemonData(**pk_data)
        db.add(db_pkdata)
        db.commit()
        db.refresh(db_pkdata)
        if db_pkdata is None:
            raise exception
    except:
        print(f"Failed to insert {pk_data['name']} data on database. [{exception}] Stoping...")
        break

    if pk_data['id'] < 151:
        print(f" {pk_data['id']}/151", end='\r', flush=True)
    else:
        print(f" {pk_data['id']}/151")
