import cv2
import os
import numpy as np
from typing import Tuple, Optional
from pathlib import Path


class StopMotionVideoProcessor:
    """
    A video processor designed for stop motion and claymation work.
    Reduces frame rate by keeping every Nth frame to achieve desired frame reduction.
    
    Stop motion context:
    - "Shooting on ones": 24fps (every frame is unique)
    - "Shooting on twos": 12fps effective (each frame shown twice at 24fps)
    - Common claymation rates: 12fps, 15fps, 24fps
    """
    
    def __init__(self):
        self.supported_formats = ['.mp4', '.avi', '.mov', '.mkv']
    
    def get_video_info(self, input_path: str) -> dict:
        """Get information about the input video."""
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video file: {input_path}")
        
        info = {
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
        }
        cap.release()
        return info
    
    def calculate_frame_skip(self, original_fps: float, target_fps: float) -> int:
        """
        Calculate how many frames to skip to achieve target fps.
        For stop motion, common reductions:
        - 24fps -> 12fps: keep every 2nd frame
        - 30fps -> 15fps: keep every 2nd frame  
        - 24fps -> 8fps: keep every 3rd frame
        """
        if target_fps >= original_fps:
            return 1  # No frame skipping needed
        
        skip_factor = int(original_fps / target_fps)
        return max(1, skip_factor)
    
    def enhance_frame_for_stop_motion(self, frame: np.ndarray, enhance_contrast: bool = True) -> np.ndarray:
        """
        Enhance a frame to look more like authentic stop motion.
        
        Args:
            frame: Input frame
            enhance_contrast: Whether to enhance contrast for crisp stop motion look
            
        Returns:
            Enhanced frame
        """
        if enhance_contrast:
            # Convert to LAB color space for better contrast adjustment
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            
            # Merge channels and convert back
            enhanced = cv2.merge([l, a, b])
            frame = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return frame
    
    def reduce_frames(
        self, 
        input_path: str, 
        output_path: str, 
        frame_reduction_factor: int = 2,
        quality: str = 'high'
    ) -> dict:
        """
        Reduce video frames by keeping every Nth frame.
        
        Args:
            input_path: Path to input MP4 file
            output_path: Path to output MP4 file
            frame_reduction_factor: Keep every Nth frame (2 = every 2nd frame, 3 = every 3rd, etc.)
            quality: 'high', 'medium', or 'low' compression quality
            
        Returns:
            Dictionary with processing results
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Get video info
        video_info = self.get_video_info(input_path)
        original_fps = video_info['fps']
        new_fps = original_fps / frame_reduction_factor
        
        # Open input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {input_path}")
        
        # Set up output video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Quality settings for stop motion work
        quality_settings = {
            'high': 95,    # Minimal compression for claymation detail
            'medium': 85,  # Balanced compression
            'low': 70      # Higher compression
        }
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        out = cv2.VideoWriter(
            output_path, 
            fourcc, 
            new_fps,  # Use reduced frame rate
            (video_info['width'], video_info['height'])
        )
        
        frame_count = 0
        kept_frames = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Keep every Nth frame based on reduction factor
                if frame_count % frame_reduction_factor == 0:
                    # Enhance frame for stop motion feel
                    enhanced_frame = self.enhance_frame_for_stop_motion(frame)
                    out.write(enhanced_frame)
                    kept_frames += 1
                
                frame_count += 1
                
                # Progress indicator for long videos
                if frame_count % 100 == 0:
                    progress = (frame_count / video_info['frame_count']) * 100
                    print(f"Processing: {progress:.1f}% complete")
        
        finally:
            cap.release()
            out.release()
        
        # Calculate results
        original_duration = video_info['duration']
        new_duration = kept_frames / new_fps
        
        results = {
            'success': True,
            'original_fps': original_fps,
            'new_fps': new_fps,
            'original_frames': video_info['frame_count'],
            'kept_frames': kept_frames,
            'reduction_factor': frame_reduction_factor,
            'original_duration': original_duration,
            'new_duration': new_duration,
            'file_size_original': os.path.getsize(input_path),
            'file_size_new': os.path.getsize(output_path),
            'compression_ratio': os.path.getsize(output_path) / os.path.getsize(input_path)
        }
        
        return results
    
    def create_stop_motion_preset(self, input_path: str, output_path: str, preset: str = 'twos') -> dict:
        """
        Apply common stop motion frame rate presets.
        
        Presets:
        - 'twos': Convert to 12fps (shooting on twos)
        - 'threes': Convert to 8fps (shooting on threes) 
        - 'fours': Convert to 6fps (shooting on fours)
        """
        video_info = self.get_video_info(input_path)
        original_fps = video_info['fps']
        
        preset_mapping = {
            'twos': 2,     # 24fps -> 12fps, 30fps -> 15fps
            'threes': 3,   # 24fps -> 8fps, 30fps -> 10fps  
            'fours': 4     # 24fps -> 6fps, 30fps -> 7.5fps
        }
        
        if preset not in preset_mapping:
            raise ValueError(f"Unknown preset: {preset}. Available: {list(preset_mapping.keys())}")
        
        reduction_factor = preset_mapping[preset]
        return self.reduce_frames_authentic(input_path, output_path, reduction_factor, quality='high')
    
    def reduce_frames_authentic(
        self,
        input_path: str,
        output_path: str,
        frame_reduction_factor: int = 2,
        quality: str = 'high',
        maintain_duration: bool = True
    ) -> dict:
        """
        Create authentic stop motion by maintaining original frame rate but duplicating frames.
        This creates proper stop motion timing rather than just a "laggy video" effect.
        
        Args:
            input_path: Path to input video file
            output_path: Path to output video file  
            frame_reduction_factor: How many times to duplicate each selected frame
            quality: Output quality setting
            maintain_duration: If True, maintains original video duration by duplicating frames
                              If False, reduces duration like standard frame reduction
        
        Returns:
            Dictionary with processing results
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Get video info
        video_info = self.get_video_info(input_path)
        original_fps = video_info['fps']
        
        # For authentic stop motion, we keep the original frame rate
        # but duplicate selected frames to create the stop motion effect
        if maintain_duration:
            output_fps = original_fps  # Keep original frame rate
        else:
            output_fps = original_fps / frame_reduction_factor  # Reduce frame rate
        
        # Open input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {input_path}")
        
        # Set up output video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # Create output directory if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        out = cv2.VideoWriter(
            output_path,
            fourcc,
            output_fps,
            (video_info['width'], video_info['height'])
        )
        
        frame_count = 0
        output_frame_count = 0
        selected_frames = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Select every Nth frame for stop motion effect
                if frame_count % frame_reduction_factor == 0:
                    # Enhance frame for stop motion feel
                    enhanced_frame = self.enhance_frame_for_stop_motion(frame)
                    selected_frames += 1
                    
                    if maintain_duration:
                        # Write the same frame multiple times to maintain duration
                        # This creates the authentic stop motion "held frame" effect
                        for _ in range(frame_reduction_factor):
                            out.write(enhanced_frame)
                            output_frame_count += 1
                    else:
                        # Just write once for reduced duration
                        out.write(enhanced_frame)
                        output_frame_count += 1
                
                frame_count += 1
                
                # Progress indicator
                if frame_count % 100 == 0:
                    progress = (frame_count / video_info['frame_count']) * 100
                    print(f"Creating stop motion: {progress:.1f}% complete")
        
        finally:
            cap.release()
            out.release()
        
        # Calculate results
        original_duration = video_info['duration']
        if maintain_duration:
            new_duration = original_duration  # Duration stays the same
            effective_fps = selected_frames / new_duration  # Effective frame rate
        else:
            new_duration = output_frame_count / output_fps
            effective_fps = output_fps
        
        results = {
            'success': True,
            'original_fps': original_fps,
            'new_fps': effective_fps,
            'output_fps': output_fps,
            'original_frames': video_info['frame_count'],
            'kept_frames': selected_frames,
            'output_frames': output_frame_count,
            'reduction_factor': frame_reduction_factor,
            'original_duration': original_duration,
            'new_duration': new_duration,
            'maintain_duration': maintain_duration,
            'file_size_original': os.path.getsize(input_path),
            'file_size_new': os.path.getsize(output_path),
            'compression_ratio': os.path.getsize(output_path) / os.path.getsize(input_path),
            'processing_method': 'authentic_stop_motion'
        }
        
        return results


def main():
    """Example usage of the StopMotionVideoProcessor."""
    processor = StopMotionVideoProcessor()
    
    # Example: Convert video to "shooting on twos" (12fps effective)
    input_file = "input_video.mp4"
    output_file = "output_stopmotion.mp4"
    
    try:
        # Get video information first
        info = processor.get_video_info(input_file)
        print(f"Original video: {info['fps']} fps, {info['frame_count']} frames")
        
        # Apply stop motion preset
        results = processor.create_stop_motion_preset(input_file, output_file, 'twos')
        
        print(f"Processing complete!")
        print(f"Reduced from {results['original_fps']} to {results['new_fps']} fps")
        print(f"Kept {results['kept_frames']} of {results['original_frames']} frames")
        print(f"File size: {results['compression_ratio']:.2%} of original")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()