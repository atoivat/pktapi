import requests as req

from core.database import SessionLocal
from core.schemas.PokemonData import PokemonData
from core.models.PokemonData import get_pkdata_by_id

""" Script to populate "pokemon_data" table on database with data from PokeAPI """


res = req.get("https://pokeapi.co/api/v2/pokemon?limit=151")
if res.status_code != 200:
    print("Failed to request from PokeAPI: status", res.status_code)

res = res.json()
pokemons = res["results"]

db = SessionLocal()

for pokemon in pokemons:
    # Request pokemon info
    poke_res = req.get(pokemon['url'])
    if poke_res.status_code != 200:
        print(f"Failed to request {pokemon['name'].capitalize()} data from PokeAPI: status", poke_res.status_code)
        break
    poke_info = poke_res.json()

    if get_pkdata_by_id(db, poke_info['id']) is not None:
        # Pokemon already registred
        continue

    # Request pokemon species info
    poke_species_res = req.get(f"https://pokeapi.co/api/v2/pokemon-species/{poke_info['id']}")
    if poke_res.status_code != 200:
        print(f"Failed to request {pokemon['name'].capitalize()}({poke_info['id']}) data from PokeAPI: status", poke_res.status_code)
        break
    poke_species = poke_species_res.json()
    
    # Handle pokemon species description language and special characters
    description = None
    for flavor_txt_entry in poke_species["flavor_text_entries"]:
        if flavor_txt_entry["language"]["name"] == "en":
            description = flavor_txt_entry["flavor_text"]\
                .replace("\n", " ")\
                .replace("\u000c", " ")
            break
    
    if description is None:
        print(f"Failed to fetch {pokemon['name'].capitalize()}({poke_info['id']}) description in english from PokeAPI")
    
    # Format data
    pk_data = {
        "id": poke_info['id'],
        "name": pokemon['name'].capitalize(),
        "types": [
            poke_info['types'][0]['type']['name'].capitalize()
        ],
        "description": description,
        "weight": poke_info['weight'],
        "sprite": poke_info['sprites']['front_default']
    }
    try:
        pk_data["types"].append(poke_info['types'][1]['type']['name'].capitalize())
    except:
        pass

    # Save in DB
    try:
        db_pkdata = PokemonData(**pk_data)
        db.add(db_pkdata)
        db.commit()
        db.refresh(db_pkdata)
        if db_pkdata is None:
            raise Exception
    except Exception as e:
        print(f"Failed to insert {pk_data['name']} data on database. [{e}]\nSkiping...")
        db.rollback()
        continue

    # Print status
    if pk_data['id'] < 151:
        print(f" {pk_data['id']}/151", end='\r', flush=True)
    else:
        print(f" {pk_data['id']}/151")
