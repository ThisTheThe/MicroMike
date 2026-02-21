#!/usr/bin/env python3
"""
CSS File Monitor and Copy Script
Monitors theme.css for changes and copies it to predefined locations.
"""

import os
import shutil
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
from datetime import datetime

# Configuration
SOURCE_FILE = "theme.css"
DESTINATION_PATHS = [
    # Add your destination paths here
    "C:/Users/Tim/Documents/pim3/newtekgit/.obsidian/themes/Art Deco CSS/theme.css"
    # Add more paths as needed
]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('css_monitor.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CSSFileHandler(FileSystemEventHandler):
    """Handler for CSS file change events."""
    
    def __init__(self, source_file, destinations):
        self.source_file = Path(source_file).resolve()
        self.destinations = [Path(dest) for dest in destinations]
        self.last_modified = 0
        
    def _handle_event(self, event):
        """Shared handler for modified and created events."""
        if event.is_directory:
            return

        file_path = Path(event.src_path).resolve()

        if file_path == self.source_file:
            current_time = time.time()
            if current_time - self.last_modified < 2:  # 2 second cooldown
                return
            self.last_modified = current_time
            self.copy_file()

    def on_modified(self, event):
        """Handle file modification events."""
        self._handle_event(event)

    def on_created(self, event):
        """Handle file creation events (catches atomic saves via temp file rename)."""
        self._handle_event(event)
    
    def copy_file(self):
        """Copy the CSS file to all destination paths."""
        if not self.source_file.exists():
            logger.error(f"Source file {self.source_file} does not exist!")
            return
            
        logger.info(f"Detected change in {self.source_file.name}")
        
        # Wait for file to be fully written (some editors write in chunks)
        time.sleep(0.1)
        
        # Check if file has content before copying
        try:
            file_size = self.source_file.stat().st_size
            if file_size == 0:
                logger.warning("Source file is empty, waiting for content...")
                time.sleep(0.5)  # Wait a bit more
                file_size = self.source_file.stat().st_size
                if file_size == 0:
                    logger.error("Source file is still empty, skipping copy")
                    return
        except Exception as e:
            logger.error(f"Error checking file size: {e}")
            return
        
        logger.info(f"File size: {file_size} bytes")
        
        success_count = 0
        for dest_path in self.destinations:
            try:
                # Create destination directory if it doesn't exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy the file
                shutil.copy2(self.source_file, dest_path)
                
                # Verify the copy was successful
                if dest_path.exists():
                    dest_size = dest_path.stat().st_size
                    if dest_size == file_size:
                        logger.info(f"SUCCESS: Copied to: {dest_path} ({dest_size} bytes)")
                        success_count += 1
                    else:
                        logger.warning(f"Copy size mismatch: {dest_path} (expected {file_size}, got {dest_size})")
                else:
                    logger.error(f"Copy failed: {dest_path} does not exist after copy")
                
            except Exception as e:
                logger.error(f"FAILED: Could not copy to {dest_path}: {e}")
        
        logger.info(f"Copy operation completed: {success_count}/{len(self.destinations)} successful")

def validate_paths(source_file, destinations):
    """Validate source file and destination paths."""
    source_path = Path(source_file)
    
    if not source_path.exists():
        logger.warning(f"Source file {source_path} does not exist yet. Monitoring will start once it's created.")
    
    # Check if destination directories are accessible
    for dest in destinations:
        dest_path = Path(dest)
        try:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"Destination accessible: {dest_path}")
        except Exception as e:
            logger.warning(f"Destination may not be accessible: {dest_path} - {e}")

def main():
    """Main function to start the file monitor."""
    print("CSS File Monitor Started")
    print("=" * 50)
    print(f"Monitoring: {SOURCE_FILE}")
    print("Destination paths:")
    for i, dest in enumerate(DESTINATION_PATHS, 1):
        print(f"  {i}. {dest}")
    print("=" * 50)
    
    # Validate paths
    validate_paths(SOURCE_FILE, DESTINATION_PATHS)
    
    # Setup file handler
    event_handler = CSSFileHandler(SOURCE_FILE, DESTINATION_PATHS)
    
    # Setup observer
    observer = Observer()
    
    # Monitor the directory containing the CSS file
    watch_directory = Path(SOURCE_FILE).parent.resolve()
    observer.schedule(event_handler, str(watch_directory), recursive=False)
    
    # Start monitoring
    observer.start()
    logger.info(f"Started monitoring {watch_directory}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file monitor...")
        observer.stop()
        print("\nFile monitor stopped.")
    
    observer.join()

if __name__ == "__main__":
    # Check for required dependencies
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("Error: watchdog library not found!")
        print("Install it with: pip install watchdog")
        exit(1)
    
    main()