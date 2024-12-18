import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from inky.auto import auto
from bs4 import BeautifulSoup
import re

# Initialize the Inky display
inky_display = auto()
inky_display.set_border(inky_display.BLACK)

# Constants for the Inky 5.7" display
DISPLAY_WIDTH = 600
DISPLAY_HEIGHT = 448
RANDOM_IMAGE_URL = "https://commons.wikimedia.org/wiki/Special:Random/File"

# User-Agent for Wikimedia compliance
HEADERS = {
    "User-Agent": "InkyDisplayScript/1.0 (https://myinkyproject.com; contact@myinkyproject.com)"
}

def get_random_image_info():
    """Fetch a random image URL and description by following the Wikimedia Random File redirect."""
    print("Fetching a random image URL...")
    response = requests.get(RANDOM_IMAGE_URL, headers=HEADERS, allow_redirects=True)
    response.raise_for_status()

    # The final URL after the redirect contains the image details
    page_url = response.url
    print(f"Redirected to file page: {page_url}")
    
    # Extract the image URL and description from the page source
    response = requests.get(page_url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the image URL
    image_tag = soup.find("a", {"class": "internal"})
    if not image_tag or "href" not in image_tag.attrs:
        raise ValueError("Could not find the image URL on the page.")
    
    image_url = image_tag["href"]
    if not image_url.startswith("http"):
        image_url = "https:" + image_url  # Handle relative links

    # Extract the description from the "Summary" section
    description_tag = soup.find("div", {"class": "description"})
    description = description_tag.get_text(strip=True) if description_tag else "No description available."

    # Remove common language prefixes like "English:"
    description = re.sub(r"^\w+:\s*", "", description)

    print(f"Found image URL: {image_url}")
    print(f"Extracted description: {description}")
    return image_url, description

def download_image(url):
    """Download an image from the given URL."""
    print(f"Downloading image from URL: {url}")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return Image.open(BytesIO(response.content))

def crop_to_fit(image):
    """Crop the image to exactly fit the display size while maintaining aspect ratio."""
    print("Cropping image to fit the display dimensions...")
    image = image.convert("RGB")  # Ensure compatibility with the Inky display
    
    # Calculate the aspect ratio of the target display
    target_ratio = DISPLAY_WIDTH / DISPLAY_HEIGHT
    img_width, img_height = image.size
    img_ratio = img_width / img_height

    if img_ratio > target_ratio:
        # Image is wider than the target; crop the width
        new_width = int(target_ratio * img_height)
        offset = (img_width - new_width) // 2
        image = image.crop((offset, 0, offset + new_width, img_height))
    else:
        # Image is taller than the target; crop the height
        new_height = int(img_width / target_ratio)
        offset = (img_height - new_height) // 2
        image = image.crop((0, offset, img_width, offset + new_height))

    # Resize cropped image to target dimensions
    image = image.resize((DISPLAY_WIDTH, DISPLAY_HEIGHT), Image.Resampling.LANCZOS)
    return image

def overlay_text(image, text):
    """Overlay description text on the image with dynamic box size and 5% opacity."""
    print("Overlaying text with dynamic box size and low opacity...")
    draw = ImageDraw.Draw(image)

    # Load a font; fallback to a default size if font file is unavailable
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 18)
    except IOError:
        font = ImageFont.load_default()

    # Define the text area dimensions
    padding = 10

    # Truncate the text to fit within one line
    words = text.split()
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        text_width = draw.textlength(test_line, font=font)
        if text_width <= DISPLAY_WIDTH - 2 * padding:
            line = test_line
        else:
            break  # Stop adding words when the line is full

    # Measure the text box dimensions
    bbox = draw.textbbox((0, 0), line, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Calculate the position to center the text horizontally
    text_x = (DISPLAY_WIDTH - text_width) // 2
    text_y = DISPLAY_HEIGHT - text_height - padding

    # Draw a semi-transparent background matching the text height (5% opacity)
    draw.rectangle(
        [(text_x - padding, text_y - padding), (text_x + text_width + padding, text_y + text_height + padding)],
        fill=(0, 0, 0, int(255 * 0.05))  # 5% opacity black
    )

    # Draw the text centered horizontally
    draw.text((text_x, text_y), line, fill="white", font=font)
    return image

def display_image(image):
    """Display the image on the Inky display."""
    print("Displaying the image on the Inky display...")
    inky_display.set_image(image)
    inky_display.show()
    print("Image displayed successfully.")

def main():
    """Main function to fetch, process, and display a random high-res image."""
    try:
        print("Starting the script...")
        image_url, description = get_random_image_info()
        image = download_image(image_url)
        cropped_image = crop_to_fit(image)
        image_with_text = overlay_text(cropped_image, description)
        display_image(image_with_text)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
