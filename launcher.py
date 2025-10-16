#!/usr/bin/env python3
"""
Mobile2 Global Bot Launcher
Simple launcher script with dependency checking
"""

import sys
import subprocess
import os
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'tkinter',
        'win32gui',
        'psutil'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            elif package == 'win32gui':
                import win32gui
            elif package == 'psutil':
                import psutil
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies!")
            print("Please install manually: pip install -r requirements.txt")
            return False
    
    return True

def check_os_compatibility():
    """Check if operating system is compatible"""
    if platform.system() != 'Windows':
        print("⚠️  This bot is designed for Windows!")
        print("Some features may not work on other operating systems.")
        return False
    print(f"✅ Operating system: {platform.system()}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['item_files', 'route_files']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def main():
    """Main launcher function"""
    print("🚀 Mobile2 Global Bot Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    # Check OS compatibility
    check_os_compatibility()
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return
    
    # Create directories
    create_directories()
    
    print("\n✅ All checks passed!")
    print("Starting Mobile2 Global Bot...")
    print("=" * 40)
    
    # Import and run the bot
    try:
        from mobile2_bot import Mobile2Bot
        bot = Mobile2Bot()
        bot.run()
    except ImportError as e:
        print(f"❌ Failed to import bot: {e}")
        print("Make sure mobile2_bot.py is in the same directory!")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()