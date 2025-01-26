import configparser
import os
import requests
import time
from PIL import Image

# Load configuration
CONFIG_PATH = "config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

# Configuration settings
DEBUG_PATH = config["settings"]["debug_path"]
IMAGE_PATH = config["settings"]["image_path"]
SCRIPT_PATH = config["settings"]["script_path"]
DEVICE_ADDRESS = config["settings"]["device_address"]
FRAME_DURATION = int(config["settings"]["frame_duration"])
UPDATE_INTERVAL = int(config["settings"]["update_interval"])
LATITUDE = config["settings"]["latitude"]
LONGITUDE = config["settings"]["longitude"]
TIMEZONE = config["settings"]["timezone"]
API_URL = config["weather"]["api_url"]

# Ensure debug directory exists
os.makedirs(DEBUG_PATH, exist_ok=True)

# Weather code images for day and night
DAY_IMAGES = {
    0: "sun.png",               # Clear sky
    1: "cloud_sun.png",         # Partly cloudy (day)
    2: "cloud.png",             # Cloudy
    3: "overcast.png",          # Overcast
    45: "cloud_wind.png",       # Fog
    48: "cloud_wind.png",       # Freezing fog
    51: "rain0.png",            # Drizzle
    61: "rain1.png",            # Light rain
    63: "rain2.png",            # Moderate rain
    65: "rain2.png",            # Heavy rain
    71: "snow.png",             # Snow
    95: "lightning.png",        # Thunderstorm
}

NIGHT_IMAGES = {
    0: "moon.png",              # Clear sky (night)
    1: "cloud_moon.png",        # Partly cloudy (night)
    61: "rain_moon.png",        # Light rain (night)
}

def fetch_weather():
    """Fetch weather data from the API."""
    url = API_URL.format(latitude=LATITUDE, longitude=LONGITUDE, timezone=TIMEZONE)
    print(f"Fetching weather data from: {url}")
    response = requests.get(url)
    data = response.json()

    try:
        current_weather = data["current_weather"]
        weather_code = current_weather["weathercode"]
        temperature = int(current_weather["temperature"])
        is_day = bool(current_weather["is_day"])
        return weather_code, temperature, is_day
    except KeyError as e:
        print(f"Error parsing weather data: {e}")
        print(f"API Response: {data}")
        raise

def get_colour_for_temperature(temperature):
    """Get a colour based on the temperature."""
    if temperature <= 0:
        return (255, 255, 255, 255)  # White for freezing or below
    elif 1 <= temperature <= 5:
        return (0, 0, 204, 255)  # Dark Blue
    elif 6 <= temperature <= 10:
        return (51, 51, 255, 255)  # Medium Blue
    elif 11 <= temperature <= 15:
        return (102, 153, 255, 255)  # Light Blue
    elif 16 <= temperature <= 19:
        return (153, 204, 255, 255)  # Sky Blue
    elif 20 <= temperature <= 29:
        return (255, 204, 153, 255)  # Light Orange
    elif 30 <= temperature <= 39:
        return (255, 165, 0, 255)  # Orange
    elif 40 <= temperature <= 50:
        return (255, 69, 0, 255)  # Bright Red
    else:
        return (153, 0, 0, 255)  # Dark Red for extreme heat

def render_text_frame(text, colour, canvas_size=(16, 16)):
    """Manually render text as pixel data with colour coding, centered horizontally."""
    print(f"Rendering text: {text} with colour {colour}")
    frame = Image.new("RGBA", canvas_size, (0, 0, 0, 255))  # Black background
    pixels = frame.load()

    # Define digits and symbols
    digits = {
        "0": [
            "0110",
            "1001",
            "1001",
            "1001",
            "1001",
            "1001",
            "0110",
            "0000",
        ],
        "1": [
            "0010",
            "0110",
            "0010",
            "0010",
            "0010",
            "0010",
            "0111",
            "0000",
        ],
        "2": [
            "0110",
            "1001",
            "0001",
            "0010",
            "0100",
            "1000",
            "1111",
            "0000",
        ],
        "3": [
            "0110",
            "1001",
            "0001",
            "0110",
            "0001",
            "1001",
            "0110",
            "0000",
        ],
        "4": [
            "0001",
            "0011",
            "0101",
            "1001",
            "1111",
            "0001",
            "0001",
            "0000",
        ],
        "5": [
            "1111",
            "1000",
            "1110",
            "0001",
            "0001",
            "1001",
            "0110",
            "0000",
        ],
        "6": [
            "0110",
            "1000",
            "1000",
            "1110",
            "1001",
            "1001",
            "0110",
            "0000",
        ],
        "7": [
            "1111",
            "0001",
            "0010",
            "0100",
            "1000",
            "1000",
            "1000",
            "0000",
        ],
        "8": [
            "0110",
            "1001",
            "1001",
            "0110",
            "1001",
            "1001",
            "0110",
            "0000",
        ],
        "9": [
            "0110",
            "1001",
            "1001",
            "0111",
            "0001",
            "0001",
            "0110",
            "0000",
        ],
        "-": [
            "0000",
            "0000",
            "0000",
            "1111",
            "0000",
            "0000",
            "0000",
            "0000",
        ],
    }

    # Calculate total text width
    char_width = 4  # Each character is 4 pixels wide
    spacing = 1     # 1 pixel spacing between characters
    total_width = len(text) * char_width + (len(text) - 1) * spacing

    # Adjust initial x_offset for centering
    x_offset = (canvas_size[0] - total_width) // 2

    # Render each character
    for char in text:
        if char in digits:
            digit = digits[char]
            for y, row in enumerate(digit):
                for x, bit in enumerate(row):
                    if bit == "1":
                        # Place pixel with the given colour
                        pixels[x + x_offset, y + 4] = colour
            x_offset += char_width + spacing  # Shift to the next character

    # Save for debugging
    frame_path = os.path.join(DEBUG_PATH, f"debug_render_text_{text}.png")
    frame.save(frame_path)
    print(f"Rendered text frame saved as: {frame_path}")

    return frame
    
def generate_frames(weather_code, temperature, is_day):
    """Generate frames for the weather display."""
    images = DAY_IMAGES if is_day else NIGHT_IMAGES
    icon_file = images.get(weather_code, "unknown.png")
    icon_path = os.path.join(IMAGE_PATH, icon_file)

    if os.path.exists(icon_path):
        icon_frame = Image.open(icon_path).resize((16, 16))
        icon_frame.save(os.path.join(DEBUG_PATH, "debug_icon_frame.png"))
        print(f"Icon frame saved as ./debug/debug_icon_frame.png")
    else:
        icon_frame = Image.new("RGBA", (16, 16), (0, 0, 0, 255))  # Fallback black frame

    colour = get_colour_for_temperature(temperature)
    temperature_frame = render_text_frame(str(temperature), colour)

    gif_path = os.path.join(DEBUG_PATH, "weather_display.gif")
    icon_frame.save(
        gif_path,
        save_all=True,
        append_images=[temperature_frame],
        duration=FRAME_DURATION,
        loop=0,
    )
    print(f"Saved GIF to {gif_path}")
    return gif_path

def send_to_display(gif_path):
    """Send the generated GIF to the display."""
    cmd = f"{SCRIPT_PATH} --address {DEVICE_ADDRESS} --set-gif {gif_path} --process-gif 16"
    print(f"Executing: {cmd}")
    os.system(cmd)

def main():
    """Main execution loop."""
    print("Starting weather display script...")
    while True:
        try:
            weather_code, temperature, is_day = fetch_weather()
            gif_path = generate_frames(weather_code, temperature, is_day)
            send_to_display(gif_path)
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f"Sleeping for {UPDATE_INTERVAL} seconds...")
        time.sleep(UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
