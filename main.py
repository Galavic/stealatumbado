import requests
import datetime
import time

# CONFIGURACIÓN
API_KEY = "TU_API_KEY_DE_ROBLOX"  
UNIVERSE_ID = TU_UNIVERSE_ID   # Número
GAME_NAME_BASE = "Mi Evento Épico"  

# Diccionario de imágenes para cada estado
IMAGES = {
    "day6": "day6.png",
    "day5": "day5.png",
    "day4": "day4.png",
    "day3": "day3.png",
    "day2": "day2.png",
    "day1": "day1.png",
    "1h": "1h.png",
    "30m": "30m.png",
    "15m": "15m.png",
    "now": "now.png"
}

# Fecha del evento
EVENT_DATETIME = datetime.datetime(2025, 10, 1, 18, 0, 0)  # Ejemplo: 1 oct 2025 6:00 PM

# Función para subir portada y cambiar nombre
def update_game(title, image_path):
    headers = {
        "x-api-key": API_KEY
    }

    # Subir imagen como icono del juego
    with open(image_path, "rb") as f:
        files = {"fileContent": f}
        response = requests.post(
            f"https://apis.roblox.com/universes/v1/{UNIVERSE_ID}/icons",
            headers=headers,
            files=files
        )

    if response.status_code != 200:
        print("Error al subir imagen:", response.text)
    else:
        print("Imagen actualizada")

    # Cambiar nombre del juego
    data = {
        "name": title,
        "description": f"Cuenta regresiva para el evento: {title}"
    }
    response = requests.patch(
        f"https://apis.roblox.com/universes/v1/{UNIVERSE_ID}",
        headers=headers,
        json=data
    )

    if response.status_code != 200:
        print("Error al cambiar nombre:", response.text)
    else:
        print("Nombre actualizado a:", title)


# Lógica de cuenta regresiva
def check_event():
    while True:
        now = datetime.datetime.utcnow()
        diff = EVENT_DATETIME - now

        if diff.days > 0:
            # Mostrar "día X"
            key = f"day{diff.days}" if diff.days <= 6 else None
            if key in IMAGES:
                update_game(f"{GAME_NAME_BASE} - Faltan {diff.days} días", IMAGES[key])

        elif diff.total_seconds() > 0:
            minutes = diff.total_seconds() / 60

            if minutes <= 60 and minutes > 30:
                update_game(f"{GAME_NAME_BASE} - Falta 1 hora", IMAGES["1h"])
            elif minutes <= 30 and minutes > 15:
                update_game(f"{GAME_NAME_BASE} - Falta 30 min", IMAGES["30m"])
            elif minutes <= 15:
                update_game(f"{GAME_NAME_BASE} - Falta 15 min", IMAGES["15m"])

        else:
            # Evento en curso
            update_game(f"{GAME_NAME_BASE} - ¡AHORA!", IMAGES["now"])
            break

        time.sleep(300)  # Checar cada 5 minutos


if __name__ == "__main__":
    check_event()
