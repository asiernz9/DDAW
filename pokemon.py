import requests
from typing import List, Optional, Dict, Any

def fetch_data(url: str) -> Optional[Dict[str, Any]]:
    """
    Makes a GET request to the provided URL and returns the JSON data.

    Args:
        url (str): The URL to make the request to.

    Returns:
        Optional[Dict[str, Any]]: The JSON data from the response if successful, or None in case of an error.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_water_type_url() -> Optional[str]:
    """
    Retrieves the URL for the "Water" type Pokémon from the PokeAPI.

    Returns:
        Optional[str]: The URL to fetch Water-type Pokémon, or None if not found or error occurs.
    """
    url = 'https://pokeapi.co/api/v2/type/'
    data = fetch_data(url)
    
    if data and isinstance(data, dict):
        for type_info in data.get('results', []):
            if type_info['name'] == 'water':
                return type_info['url']
    return None

def buscar_pokemons_agua() -> List[str]:
    """
    Fetches the list of all Water-type Pokémon by making an API request.

    Returns:
        List[str]: A list of names of Pokémon that are of Water type.
    """
    water_type_url = get_water_type_url()
    
    if water_type_url:
        data = fetch_data(water_type_url)
        
        if data and isinstance(data, dict):
            return [pokemon['pokemon']['name'] for pokemon in data.get('pokemon', [])]
    
    return []

def display_pokemons(pokemons: List[str]) -> None:
    """
    Displays the names of all Water-type Pokémon in a readable format.

    Args:
        pokemons (List[str]): A list of Pokémon names to be displayed.
    """
    if pokemons:
        print(f"The Water-type Pokémon are: {', '.join(pokemons)}.")
    else:
        print("No Water-type Pokémon found.")

if __name__ == "__main__":
    """
    Main function to fetch and display Water-type Pokémon.
    """
    pokemons_agua = buscar_pokemons_agua()
    display_pokemons(pokemons_agua)
