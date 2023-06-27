import webbrowser
import requests

# URL del servidor FastAPI
SERVER_URL = "http://192.168.0.24:8080"

# Archivo HTML para el formulario
HTML_FILE_PATH = "form.html"

# Cargar el archivo HTML del formulario
def load_html_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


# Ejecutar la solicitud al servidor FastAPI
def execute_api_request(method):
    if method == "pokemon":
        pokemon_id = input("Escribe el ID de un Pokemon: ")
        response = requests.get(f"{SERVER_URL}/pokemon/{pokemon_id}")
        pokemon_info = response.json()
        image_path = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokemon_id}.png"
        html = generate_html_response(pokemon_info, image_path)
        with open("pokemon.html", "w") as html_file:
            html_file.write(html)
        print("Página HTML generada correctamente.")
        webbrowser.open("pokemon.html")
    elif method == "tipos":
        response = requests.get(f"{SERVER_URL}/plot")
        print("Plot generated.")
    elif method == "top5":
        response = requests.get(f"{SERVER_URL}/strongest")
        strongest_pokemon = response.json()

        # Obtener los 5 primeros Pokémon más fuertes
        top5_pokemon = strongest_pokemon[:5]

        # Generar el HTML del top 5 de Pokémon
        html = generate_top5_html_response(top5_pokemon)

        with open("top5.html", "w") as html_file:
            html_file.write(html)

        print("Página HTML generada para el top 5 de Pokémon más fuertes.")
        webbrowser.open("top5.html")

        
    elif method == "put":
        pokemon_id = input("Escribe el ID de un Pokemon: ")
        updated_name = input("Nuevo nombre para el Pokemon: ")

        # Crear un diccionario con los datos actualizados del Pokémon
        updated_data = {"updated_name": updated_name}

        response = requests.put(f"{SERVER_URL}/put/{pokemon_id}", json=updated_data)

        if response.status_code == 200:
            print("Pokémon updated successfully.")
        else:
            print("Failed to update Pokémon.")
    else:
        print("Invalid method.")

# Generar la respuesta HTML con la información del Pokémon
def generate_html_response(pokemon_info: dict, image_path: str) -> str:
    css_styles = """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f0f0;
        background-image: url('https://images5.alphacoders.com/109/1092473.png');
        background-size: cover;
        background-position: center;
        text-align: center;
        margin-top: 50px;
    }

    .pokemon-card {
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
        padding: 30px;
        background-color: #fff;
        max-width: 500px;
        margin: 0 auto;
    }

    h1 {
        font-size: 36px;
        color: #333;
        margin-bottom: 10px;
    }

    p {
        font-size: 18px;
        color: #666;
        margin: 5px;
    }

    .pokemon-image {
        width: 200px;
        height: auto;
        margin-top: 20px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
    }
    </style>
    """

    # Formatear el tipo del Pokémon sin corchetes y comillas
    pokemon_type = ", ".join(pokemon_info['type'])

    # Obtener las estadísticas del Pokémon
    stats = pokemon_info['stats']

    # Obtener las evoluciones del Pokémon
    evolutions = pokemon_info['evolution']

    html_response = f"""
    <html>
    <head>
        <title>{pokemon_info['name']} - Pokedex</title>
        {css_styles}
    </head>
    <body>
        <div class="pokemon-card">
            <h1>{pokemon_info['name']}</h1>
            <p>ID Pokedex: {pokemon_info['id']}</p>
            <p>Tipo: {pokemon_type}</p>
            <p>Altura: {pokemon_info['height']}</p>
            <p>Peso: {pokemon_info['weight']}</p>
            <p>Habilidades: {', '.join(pokemon_info['abilities'])}</p>
            <p>Estadísticas:</p>
            <ul>
                <li>HP: {stats['hp']}</li>
                <li>Ataque: {stats['attack']}</li>
                <li>Defensa: {stats['defense']}</li>
                <li>Ataque especial: {stats['sp.atk']}</li>
                <li>Defensa especial: {stats['sp.def']}</li>
                <li>Velocidad: {stats['speed']}</li>
                <li>Total: {stats['total']}</li>
            </ul>
            <p>Evoluciones: {', '.join(evolutions)}</p>
            <p>Descripción: {pokemon_info['description']}</p>
            <img src="{image_path}" class="pokemon-image">
        </div>
    </body>
    </html>
    """

    return html_response

# Generar la respuesta HTML para el top 5 de Pokémon
def generate_top5_html_response(pokemon_list):
    css_styles = """
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f0f0f0;
        background-image: url('https://images5.alphacoders.com/109/1092473.png');
        background-size: cover;
        background-position: center;
        text-align: center;
        margin-top: 50px;
    }

    .pokemon-card {
        display: inline-block;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
        padding: 30px;
        background-color: #fff;
        max-width: 500px;
        margin: 0 auto;
    }

    h1 {
        font-size: 36px;
        color: #333;
        margin-bottom: 10px;
    }

    p {
        font-size: 18px;
        color: #666;
        margin: 5px;
    }

    .pokemon-image {
        width: 200px;
        height: auto;
        margin-top: 20px;
        box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.3);
    }
    </style>
    """

    pokemon_cards = ""
    for i, pokemon in enumerate(pokemon_list, start=1):
        image_path = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{pokemon['id']}.png"
        pokemon_card = f"""
        <div class="pokemon-card">
            <h1>{pokemon['name']}</h1>
            <img src="{image_path}" class="pokemon-image">
            <p>Puesto: {i}</p>
        </div>
        """
        pokemon_cards += pokemon_card

    html_response = f"""
    <html>
    <head>
        <title>Top 5 Pokémon más fuertes - Pokedex</title>
        {css_styles}
    </head>
    <body>
        <h1>Top 5 Pokémon más fuertes</h1>
        {pokemon_cards}
    </body>
    </html>
    """

    return html_response



if __name__ == "__main__":
    method = input("Nombre del Metodo a utilizar: \n -pokemon (Muestra estadisticas de un Pokemon) \n -top5 (Muestra los 5 Pokemons mas fuertes) \n -tipos (Grafico de los tipos con mas Pokemons) \n -put (Modifica el Nombre de un Pokemon) \n Metodo: ")
    execute_api_request(method)
