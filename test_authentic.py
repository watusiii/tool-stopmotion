#!/usr/bin/env python3
"""
Quick test to verify the authentic stop motion processing works
"""

import cv2
import numpy as np
import os
from video_processor import StopMotionVideoProcessor

def create_simple_test_video(filename="test_smooth.mp4", fps=30, duration=3):
    """Create a smooth test video to convert to stop motion."""
    
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
    
    total_frames = int(fps * duration)
    
    for i in range(total_frames):
        # Create smooth motion - bouncing ball
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:, :] = [20, 30, 50]  # Dark blue background
        
        # Smooth bouncing ball animation
        t = i / total_frames
        x = int(width/2 + 200 * np.sin(t * 4 * np.pi))
        y = int(height/2 + 150 * np.cos(t * 6 * np.pi))
        
        cv2.circle(frame, (x, y), 25, (100, 200, 255), -1)
        
        # Frame number
        cv2.putText(frame, f"Frame {i+1}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        out.write(frame)
    
    out.release()
    print(f"✅ Created smooth test video: {filename}")
    return filename

def test_both_methods():
    """Test both classic and authentic stop motion processing."""
    
    print("🎬 Testing Stop Motion Processing Methods")
    print("=" * 50)
    
    # Create test video
    test_input = create_simple_test_video("test_smooth_input.mp4", fps=30, duration=2)
    
    processor = StopMotionVideoProcessor()
    
    try:
        # Get original info
        info = processor.get_video_info(test_input)
        print(f"\nOriginal video: {info['fps']} fps, {info['frame_count']} frames, {info['duration']:.1f}s")
        
        # Test 1: Classic method
        print("\n1. Testing Classic Method (frame reduction)...")
        result_classic = processor.reduce_frames(
            test_input,
            "test_output_classic.mp4",
            frame_reduction_factor=3,
            quality="high"
        )
        print(f"   Classic: {result_classic['original_fps']:.1f} → {result_classic['new_fps']:.1f} fps")
        print(f"   Duration: {result_classic['original_duration']:.1f}s → {result_classic['new_duration']:.1f}s")
        print(f"   Frames: {result_classic['original_frames']} → {result_classic['kept_frames']}")
        
        # Test 2: Authentic method
        print("\n2. Testing Authentic Method (held frames)...")
        result_authentic = processor.reduce_frames_authentic(
            test_input,
            "test_output_authentic.mp4",
            frame_reduction_factor=3,
            quality="high",
            maintain_duration=True
        )
        print(f"   Authentic: {result_authentic['original_fps']:.1f} fps output at {result_authentic['output_fps']:.1f} fps")
        print(f"   Effective: {result_authentic['new_fps']:.1f} fps (unique frames)")
        print(f"   Duration: {result_authentic['original_duration']:.1f}s → {result_authentic['new_duration']:.1f}s")
        print(f"   Frames: {result_authentic['original_frames']} → {result_authentic['kept_frames']} unique → {result_authentic['output_frames']} total")
        
        print("\n✅ Both methods tested successfully!")
        
        print("\n📊 Results Comparison:")
        print(f"   Classic creates shorter, faster video ({result_classic['new_duration']:.1f}s)")
        print(f"   Authentic maintains duration ({result_authentic['new_duration']:.1f}s) with proper frame timing")
        print(f"   Authentic should feel more like real stop motion!")
        
        print("\nGenerated test files:")
        for filename in ["test_smooth_input.mp4", "test_output_classic.mp4", "test_output_authentic.mp4"]:
            if os.path.exists(filename):
                size = os.path.getsize(filename) / (1024 * 1024)
                print(f"   {filename}: {size:.2f} MB")
        
        print("\n🎉 Test complete! Try playing both output files to see the difference.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_both_methods()