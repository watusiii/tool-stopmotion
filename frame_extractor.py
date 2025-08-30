import cv2
import numpy as np
import os
import base64
from typing import List, Dict, Tuple
from pathlib import Path
import json


class FrameExtractor:
    """
    Clean, modular frame extraction for timeline editing.
    Separates concerns: extraction, thumbnail generation, metadata.
    """
    
    def __init__(self, thumbnail_width: int = 120):
        self.thumbnail_width = thumbnail_width
        
    def extract_frames_with_metadata(
        self, 
        video_path: str, 
        frame_reduction_factor: int = 2
    ) -> Dict:
        """
        Extract frames and generate metadata for timeline editing.
        
        Args:
            video_path: Path to input video
            frame_reduction_factor: Keep every Nth frame
            
        Returns:
            Dictionary with frames data, thumbnails, and metadata
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video not found: {video_path}")
            
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
            
        # Video metadata
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps
        
        frames_data = []
        frame_count = 0
        extracted_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Extract every Nth frame
                if frame_count % frame_reduction_factor == 0:
                    # Generate thumbnail
                    thumbnail_b64 = self._create_thumbnail(frame)
                    
                    # Frame timing info
                    timestamp = frame_count / fps
                    
                    frame_data = {
                        'index': extracted_count,
                        'original_frame': frame_count,
                        'timestamp': timestamp,
                        'thumbnail': thumbnail_b64,
                        'hold_duration': frame_reduction_factor,  # Default hold
                        'selected': True  # Default selected for timeline
                    }
                    
                    frames_data.append(frame_data)
                    extracted_count += 1
                    
                frame_count += 1
                
        finally:
            cap.release()
            
        result = {
            'success': True,
            'video_metadata': {
                'fps': fps,
                'width': width,
                'height': height,
                'total_frames': total_frames,
                'duration': duration,
                'extracted_frames': extracted_count,
                'reduction_factor': frame_reduction_factor
            },
            'frames': frames_data,
            'timeline_data': self._generate_timeline_data(frames_data)
        }
        
        return result
        
    def _create_thumbnail(self, frame: np.ndarray) -> str:
        """
        Create base64-encoded thumbnail for web display.
        
        Args:
            frame: OpenCV frame
            
        Returns:
            Base64 encoded JPEG thumbnail
        """
        # Calculate thumbnail height maintaining aspect ratio
        height, width = frame.shape[:2]
        aspect_ratio = width / height
        thumbnail_height = int(self.thumbnail_width / aspect_ratio)
        
        # Resize frame
        thumbnail = cv2.resize(frame, (self.thumbnail_width, thumbnail_height))
        
        # Encode as JPEG
        _, buffer = cv2.imencode('.jpg', thumbnail, [cv2.IMWRITE_JPEG_QUALITY, 85])
        
        # Convert to base64
        thumbnail_b64 = base64.b64encode(buffer).decode('utf-8')
        
        return f"data:image/jpeg;base64,{thumbnail_b64}"
        
    def _generate_timeline_data(self, frames_data: List[Dict]) -> Dict:
        """
        Generate timeline metadata for editor.
        
        Args:
            frames_data: List of frame data dictionaries
            
        Returns:
            Timeline configuration data
        """
        total_hold_duration = sum(frame['hold_duration'] for frame in frames_data)
        
        timeline_data = {
            'total_frames': len(frames_data),
            'total_hold_duration': total_hold_duration,
            'default_hold': frames_data[0]['hold_duration'] if frames_data else 2,
            'presets': {
                'fast_action': 1,
                'normal': 2, 
                'slow_motion': 4,
                'dramatic_pause': 6
            }
        }
        
        return timeline_data
        
    def save_timeline_config(self, frames_data: List[Dict], output_path: str):
        """
        Save timeline configuration to JSON file.
        
        Args:
            frames_data: Modified frames data with user timing
            output_path: Path to save JSON config
        """
        config = {
            'version': '1.0',
            'frames': frames_data,
            'created_at': str(pd.Timestamp.now()) if 'pd' in globals() else 'unknown'
        }
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
    def load_timeline_config(self, config_path: str) -> Dict:
        """
        Load timeline configuration from JSON file.
        
        Args:
            config_path: Path to JSON config file
            
        Returns:
            Timeline configuration data
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        return config


class TimelineProcessor:
    """
    Processes video with custom timeline data.
    Separates rendering logic from extraction.
    """
    
    def __init__(self):
        pass
        
    def render_custom_timing(
        self, 
        video_path: str, 
        timeline_config: Dict, 
        output_path: str,
        quality: str = 'high'
    ) -> Dict:
        """
        Render video with custom frame timing from timeline editor.
        
        Args:
            video_path: Original video path
            timeline_config: User's timing configuration
            output_path: Output video path
            quality: Rendering quality
            
        Returns:
            Rendering results
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
            
        # Get video info
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Setup output writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, original_fps, (width, height))
        
        frames_data = timeline_config['frames']
        total_output_frames = 0
        
        try:
            for frame_data in frames_data:
                if not frame_data.get('selected', True):
                    continue
                    
                # Seek to specific frame
                original_frame_num = frame_data['original_frame']
                cap.set(cv2.CAP_PROP_POS_FRAMES, original_frame_num)
                
                ret, frame = cap.read()
                if not ret:
                    continue
                    
                # Write frame multiple times based on hold duration
                hold_duration = frame_data.get('hold_duration', 2)
                for _ in range(hold_duration):
                    out.write(frame)
                    total_output_frames += 1
                    
        finally:
            cap.release()
            out.release()
            
        # Calculate results
        output_duration = total_output_frames / original_fps
        
        results = {
            'success': True,
            'method': 'custom_timeline',
            'original_frames': len(frames_data),
            'output_frames': total_output_frames,
            'output_duration': output_duration,
            'original_fps': original_fps,
            'file_size': os.path.getsize(output_path) if os.path.exists(output_path) else 0
        }
        
        return results


# Example usage for testing
if __name__ == "__main__":
    extractor = FrameExtractor()
    
    # Extract frames for timeline editing
    try:
        result = extractor.extract_frames_with_metadata("test_video.mp4", 3)
        print(f"Extracted {result['video_metadata']['extracted_frames']} frames")
        print(f"Timeline contains {result['timeline_data']['total_frames']} frames")
        
        # Save example config
        extractor.save_timeline_config(result['frames'], "example_timeline.json")
        print("Saved timeline config")
        
    except Exception as e:
        print(f"Error: {e}")