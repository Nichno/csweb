# CSWEB

## Open Source Python-Based Web Interface for Counter-Strike 2 Demo Analysis

**CSWEB** is a Flask-based web application that provides an intuitive interface for analyzing Counter-Strike 2 (CS2) demo files using the powerful [DemoParser2](https://github.com/LaihoE/demoparser) library.

## Features

- 🎮 **Demo File Upload** - Upload `.dem` files directly through the web interface
- 📊 **Comprehensive Statistics** - Analyze personal kill/death ratios, headshots, MVP count, and utility damage
- 👥 **Team Analysis** - View team compositions and player statistics
- 📈 **Kill Tracking** - Detailed kill logs with weapon information and map locations
- 💾 **Match Management** - Store and manage multiple demo files
- 🔄 **Easy Re-analysis** - Quickly re-analyze previously uploaded matches

## Technology Stack

- **Backend**: Python Flask
- **Data Processing**: Pandas
- **Demo Parsing**: [DemoParser2](https://github.com/LaihoE/demoparser)
- **Frontend**: HTML/CSS (templates)

## Project Structure

```
csweb/
├── app.py           # Main Flask application
├── analyzer.py      # Demo parsing and analysis logic
├── templates/       # HTML templates for web interface
├── matches/         # Directory for uploaded demo files
└── README.md        # This file
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Nichno/csweb.git
   cd csweb
   ```

2. Install dependencies:
   ```bash
   pip install flask pandas demoparser2
   ```

3. Run the application:
   ```bash
   python app.py
   ```

The application will start on `http://localhost:5001`

## Usage

1. Open your browser and navigate to `http://localhost:5001`
2. Upload a Counter-Strike 2 demo file (`.dem` format)
3. The application will automatically parse and analyze the demo
4. View detailed statistics including:
   - Personal stats (kills, deaths, headshots, MVPs, utility damage)
   - Team rosters
   - Complete kill log with weapon information
   - Map locations for kills and deaths

## Routes

- `/` - Main page with match list and current statistics
- `/upload` - Upload new demo files
- `/matches` - View all available matches
- `/analyze/<filename>` - Analyze a specific demo file
- `/download/<filename>` - Download a demo file
- `/<match_id>` - Dynamic match analysis page

## Configuration

- **Upload Folder**: `matches/` (default)
- **Allowed Extensions**: `.dem` files only
- **Port**: 5001 (configurable in `app.py`)
- **Debug Mode**: Enabled by default (change in production)

## How It Works

1. **Upload**: Users upload a Counter-Strike 2 demo file through the web interface
2. **Parse**: DemoParser2 extracts match data including:
   - Player statistics (kills, deaths, MVPs, utility damage)
   - Team information
   - Death events with kill details
3. **Analyze**: The analyzer processes this data and calculates personalized stats
4. **Display**: Results are rendered on the web interface for easy viewing

## Notes

- The application stores your Steam ID in `analyzer.py` for personalized statistics
- Demo files are stored in the `matches/` directory after upload
- The application runs with `debug=True` by default for development

## License

Open source project without a specific license.

## Contributing

Feel free to open issues or submit pull requests to improve CSWEB!