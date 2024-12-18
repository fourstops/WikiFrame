# WikiFrame

![WikiFrame Logo](./WikiFrame_Logo.png)

WikiFrame is a dynamic e-paper display project that showcases randomly selected high-resolution images from Wikimedia Commons. Designed for the Pimoroni Inky 5.7" e-paper display, WikiFrame fetches a new image every 15 minutes, displays it beautifully, and overlays a short, centered description for added context. 

## Features
- **Random Image Display**: Fetches high-resolution images from Wikimedia Commons' `Special:Random/File`.
- **Automatic Updates**: Refreshes every 15 minutes with a new image and description.
- **Dynamic Font Sizing**: Automatically adjusts text size to ensure the description fits within the display.
- **Subtle Overlay**: Displays a semi-transparent background (5% opacity) for the text, ensuring readability without obstructing the image.
- **Monochrome Optimization**: Tailored for the Pimoroni Inky 5.7" display, making the most of its e-paper capabilities.

## How It Works
1. **Image Fetching**: WikiFrame fetches a random file from Wikimedia Commons using the `Special:Random/File` URL.
2. **Description Extraction**: Extracts and processes the "Summary" section from the image page, removing unnecessary prefixes like "English:".
3. **Image Processing**: Crops and resizes the image to fit the Inky 5.7" display (600x448 pixels) without distortion.
4. **Display**: Renders the image and overlays the description text dynamically.

## Hardware Requirements
- Raspberry Pi (any model with SPI support)
- Pimoroni Inky 5.7" e-paper display
- MicroSD card with Raspberry Pi OS
- Internet connection for fetching images and descriptions

## Software Requirements
- Python 3.7 or later
- Required Python libraries:
  - `inky`
  - `requests`
  - `pillow`
  - `beautifulsoup4`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/WikiFrame.git
   cd WikiFrame
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure SPI is enabled on your Raspberry Pi:
   ```bash
   sudo raspi-config
   ```
   - Navigate to **Interface Options** > **SPI** > **Enable**.

5. Test the script:
   ```bash
   python3 wiki_frame.py
   ```

## Automating with Cron
To run WikiFrame every 15 minutes:
1. Edit the crontab:
   ```bash
   crontab -e
   ```

2. Add the following line:
   ```bash
   */15 * * * * /bin/bash /path/to/run_inky_display.sh >> /path/to/wiki_frame.log 2>&1
   ```

## Project Structure
```
WikiFrame/
├── wiki_frame.py         # Main Python script
├── run_inky_display.sh   # Bash script for running the Python script
├── requirements.txt      # Required Python libraries
├── WikiFrame_Logo.png    # Project logo
└── README.md             # Project documentation
```

## Contributing
Contributions are welcome! If you’d like to add features or fix issues:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request explaining your changes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Future Improvements
- Add multi-language support for extracting and displaying descriptions.
- Implement caching to prevent re-fetching the same image multiple times.
- Support for different e-paper display sizes and configurations.
