from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import aiofiles
import os
import uuid
from pathlib import Path
from video_processor import StopMotionVideoProcessor
from frame_extractor import FrameExtractor, TimelineProcessor

app = FastAPI(title="Stop Motion Video Processor", version="1.0.0")

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

processor = StopMotionVideoProcessor()
extractor = FrameExtractor()
timeline_processor = TimelineProcessor()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML interface."""
    try:
        async with aiofiles.open("templates/index.html", mode='r', encoding='utf-8') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Stop Motion Processor</title></head>
        <body>
            <h1>Stop Motion Video Processor</h1>
            <p>Templates not found. Please check setup.</p>
        </body>
        </html>
        """)

@app.get("/timeline-editor", response_class=HTMLResponse)
async def timeline_editor():
    """Serve the timeline editor interface."""
    try:
        async with aiofiles.open("templates/timeline_editor.html", mode='r', encoding='utf-8') as f:
            content = await f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Timeline editor not found")

@app.post("/process")
async def process_video(
    file: UploadFile = File(...),
    reduction_factor: int = Form(2),
    preset: str = Form("custom"),
    quality: str = Form("high"),
    processing_method: str = Form("authentic")
):
    """Process uploaded video with frame reduction."""
    
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported video format")
    
    # Generate unique filenames
    file_id = str(uuid.uuid4())
    input_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    output_filename = f"{file_id}_processed.mp4"
    output_path = OUTPUT_DIR / output_filename
    
    try:
        # Save uploaded file
        async with aiofiles.open(input_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Get video info
        video_info = processor.get_video_info(str(input_path))
        
        # Process video based on preset or custom reduction
        if preset != "custom":
            results = processor.create_stop_motion_preset(
                str(input_path), 
                str(output_path), 
                preset
            )
        else:
            # Choose processing method based on user selection
            if processing_method == "authentic":
                results = processor.reduce_frames_authentic(
                    str(input_path),
                    str(output_path),
                    reduction_factor,
                    quality,
                    maintain_duration=True
                )
            else:
                # Classic method (frame reduction)
                results = processor.reduce_frames(
                    str(input_path),
                    str(output_path),
                    reduction_factor,
                    quality
                )
        
        # Clean up input file
        os.remove(input_path)
        
        # Return processing results
        return {
            "success": True,
            "download_url": f"/download/{output_filename}",
            "results": results,
            "original_info": video_info
        }
        
    except Exception as e:
        # Clean up files on error
        if input_path.exists():
            os.remove(input_path)
        if output_path.exists():
            os.remove(output_path)
        
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download processed video file."""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='video/mp4'
    )

@app.get("/info")
async def get_info():
    """Get information about stop motion frame rates and techniques."""
    return {
        "stop_motion_info": {
            "shooting_on_ones": {
                "description": "24fps - every frame is unique, super smooth but time-intensive",
                "typical_use": "Feature films, high-budget productions"
            },
            "shooting_on_twos": {
                "description": "12fps effective - each frame shown twice, good balance",
                "typical_use": "Most claymation and stop motion work"
            },
            "shooting_on_threes": {
                "description": "8fps effective - more stylized, quicker to produce",
                "typical_use": "Stylized animation, budget productions"
            }
        },
        "presets": {
            "twos": "Reduces to 'shooting on twos' - 12fps effective rate",
            "threes": "Reduces to 'shooting on threes' - 8fps effective rate", 
            "fours": "Reduces to 'shooting on fours' - 6fps effective rate"
        },
        "supported_formats": [".mp4", ".avi", ".mov", ".mkv"]
    }

@app.post("/extract-frames")
async def extract_frames_for_timeline(
    file: UploadFile = File(...),
    reduction_factor: int = Form(3)
):
    """Extract frames for timeline editing."""
    
    if not file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        raise HTTPException(status_code=400, detail="Unsupported video format")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    input_path = UPLOAD_DIR / f"{file_id}_{file.filename}"
    
    try:
        # Save uploaded file
        async with aiofiles.open(input_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Extract frames with thumbnails
        result = extractor.extract_frames_with_metadata(
            str(input_path), 
            reduction_factor
        )
        
        # Add file reference for later processing
        result['file_id'] = file_id
        result['original_filename'] = file.filename
        
        return result
        
    except Exception as e:
        # Clean up on error
        if input_path.exists():
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/render-custom-timeline")
async def render_custom_timeline(
    file_id: str = Form(...),
    timeline_data: str = Form(...)  # JSON string of timeline config
):
    """Render video with custom timeline timing."""
    
    try:
        # Parse timeline data
        import json
        timeline_config = json.loads(timeline_data)
        
        # Find original file
        input_files = list(UPLOAD_DIR.glob(f"{file_id}_*"))
        if not input_files:
            raise HTTPException(status_code=404, detail="Original file not found")
        
        input_path = input_files[0]
        output_filename = f"{file_id}_custom_timeline.mp4"
        output_path = OUTPUT_DIR / output_filename
        
        # Render with custom timing
        results = timeline_processor.render_custom_timing(
            str(input_path),
            timeline_config,
            str(output_path),
            quality='high'
        )
        
        # Clean up input file
        os.remove(input_path)
        
        return {
            "success": True,
            "download_url": f"/download/{output_filename}",
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)