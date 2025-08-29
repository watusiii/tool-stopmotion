# Stop Motion Video Processor

A Python-based video processing tool designed specifically for claymation and stop-motion animation. Reduces video frame rates using industry-standard techniques.

## Features

- **Frame Rate Reduction**: Convert videos to classic stop-motion frame rates
- **Stop Motion Presets**: 
  - Shooting on Twos (12fps) - Most common for claymation
  - Shooting on Threes (8fps) - Stylized animation
  - Shooting on Fours (6fps) - Highly stylized
- **Custom Reduction**: Choose any frame reduction factor (2-10x)
- **Quality Control**: High, medium, or low compression options
- **Clean Interface**: Modern shadcn-inspired UI with dark theme
- **Real-time Processing**: Web-based interface with progress tracking

## Stop Motion Context

### Frame Rate Standards
- **Shooting on Ones (24fps)**: Every frame is unique, smoothest animation but most time-intensive. Used in feature films.
- **Shooting on Twos (12fps)**: Each frame shown twice. Perfect balance of smoothness and production time. Most common for claymation.
- **Shooting on Threes (8fps)**: More stylized look, faster to produce. Good for budget productions or artistic effect.

### Supported Formats
- MP4, AVI, MOV, MKV input
- MP4 output optimized for stop motion

## Installation

1. **Clone or download this repository**
2. **Run setup script**:
   ```bash
   python setup.py
   ```

### Manual Installation

If the setup script doesn't work, install manually:

```bash
pip install -r requirements.txt
```

Requirements:
- Python 3.8+
- OpenCV (opencv-python)
- FastAPI
- Uvicorn
- Additional dependencies in requirements.txt

## Usage

1. **Start the application**:
   ```bash
   python app.py
   ```

2. **Open your browser** to: `http://localhost:8000`

3. **Upload your video** and choose settings:
   - Select a stop motion preset or use custom reduction
   - Choose output quality
   - Click "Process Video"

4. **Download** your processed video

## API Endpoints

- `GET /` - Main web interface
- `POST /process` - Process video with parameters
- `GET /download/{filename}` - Download processed video
- `GET /info` - Get stop motion information and presets

## Technical Details

### Frame Reduction Algorithm
The processor reduces frames by keeping every Nth frame based on the reduction factor:
- Factor 2: Keep every 2nd frame (24fps → 12fps)
- Factor 3: Keep every 3rd frame (24fps → 8fps)
- Factor 4: Keep every 4th frame (24fps → 6fps)

### Quality Settings
- **High**: Minimal compression (95% quality) - Best for claymation detail
- **Medium**: Balanced compression (85% quality)
- **Low**: Higher compression (70% quality) - Smaller file sizes

## File Structure

```
tool-stopmotion/
├── app.py                 # FastAPI web server
├── video_processor.py     # Core video processing logic
├── requirements.txt       # Python dependencies
├── setup.py              # Setup script
├── templates/
│   └── index.html        # Web interface
├── uploads/              # Temporary upload storage
└── outputs/              # Processed video output
```

## Examples

### CLI Usage (Direct)
```python
from video_processor import StopMotionVideoProcessor

processor = StopMotionVideoProcessor()

# Convert to "shooting on twos" (12fps)
results = processor.create_stop_motion_preset(
    "input.mp4", 
    "output.mp4", 
    "twos"
)

print(f"Reduced from {results['original_fps']} to {results['new_fps']} fps")
```

### Web Interface
1. Upload your MP4 file
2. Select "Shooting on Twos" preset
3. Choose "High" quality
4. Process and download

## Troubleshooting

### Common Issues

**OpenCV not found**:
```bash
pip install opencv-python
```

**Permission errors**:
Make sure the uploads/ and outputs/ directories are writable.

**Large file processing**:
For very large files, processing may take several minutes. The web interface shows progress.

### Performance Tips
- Use "Medium" or "Low" quality for faster processing
- Higher reduction factors process faster
- Close other applications when processing large files

## Credits

Created for claymation and stop-motion artists. Interface inspired by shadcn/ui design principles.

## License

Open source - feel free to modify and distribute.