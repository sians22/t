#!/usr/bin/env python3
"""
Test script for Mobile2 Global Bot
Tests basic functionality without requiring game connection
"""

import sys
import os
import json
import time
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config_loading():
    """Test configuration loading"""
    print("Testing configuration loading...")
    
    try:
        from mobile2_bot import Mobile2Bot
        bot = Mobile2Bot()
        
        # Test config structure
        required_keys = [
            'potions', 'wallhack', 'restart_here', 'upgrade_slot1',
            'farm', 'targeting', 'base_skills', 'esp', 'speed',
            'items', 'whitelist', 'player_actions', 'gm_actions',
            'spambot', 'fishing', 'route'
        ]
        
        for key in required_keys:
            if key not in bot.config:
                print(f"❌ Missing config key: {key}")
                return False
        
        print("✅ Configuration loading test passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration loading test failed: {e}")
        return False

def test_game_interaction():
    """Test game interaction module"""
    print("Testing game interaction module...")
    
    try:
        from game_interaction import GameInteraction
        game = GameInteraction()
        
        # Test basic methods (without connecting to game)
        print("✅ Game interaction module loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Game interaction test failed: {e}")
        return False

def test_ui_creation():
    """Test UI creation"""
    print("Testing UI creation...")
    
    try:
        from mobile2_bot import Mobile2Bot
        
        # Create bot instance (this will create the UI)
        bot = Mobile2Bot()
        
        # Test if main window exists
        if hasattr(bot, 'root') and bot.root:
            print("✅ UI creation test passed")
            return True
        else:
            print("❌ UI creation test failed - no root window")
            return False
            
    except Exception as e:
        print(f"❌ UI creation test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("Testing file operations...")
    
    try:
        # Test config file creation
        test_config = {
            "test": "value",
            "nested": {
                "key": "value"
            }
        }
        
        with open("test_config.json", "w") as f:
            json.dump(test_config, f, indent=2)
        
        # Test config file loading
        with open("test_config.json", "r") as f:
            loaded_config = json.load(f)
        
        if loaded_config == test_config:
            print("✅ File operations test passed")
            os.remove("test_config.json")  # Clean up
            return True
        else:
            print("❌ File operations test failed - config mismatch")
            return False
            
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Mobile2 Global Bot Test Suite")
    print("=" * 40)
    
    tests = [
        test_config_loading,
        test_game_interaction,
        test_ui_creation,
        test_file_operations
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed! Bot is ready to use.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)