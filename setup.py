#!/usr/bin/env python3
"""
Setup script for Mobile2 Global Bot
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        'item_files',
        'route_files',
        'configs',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_config_files():
    """Create default configuration files"""
    # Main config
    if not os.path.exists('bot_config.json'):
        with open('config_template.json', 'r') as f:
            config = json.load(f)
        
        with open('bot_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("✅ Created bot_config.json")
    
    # Logging config
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.FileHandler",
                "filename": "logs/bot.log",
                "mode": "a"
            }
        },
        "loggers": {
            "": {
                "handlers": ["default", "file"],
                "level": "DEBUG",
                "propagate": False
            }
        }
    }
    
    with open('logging_config.json', 'w') as f:
        json.dump(logging_config, f, indent=2)
    
    print("✅ Created logging_config.json")

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
        ])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform == 'win32':
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Mobile2 Global Bot.lnk")
            target = os.path.join(os.getcwd(), "start_bot.bat")
            wDir = os.getcwd()
            icon = os.path.join(os.getcwd(), "start_bot.bat")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
            
            print("✅ Created desktop shortcut")
        except ImportError:
            print("⚠️  Could not create desktop shortcut (winshell not available)")
        except Exception as e:
            print(f"⚠️  Could not create desktop shortcut: {e}")

def main():
    """Main setup function"""
    print("🔧 Mobile2 Global Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    
    print(f"✅ Python version: {sys.version}")
    
    # Create directories
    create_directories()
    
    # Create config files
    create_config_files()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed due to dependency installation error")
        return False
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print("\n✅ Setup completed successfully!")
    print("\nTo start the bot:")
    print("1. Run 'start_bot.bat' (Windows)")
    print("2. Or run 'python launcher.py'")
    print("3. Or run 'python mobile2_bot.py' directly")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)