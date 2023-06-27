from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json
import matplotlib.pyplot as plt

app = FastAPI()

# Ruta al archivo JSON
JSON_FILE_PATH = "pokemon_full.json"

# Cargar datos del archivo JSON
def load_pokemon_data():
    with open(JSON_FILE_PATH, "r") as json_file:
        return json.load(json_file)

def save_pokemon_data(data):
    with open(JSON_FILE_PATH, "w") as json_file:
        json.dump(data, json_file, indent=4)

pokemon_data = load_pokemon_data()

@app.get("/pokemon/{pokemon_id}")
def get_pokemon(pokemon_id: int):
    # Obtener la información del Pokémon del archivo JSON
    pokemon_info = pokemon_data[pokemon_id - 1]

    # Obtener la ruta de la imagen del Pokémon
    image_path = get_image_path(pokemon_id)

    # Agregar la ruta de la imagen al diccionario de información del Pokémon
    pokemon_info["image_path"] = image_path

    # Devolver la información del Pokémon como respuesta JSON
    return JSONResponse(content=pokemon_info, status_code=200)

@app.put("/put/{pokemon_id}")
def update_pokemon_name(pokemon_id: int, updated_data: dict):
    updated_name = updated_data.get("updated_name")
    # Verificar si el ID del Pokémon es válido
    if pokemon_id < 1 or pokemon_id > len(pokemon_data):
        raise HTTPException(status_code=404, detail="El ID del Pokémon no es válido")

    # Actualizar el nombre del Pokémon en la lista de datos en memoria
    pokemon_data[pokemon_id - 1]["name"] = updated_name

    # Guardar los datos actualizados en el archivo JSON
    save_pokemon_data(pokemon_data)

    # Obtener la información actualizada del Pokémon
    updated_pokemon_info = pokemon_data[pokemon_id - 1]

    # Obtener la ruta de la imagen del Pokémon
    image_path = get_image_path(pokemon_id)

    # Agregar la ruta de la imagen al diccionario de información del Pokémon
    updated_pokemon_info["image_path"] = image_path

    # Devolver la información actualizada del Pokémon como respuesta JSON
    return JSONResponse(content=updated_pokemon_info, status_code=200)

@app.get("/plot")
def plot_pokemon_types():
    # Contar la cantidad de Pokémon por tipo
    type_counts = {}
    for pokemon in pokemon_data:
        pokemon_types = pokemon["type"]
        for pokemon_type in pokemon_types:
            if pokemon_type in type_counts:
                type_counts[pokemon_type] += 1
            else:
                type_counts[pokemon_type] = 1

    # Generar el gráfico de barras
    types = list(type_counts.keys())
    counts = list(type_counts.values())

    plt.bar(types, counts)
    plt.xlabel("Tipo de Pokémon")
    plt.ylabel("Cantidad")
    plt.title("Cantidad de Pokémon por Tipo")
    plt.tick_params(axis='x', rotation=90)
    plt.show()

@app.get("/strongest")
def get_strongest_pokemon():
    # Ordenar los Pokémon por su estadística de ataque (attack) en orden descendente
    sorted_pokemon = sorted(pokemon_data, key=lambda p: p["stats"]["attack"], reverse=True)

    # Obtener los 5 Pokémon más fuertes
    strongest_pokemon = sorted_pokemon[:5]

    # Devolver los 5 Pokémon más fuertes como respuesta JSON
    return JSONResponse(content=strongest_pokemon, status_code=200)

def get_image_path(pokemon_id: int) -> str:
    pokemon_id_str = str(pokemon_id).zfill(3)
    return f'{pokemon_id_str}.png'


