# Stop Motion Studio

A professional video processing tool designed specifically for claymation and stop-motion animation. Transform smooth CG videos into authentic stop-motion with frame-precise timing control.

## ✨ Features

### 🎬 Professional Timeline Editor
- **Full-width timeline interface** - Like CapCut, After Effects, or DaVinci Resolve
- **Large video preview window** - See exactly what you're editing
- **Frame-by-frame control** - Click any frame to select and adjust timing
- **Visual playhead marker** - Track your position in the timeline
- **Transport controls** - Play, pause, skip with variable speed (0.1x - 2.0x)

### 🎯 Authentic Stop Motion Processing
- **True frame holding** - Maintains original duration with proper timing
- **Frame enhancement** - Sharpens and enhances contrast for crisp stop-motion look
- **Smart timing algorithms** - Creates authentic stop-motion feel, not "laggy video"

### ⚡ Two Processing Modes
1. **Quick Process** - Fast processing with standard presets
2. **Timeline Editor** - Professional frame-by-frame control

### 🎭 Stop Motion Presets
- **Shooting on Twos (12fps)** - Classic claymation standard (Wallace & Gromit style)
- **Shooting on Threes (8fps)** - Stylized animation for artistic projects
- **Shooting on Fours (6fps)** - Highly stylized, dreamlike quality
- **Custom timing** - Set any frame duration from 1-20 frames

### 📁 File Support
- **Input**: MP4, AVI, MOV, MKV
- **Output**: Optimized MP4 for stop-motion playback
- **Quality options**: Cinema, Balanced, Web-optimized

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   python setup.py
   ```
   Or manually: `pip install -r requirements.txt`

2. **Start the application**:
   ```bash
   python app.py
   ```

3. **Open your browser**: `http://localhost:8000`

4. **Choose your workflow**:
   - **Quick Process**: Upload → Select preset → Download
   - **Timeline Editor**: Upload → Frame-by-frame editing → Export

## 🎨 Timeline Editor Workflow

### Getting Started
1. Upload your video (drag & drop supported)
2. Select **"Timeline Editor"** mode
3. Click "Process Video" to extract frames

### Professional Editing Interface
- **Video Preview**: Large preview window shows selected frame in real-time
- **Horizontal Timeline**: Frames displayed like professional video editors
- **Frame Selection**: Click any frame to select and preview
- **Hold Duration**: Adjust how long each frame is held (1-20 frames)
- **Include/Exclude**: Toggle frames on/off for final export
- **Transport Controls**: Play through your timing to preview results

### Frame Timing Guide
- **1-2 frames**: Fast action (punches, quick movements)
- **2-3 frames**: Normal movement (walking, gestures) 
- **4-6 frames**: Slow, careful motion (dramatic moments)
- **6+ frames**: Dramatic pauses, reaction shots

### Professional Controls
- **Quick Presets**: Fast, Normal, Slow, Hold buttons
- **Playback Speed**: 0.1x - 2.0x for detailed timing review
- **Visual Feedback**: Frame width represents hold duration
- **Playhead Marker**: Red line shows current timeline position

## 🔧 Technical Details

### Authentic Stop Motion Algorithm
Our "Authentic Stop Motion" mode creates proper stop-motion timing by:
1. **Selecting key frames** based on motion analysis
2. **Holding each frame** for the specified duration
3. **Maintaining original video length** with proper frame timing
4. **Enhancing frame clarity** with contrast and sharpness adjustments

This creates the distinctive "posed" look of real claymation, not just frame-dropped video.

### Architecture
```
tool-stopmotion/
├── app.py                    # FastAPI web server
├── video_processor.py        # Core video processing 
├── frame_extractor.py        # Frame extraction & thumbnails
├── templates/
│   ├── index.html           # Main interface
│   └── timeline_editor.html # Professional timeline editor
├── uploads/                 # Temporary video storage
└── outputs/                # Processed video output
```

### API Endpoints
- `GET /` - Main web interface
- `GET /timeline-editor` - Professional timeline editor
- `POST /extract-frames` - Extract frames for timeline editing
- `POST /process` - Standard video processing
- `POST /render-custom-timeline` - Render with custom timing
- `GET /download/{filename}` - Download processed videos

## 📱 User Interface

### Modern Design
- **Professional video editor layout** - Familiar to users of CapCut, After Effects
- **Clean Lucide icons** - No emojis, professional iconography
- **Responsive timeline** - Scrollable horizontal frame track
- **Real-time preview** - Immediate feedback on timing changes

### Accessibility
- **Drag & drop uploads** - Intuitive file handling
- **Visual frame duration** - Frame width shows timing
- **Keyboard shortcuts** - Professional editing workflow
- **Progress tracking** - Clear feedback during processing

## 🎯 Stop Motion Context

### Why This Tool Exists
Converting smooth CG animation to authentic stop-motion requires more than just removing frames. Real stop-motion has:
- **Distinctive timing** - Each pose is held for specific durations
- **Frame clarity** - No motion blur, sharp details
- **Artistic pacing** - Fast actions use fewer frames, slow actions use more

### Professional Use Cases
- **CG to Claymation**: Convert Blender renders to authentic stop-motion feel
- **Video Stylization**: Give live-action footage a stop-motion aesthetic  
- **Animation Timing**: Study and adjust frame timing for stop-motion projects
- **Educational**: Learn stop-motion principles through hands-on editing

## 🛠 Installation & Setup

### Requirements
- **Python 3.8+**
- **Modern web browser** (Chrome, Firefox, Safari, Edge)
- **2GB+ RAM** for video processing
- **Fast storage** for temporary video files

### Dependencies
All dependencies are automatically installed via `setup.py`:
- OpenCV (video processing)
- FastAPI (web framework)  
- Uvicorn (web server)
- Aiofiles (async file handling)
- NumPy (frame manipulation)

### Windows Quick Start
1. Download or clone this repository
2. Double-click `install.bat` to install dependencies
3. Double-click `run.bat` to start the application
4. Open browser to `http://localhost:8000`

## 🎬 Examples

### Converting CG Animation
```python
# Direct API usage
from video_processor import StopMotionVideoProcessor

processor = StopMotionVideoProcessor()

# Convert smooth 30fps CG to authentic 12fps stop-motion
results = processor.reduce_frames_authentic(
    "smooth_cg_animation.mp4",
    "stop_motion_output.mp4", 
    frame_reduction_factor=3,
    maintain_duration=True  # Keep original timing with held frames
)

print(f"Created authentic stop-motion: {results['new_fps']} fps effective")
```

### Web Interface Workflow
1. **Upload**: Drag your CG video into the interface
2. **Select Mode**: Choose "Timeline Editor" for full control
3. **Edit Timing**: 
   - Fast sword swing → 1-2 frame holds
   - Character walking → 2-3 frame holds  
   - Reaction shots → 6+ frame holds
4. **Preview**: Use transport controls to review timing
5. **Export**: Download your authentic stop-motion video

## 🔍 Troubleshooting

### Common Issues

**"White text on white background"**
- Fixed in latest version with proper contrast

**"Video preview too small"**  
- Updated: Preview now fills full window size

**"Can't see timeline position"**
- Added: Red playhead marker shows current position

**NumPy compatibility errors**:
```bash
pip install "numpy<2.0.0" --force-reinstall
pip install opencv-python
```

**File not processing**:
- Check file format (MP4, AVI, MOV, MKV supported)
- Ensure sufficient disk space for temporary files
- Try lower quality setting for large files

### Performance Tips
- **Use Timeline Editor** for best results vs. Quick Process
- **Cinema quality** for final renders, Web quality for previews  
- **Close other applications** when processing large videos
- **SSD storage** recommended for faster frame extraction

## 🎨 Design Philosophy

Built for **claymation artists** and **stop-motion creators** who need:
- **Professional tools** without professional price tags
- **Authentic stop-motion feel** from CG source material
- **Frame-precise control** over timing and pacing
- **Familiar interface** like industry-standard video editors

## 📄 License

Open source - modify and distribute freely. Created for the stop-motion animation community.

---

*Transform your smooth CG animations into authentic claymation masterpieces with professional timeline control.*