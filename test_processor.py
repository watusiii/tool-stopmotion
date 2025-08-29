#!/usr/bin/env python3
"""
Test script for the Stop Motion Video Processor
"""

import cv2
import numpy as np
import os
from video_processor import StopMotionVideoProcessor

def create_test_video(filename="test_video.mp4", duration=3, fps=30):
    """Create a simple test video for processing."""
    
    # Video properties
    width, height = 640, 480
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    total_frames = int(fps * duration)
    
    for i in range(total_frames):
        # Create a frame with moving circle
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Background color changes over time
        bg_color = int(50 + 50 * np.sin(i * 0.1))
        frame[:, :] = [bg_color, bg_color//2, bg_color//3]
        
        # Moving circle
        x = int(width/2 + 200 * np.sin(i * 0.05))
        y = int(height/2 + 100 * np.cos(i * 0.05))
        
        cv2.circle(frame, (x, y), 30, (255, 255, 255), -1)
        
        # Frame counter text
        cv2.putText(frame, f"Frame {i+1}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print(f"✅ Created test video: {filename}")
    return filename

def test_video_processor():
    """Test the video processor functionality."""
    
    print("🎬 Testing Stop Motion Video Processor")
    print("=" * 50)
    
    # Create test video
    test_input = create_test_video("test_input.mp4", duration=2, fps=24)
    
    # Initialize processor
    processor = StopMotionVideoProcessor()
    
    try:
        # Test 1: Get video info
        print("\n1. Testing video info...")
        info = processor.get_video_info(test_input)
        print(f"   Original: {info['fps']} fps, {info['frame_count']} frames")
        print(f"   Duration: {info['duration']:.1f}s")
        print(f"   Resolution: {info['width']}x{info['height']}")
        
        # Test 2: Custom reduction
        print("\n2. Testing custom frame reduction (every 2nd frame)...")
        result1 = processor.reduce_frames(
            test_input, 
            "test_output_custom.mp4", 
            frame_reduction_factor=2,
            quality="high"
        )
        print(f"   Reduced: {result1['original_fps']} → {result1['new_fps']} fps")
        print(f"   Frames: {result1['original_frames']} → {result1['kept_frames']}")
        
        # Test 3: Preset - shooting on twos
        print("\n3. Testing 'shooting on twos' preset...")
        result2 = processor.create_stop_motion_preset(
            test_input,
            "test_output_twos.mp4",
            "twos"
        )
        print(f"   Reduced: {result2['original_fps']} → {result2['new_fps']} fps")
        print(f"   Frames: {result2['original_frames']} → {result2['kept_frames']}")
        
        # Test 4: Preset - shooting on threes
        print("\n4. Testing 'shooting on threes' preset...")
        result3 = processor.create_stop_motion_preset(
            test_input,
            "test_output_threes.mp4", 
            "threes"
        )
        print(f"   Reduced: {result3['original_fps']} → {result3['new_fps']} fps")
        print(f"   Frames: {result3['original_frames']} → {result3['kept_frames']}")
        
        print("\n✅ All tests passed!")
        print("\nGenerated files:")
        for filename in ["test_input.mp4", "test_output_custom.mp4", 
                        "test_output_twos.mp4", "test_output_threes.mp4"]:
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"   {filename}: {size:,} bytes")
        
        print("\n🎉 Video processor is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup test files (optional)
        cleanup = input("\nClean up test files? (y/N): ").lower().strip()
        if cleanup == 'y':
            for filename in ["test_input.mp4", "test_output_custom.mp4", 
                            "test_output_twos.mp4", "test_output_threes.mp4"]:
                try:
                    if os.path.exists(filename):
                        os.remove(filename)
                        print(f"Removed {filename}")
                except:
                    pass

if __name__ == "__main__":
    # Check if opencv is working
    try:
        import cv2
        print(f"OpenCV version: {cv2.__version__}")
    except ImportError as e:
        print(f"❌ OpenCV not available: {e}")
        print("Please install with: pip install opencv-python")
        exit(1)
    
    test_video_processor()