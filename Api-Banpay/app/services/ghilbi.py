import requests
from fastapi import HTTPException

GHIBLI_API_URL = "https://ghibliapi.vercel.app"

def get_ghibli_data(resource: str):
    """
    Consume la API de Studio Ghibli para obtener datos según el recurso.
    """
    valid_resources = ["films", "people", "locations", "species", "vehicles"]
    if resource not in valid_resources:
        raise ValueError(f"Invalid resource: {resource}")

    try:
        response = requests.get(f"{GHIBLI_API_URL}/{resource}")
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 200
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error consuming Ghibli API: {str(e)}")