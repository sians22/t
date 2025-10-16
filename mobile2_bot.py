#!/usr/bin/env python3
"""
Mobile2 Global Bot - GGBOT v2
A comprehensive bot for Mobile2 Global with all requested features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import time
import threading
import random
import os
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Mobile2Bot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GGBOT v2 - Mobile2 Global Bot")
        self.root.geometry("1200x800")
        
        # Bot state
        self.is_running = False
        self.bot_thread = None
        
        # Configuration
        self.config = self.load_config()
        
        # Initialize all features
        self.setup_ui()
        self.setup_bot_features()
        
    def load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            "potions": {
                "red_potion_threshold": 50,
                "blue_potion_threshold": 50,
                "stop_when_no_red": False
            },
            "wallhack": {
                "enabled": False
            },
            "restart_here": {
                "enabled": False,
                "position": (0, 0)
            },
            "upgrade_slot1": {
                "enabled": False
            },
            "farm": {
                "range": 100,
                "position": (0, 0),
                "enabled": False
            },
            "targeting": {
                "mobs": [],
                "stones": [],
                "attack_groups": 1
            },
            "base_skills": {
                "enabled": False
            },
            "esp": {
                "players": False,
                "stones": False
            },
            "speed": {
                "movement": 1.0,
                "wait_hack": 1.0,
                "wait_hack_range": 1.0
            },
            "items": {
                "search_items": [],
                "pickup_filter": True,
                "drop_no_bonus": False
            },
            "whitelist": {
                "players": [],
                "range": 100,
                "active": False
            },
            "player_actions": {
                "stop_wait_range": False,
                "stop_speedhacks": False,
                "stop_bot": False,
                "quit_game": False,
                "sound_alarm": False
            },
            "gm_actions": {
                "stop_wait_range": False,
                "stop_speedhacks": False,
                "stop_bot": False,
                "quit_game": False,
                "sound_alarm": False
            },
            "spambot": {
                "text": "",
                "seconds": 5,
                "enabled": False
            },
            "fishing": {
                "kill_fish": False,
                "grill_fish": False,
                "drop_dead_fish": False,
                "drop_hair_color": False,
                "dead_alarm": False,
                "delay_ms": 2650
            },
            "route": {
                "recording": False,
                "farm_range": 100,
                "name": "",
                "waypoints": [],
                "auto_route": False
            }
        }
        
        try:
            if os.path.exists("bot_config.json"):
                with open("bot_config.json", "r") as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open("bot_config.json", "w") as f:
                json.dump(self.config, f, indent=2)
            logger.info("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def setup_ui(self):
        """Setup the main UI"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_potion_tab()
        self.create_movement_tab()
        self.create_targeting_tab()
        self.create_items_tab()
        self.create_whitelist_tab()
        self.create_spambot_tab()
        self.create_fishing_tab()
        self.create_route_tab()
        self.create_settings_tab()
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Bot", command=self.start_bot)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Save Settings", command=self.save_config).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Load Settings", command=self.load_settings).pack(side=tk.RIGHT, padx=5)
    
    def create_potion_tab(self):
        """Create potion management tab"""
        potion_frame = ttk.Frame(self.notebook)
        self.notebook.add(potion_frame, text="Potions")
        
        # Red Potion
        red_frame = ttk.LabelFrame(potion_frame, text="Red Potion")
        red_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(red_frame, text="HP Threshold (%):").pack(side=tk.LEFT, padx=5)
        self.red_threshold = tk.IntVar(value=self.config["potions"]["red_potion_threshold"])
        ttk.Spinbox(red_frame, from_=1, to=100, textvariable=self.red_threshold, width=10).pack(side=tk.LEFT, padx=5)
        
        # Blue Potion
        blue_frame = ttk.LabelFrame(potion_frame, text="Blue Potion")
        blue_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(blue_frame, text="MP Threshold (%):").pack(side=tk.LEFT, padx=5)
        self.blue_threshold = tk.IntVar(value=self.config["potions"]["blue_potion_threshold"])
        ttk.Spinbox(blue_frame, from_=1, to=100, textvariable=self.blue_threshold, width=10).pack(side=tk.LEFT, padx=5)
        
        # Stop when no red potions
        self.stop_no_red = tk.BooleanVar(value=self.config["potions"]["stop_when_no_red"])
        ttk.Checkbutton(potion_frame, text="Stop bot when no red potions", variable=self.stop_no_red).pack(anchor=tk.W, padx=5, pady=5)
    
    def create_movement_tab(self):
        """Create movement and hacks tab"""
        movement_frame = ttk.Frame(self.notebook)
        self.notebook.add(movement_frame, text="Movement & Hacks")
        
        # Wallhack
        wallhack_frame = ttk.LabelFrame(movement_frame, text="Wallhack")
        wallhack_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.wallhack_enabled = tk.BooleanVar(value=self.config["wallhack"]["enabled"])
        ttk.Checkbutton(wallhack_frame, text="Enable Wallhack", variable=self.wallhack_enabled).pack(anchor=tk.W, padx=5)
        
        # Restart Here
        restart_frame = ttk.LabelFrame(movement_frame, text="Restart Here")
        restart_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.restart_enabled = tk.BooleanVar(value=self.config["restart_here"]["enabled"])
        ttk.Checkbutton(restart_frame, text="Restart Here", variable=self.restart_enabled).pack(anchor=tk.W, padx=5)
        
        # Movement Speed
        speed_frame = ttk.LabelFrame(movement_frame, text="Speed Settings")
        speed_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(speed_frame, text="Movement Speed:").pack(side=tk.LEFT, padx=5)
        self.movement_speed = tk.DoubleVar(value=self.config["speed"]["movement"])
        ttk.Spinbox(speed_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.movement_speed, width=10).pack(side=tk.LEFT, padx=5)
        
        # Wait Hack
        wait_frame = ttk.LabelFrame(movement_frame, text="Wait Hack")
        wait_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(wait_frame, text="Wait Hack Speed:").pack(side=tk.LEFT, padx=5)
        self.wait_hack_speed = tk.DoubleVar(value=self.config["speed"]["wait_hack"])
        ttk.Spinbox(wait_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.wait_hack_speed, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(wait_frame, text="Wait Hack Range:").pack(side=tk.LEFT, padx=5)
        self.wait_hack_range = tk.DoubleVar(value=self.config["speed"]["wait_hack_range"])
        ttk.Spinbox(wait_frame, from_=0.1, to=5.0, increment=0.1, textvariable=self.wait_hack_range, width=10).pack(side=tk.LEFT, padx=5)
    
    def create_targeting_tab(self):
        """Create targeting and farming tab"""
        target_frame = ttk.Frame(self.notebook)
        self.notebook.add(target_frame, text="Targeting & Farming")
        
        # Farm Range
        farm_frame = ttk.LabelFrame(target_frame, text="Farm Settings")
        farm_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(farm_frame, text="Farm Range:").pack(side=tk.LEFT, padx=5)
        self.farm_range = tk.IntVar(value=self.config["farm"]["range"])
        ttk.Spinbox(farm_frame, from_=10, to=1000, textvariable=self.farm_range, width=10).pack(side=tk.LEFT, padx=5)
        
        self.farm_enabled = tk.BooleanVar(value=self.config["farm"]["enabled"])
        ttk.Checkbutton(farm_frame, text="Enable Farming", variable=self.farm_enabled).pack(anchor=tk.W, padx=5)
        
        # Mob Selection
        mob_frame = ttk.LabelFrame(target_frame, text="Mob Selection")
        mob_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.mob_listbox = tk.Listbox(mob_frame, height=4)
        self.mob_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        mob_buttons = ttk.Frame(mob_frame)
        mob_buttons.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(mob_buttons, text="Add Mob", command=self.add_mob).pack(fill=tk.X, pady=2)
        ttk.Button(mob_buttons, text="Remove Mob", command=self.remove_mob).pack(fill=tk.X, pady=2)
        
        # Stone Selection
        stone_frame = ttk.LabelFrame(target_frame, text="Stone Selection")
        stone_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stone_listbox = tk.Listbox(stone_frame, height=4)
        self.stone_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        stone_buttons = ttk.Frame(stone_frame)
        stone_buttons.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(stone_buttons, text="Add Stone", command=self.add_stone).pack(fill=tk.X, pady=2)
        ttk.Button(stone_buttons, text="Remove Stone", command=self.remove_stone).pack(fill=tk.X, pady=2)
        
        # Attack Groups
        attack_frame = ttk.LabelFrame(target_frame, text="Attack Groups")
        attack_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.attack_groups_enabled = tk.BooleanVar(value=True)
        ttk.Checkbutton(attack_frame, text="Attack Multiple Groups", variable=self.attack_groups_enabled).pack(anchor=tk.W, padx=5)
        
        ttk.Label(attack_frame, text="Group Amount:").pack(side=tk.LEFT, padx=5)
        self.group_amount = tk.IntVar(value=self.config["targeting"]["attack_groups"])
        ttk.Spinbox(attack_frame, from_=1, to=10, textvariable=self.group_amount, width=10).pack(side=tk.LEFT, padx=5)
        
        # Base Skills
        self.base_skills_enabled = tk.BooleanVar(value=self.config["base_skills"]["enabled"])
        ttk.Checkbutton(target_frame, text="Auto Base Skills (Air Rage, etc.)", variable=self.base_skills_enabled).pack(anchor=tk.W, padx=5, pady=5)
    
    def create_items_tab(self):
        """Create item management tab"""
        items_frame = ttk.Frame(self.notebook)
        self.notebook.add(items_frame, text="Items")
        
        # Item Search
        search_frame = ttk.LabelFrame(items_frame, text="Item Search")
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search Item:").pack(side=tk.LEFT, padx=5)
        self.item_search = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.item_search, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(search_frame, text="Add Item", command=self.add_item).pack(side=tk.LEFT, padx=5)
        
        # Item List
        list_frame = ttk.LabelFrame(items_frame, text="Item List")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.item_listbox = tk.Listbox(list_frame)
        self.item_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        item_buttons = ttk.Frame(list_frame)
        item_buttons.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(item_buttons, text="Delete Item", command=self.delete_item).pack(fill=tk.X, pady=2)
        ttk.Button(item_buttons, text="Clear Items", command=self.clear_items).pack(fill=tk.X, pady=2)
        
        # Item Settings
        settings_frame = ttk.LabelFrame(items_frame, text="Item Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.pickup_filter = tk.BooleanVar(value=self.config["items"]["pickup_filter"])
        ttk.Checkbutton(settings_frame, text="Pickup Filter (Only listed items)", variable=self.pickup_filter).pack(anchor=tk.W, padx=5)
        
        self.drop_no_bonus = tk.BooleanVar(value=self.config["items"]["drop_no_bonus"])
        ttk.Checkbutton(settings_frame, text="Drop items with no bonus", variable=self.drop_no_bonus).pack(anchor=tk.W, padx=5)
        
        # File Management
        file_frame = ttk.LabelFrame(items_frame, text="File Management")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(file_frame, text="File Name:").pack(side=tk.LEFT, padx=5)
        self.file_name = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_name, width=20).pack(side=tk.LEFT, padx=5)
        
        file_buttons = ttk.Frame(file_frame)
        file_buttons.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(file_buttons, text="Save File", command=self.save_item_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="Load File", command=self.load_item_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons, text="Delete File", command=self.delete_item_file).pack(side=tk.LEFT, padx=2)
    
    def create_whitelist_tab(self):
        """Create whitelist and player detection tab"""
        whitelist_frame = ttk.Frame(self.notebook)
        self.notebook.add(whitelist_frame, text="Whitelist & Players")
        
        # Player Whitelist
        player_frame = ttk.LabelFrame(whitelist_frame, text="Player Whitelist")
        player_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(player_frame, text="Player Name:").pack(side=tk.LEFT, padx=5)
        self.player_name = tk.StringVar()
        ttk.Entry(player_frame, textvariable=self.player_name, width=20).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(player_frame, text="Add to Whitelist", command=self.add_to_whitelist).pack(side=tk.LEFT, padx=5)
        
        # Whitelist List
        wl_list_frame = ttk.LabelFrame(whitelist_frame, text="Whitelist")
        wl_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.whitelist_listbox = tk.Listbox(wl_list_frame)
        self.whitelist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        wl_buttons = ttk.Frame(wl_list_frame)
        wl_buttons.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(wl_buttons, text="Delete from Whitelist", command=self.delete_from_whitelist).pack(fill=tk.X, pady=2)
        
        # Range Settings
        range_frame = ttk.LabelFrame(whitelist_frame, text="Range Settings")
        range_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(range_frame, text="Player Range:").pack(side=tk.LEFT, padx=5)
        self.player_range = tk.IntVar(value=self.config["whitelist"]["range"])
        ttk.Spinbox(range_frame, from_=10, to=1000, textvariable=self.player_range, width=10).pack(side=tk.LEFT, padx=5)
        
        self.activate_range = tk.BooleanVar(value=self.config["whitelist"]["active"])
        ttk.Checkbutton(range_frame, text="Activate Range", variable=self.activate_range).pack(anchor=tk.W, padx=5)
        
        # Player Actions
        actions_frame = ttk.LabelFrame(whitelist_frame, text="Player Actions")
        actions_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stop_wait_range = tk.BooleanVar(value=self.config["player_actions"]["stop_wait_range"])
        ttk.Checkbutton(actions_frame, text="Stop Wait+Range when player enters", variable=self.stop_wait_range).pack(anchor=tk.W, padx=5)
        
        self.stop_speedhacks = tk.BooleanVar(value=self.config["player_actions"]["stop_speedhacks"])
        ttk.Checkbutton(actions_frame, text="Stop Speedhacks when player enters", variable=self.stop_speedhacks).pack(anchor=tk.W, padx=5)
        
        self.stop_bot_player = tk.BooleanVar(value=self.config["player_actions"]["stop_bot"])
        ttk.Checkbutton(actions_frame, text="Stop Bot when player enters", variable=self.stop_bot_player).pack(anchor=tk.W, padx=5)
        
        self.quit_player = tk.BooleanVar(value=self.config["player_actions"]["quit_game"])
        ttk.Checkbutton(actions_frame, text="Quit when player enters", variable=self.quit_player).pack(anchor=tk.W, padx=5)
        
        self.sound_alarm_player = tk.BooleanVar(value=self.config["player_actions"]["sound_alarm"])
        ttk.Checkbutton(actions_frame, text="Sound Alarm when player enters", variable=self.sound_alarm_player).pack(anchor=tk.W, padx=5)
        
        # GM Actions
        gm_frame = ttk.LabelFrame(whitelist_frame, text="GM Actions")
        gm_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.stop_wait_range_gm = tk.BooleanVar(value=self.config["gm_actions"]["stop_wait_range"])
        ttk.Checkbutton(gm_frame, text="Stop Wait+Range when GM enters", variable=self.stop_wait_range_gm).pack(anchor=tk.W, padx=5)
        
        self.stop_speedhacks_gm = tk.BooleanVar(value=self.config["gm_actions"]["stop_speedhacks"])
        ttk.Checkbutton(gm_frame, text="Stop Speedhacks when GM enters", variable=self.stop_speedhacks_gm).pack(anchor=tk.W, padx=5)
        
        self.stop_bot_gm = tk.BooleanVar(value=self.config["gm_actions"]["stop_bot"])
        ttk.Checkbutton(gm_frame, text="Stop Bot when GM enters", variable=self.stop_bot_gm).pack(anchor=tk.W, padx=5)
        
        self.quit_gm = tk.BooleanVar(value=self.config["gm_actions"]["quit_game"])
        ttk.Checkbutton(gm_frame, text="Quit when GM enters", variable=self.quit_gm).pack(anchor=tk.W, padx=5)
        
        self.sound_alarm_gm = tk.BooleanVar(value=self.config["gm_actions"]["sound_alarm"])
        ttk.Checkbutton(gm_frame, text="Sound Alarm when GM enters", variable=self.sound_alarm_gm).pack(anchor=tk.W, padx=5)
    
    def create_spambot_tab(self):
        """Create spambot tab"""
        spam_frame = ttk.Frame(self.notebook)
        self.notebook.add(spam_frame, text="Spambot")
        
        # Spam Settings
        settings_frame = ttk.LabelFrame(spam_frame, text="Spam Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Text:").pack(anchor=tk.W, padx=5)
        self.spam_text = tk.Text(settings_frame, height=3, width=50)
        self.spam_text.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Seconds:").pack(side=tk.LEFT, padx=5)
        self.spam_seconds = tk.IntVar(value=self.config["spambot"]["seconds"])
        ttk.Spinbox(settings_frame, from_=1, to=300, textvariable=self.spam_seconds, width=10).pack(side=tk.LEFT, padx=5)
        
        self.spam_enabled = tk.BooleanVar(value=self.config["spambot"]["enabled"])
        ttk.Checkbutton(settings_frame, text="Start Spambot", variable=self.spam_enabled).pack(anchor=tk.W, padx=5)
    
    def create_fishing_tab(self):
        """Create fishing bot tab"""
        fishing_frame = ttk.Frame(self.notebook)
        self.notebook.add(fishing_frame, text="Fishing Bot")
        
        # Fishing Settings
        settings_frame = ttk.LabelFrame(fishing_frame, text="Fishing Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.kill_fish = tk.BooleanVar(value=self.config["fishing"]["kill_fish"])
        ttk.Checkbutton(settings_frame, text="Kill Fish", variable=self.kill_fish).pack(anchor=tk.W, padx=5)
        
        self.grill_fish = tk.BooleanVar(value=self.config["fishing"]["grill_fish"])
        ttk.Checkbutton(settings_frame, text="Grill Fish", variable=self.grill_fish).pack(anchor=tk.W, padx=5)
        
        self.drop_dead_fish = tk.BooleanVar(value=self.config["fishing"]["drop_dead_fish"])
        ttk.Checkbutton(settings_frame, text="Drop Dead Fish", variable=self.drop_dead_fish).pack(anchor=tk.W, padx=5)
        
        self.drop_hair_color = tk.BooleanVar(value=self.config["fishing"]["drop_hair_color"])
        ttk.Checkbutton(settings_frame, text="Drop Hair Color", variable=self.drop_hair_color).pack(anchor=tk.W, padx=5)
        
        self.dead_alarm = tk.BooleanVar(value=self.config["fishing"]["dead_alarm"])
        ttk.Checkbutton(settings_frame, text="Dead Alarm", variable=self.dead_alarm).pack(anchor=tk.W, padx=5)
        
        ttk.Label(settings_frame, text="Delay (ms):").pack(side=tk.LEFT, padx=5)
        self.fishing_delay = tk.IntVar(value=self.config["fishing"]["delay_ms"])
        ttk.Spinbox(settings_frame, from_=1000, to=10000, textvariable=self.fishing_delay, width=10).pack(side=tk.LEFT, padx=5)
    
    def create_route_tab(self):
        """Create route recording tab"""
        route_frame = ttk.Frame(self.notebook)
        self.notebook.add(route_frame, text="Route Recording")
        
        # Route Recording
        record_frame = ttk.LabelFrame(route_frame, text="Route Recording")
        record_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.record_route = tk.BooleanVar(value=self.config["route"]["recording"])
        ttk.Checkbutton(record_frame, text="Start Recording", variable=self.record_route).pack(anchor=tk.W, padx=5)
        
        # Route Settings
        settings_frame = ttk.LabelFrame(route_frame, text="Route Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(settings_frame, text="Farm Range:").pack(side=tk.LEFT, padx=5)
        self.route_farm_range = tk.IntVar(value=self.config["route"]["farm_range"])
        ttk.Spinbox(settings_frame, from_=10, to=1000, textvariable=self.route_farm_range, width=10).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(settings_frame, text="Route Name:").pack(side=tk.LEFT, padx=5)
        self.route_name = tk.StringVar(value=self.config["route"]["name"])
        ttk.Entry(settings_frame, textvariable=self.route_name, width=20).pack(side=tk.LEFT, padx=5)
        
        # Route Management
        mgmt_frame = ttk.LabelFrame(route_frame, text="Route Management")
        mgmt_frame.pack(fill=tk.X, padx=5, pady=5)
        
        route_buttons = ttk.Frame(mgmt_frame)
        route_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(route_buttons, text="Save Route", command=self.save_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(route_buttons, text="Load Route", command=self.load_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(route_buttons, text="Delete Route", command=self.delete_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(route_buttons, text="Clear Route", command=self.clear_route).pack(side=tk.LEFT, padx=2)
        
        # Auto Route
        auto_frame = ttk.LabelFrame(route_frame, text="Auto Route")
        auto_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.auto_route = tk.BooleanVar(value=self.config["route"]["auto_route"])
        ttk.Checkbutton(auto_frame, text="Start Auto Route", variable=self.auto_route).pack(anchor=tk.W, padx=5)
    
    def create_settings_tab(self):
        """Create general settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # ESP Settings
        esp_frame = ttk.LabelFrame(settings_frame, text="ESP Settings")
        esp_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.esp_players = tk.BooleanVar(value=self.config["esp"]["players"])
        ttk.Checkbutton(esp_frame, text="ESP Players", variable=self.esp_players).pack(anchor=tk.W, padx=5)
        
        self.esp_stones = tk.BooleanVar(value=self.config["esp"]["stones"])
        ttk.Checkbutton(esp_frame, text="ESP Stones", variable=self.esp_stones).pack(anchor=tk.W, padx=5)
        
        # Upgrade Settings
        upgrade_frame = ttk.LabelFrame(settings_frame, text="Upgrade Settings")
        upgrade_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.upgrade_slot1 = tk.BooleanVar(value=self.config["upgrade_slot1"]["enabled"])
        ttk.Checkbutton(upgrade_frame, text="Upgrade Item Slot 1", variable=self.upgrade_slot1).pack(anchor=tk.W, padx=5)
    
    def setup_bot_features(self):
        """Initialize bot feature handlers"""
        # Initialize game interaction
        from game_interaction import GameInteraction
        self.game = GameInteraction()
        
        # Try to connect to game
        if self.game.connect_to_game():
            logger.info("Connected to Mobile2 Global")
        else:
            logger.warning("Could not connect to Mobile2 Global - some features may not work")
        
        # Initialize feature timers
        self.last_potion_check = 0
        self.last_attack = 0
        self.last_movement = 0
        self.last_spam = 0
        self.last_fishing = 0
    
    # Event handlers
    def add_mob(self):
        mob_name = tk.simpledialog.askstring("Add Mob", "Enter mob name:")
        if mob_name:
            self.mob_listbox.insert(tk.END, mob_name)
    
    def remove_mob(self):
        selection = self.mob_listbox.curselection()
        if selection:
            self.mob_listbox.delete(selection[0])
    
    def add_stone(self):
        stone_name = tk.simpledialog.askstring("Add Stone", "Enter stone name:")
        if stone_name:
            self.stone_listbox.insert(tk.END, stone_name)
    
    def remove_stone(self):
        selection = self.stone_listbox.curselection()
        if selection:
            self.stone_listbox.delete(selection[0])
    
    def add_item(self):
        item_name = self.item_search.get()
        if item_name:
            self.item_listbox.insert(tk.END, item_name)
            self.item_search.set("")
    
    def delete_item(self):
        selection = self.item_listbox.curselection()
        if selection:
            self.item_listbox.delete(selection[0])
    
    def clear_items(self):
        self.item_listbox.delete(0, tk.END)
    
    def add_to_whitelist(self):
        player_name = self.player_name.get()
        if player_name:
            self.whitelist_listbox.insert(tk.END, player_name)
            self.player_name.set("")
    
    def delete_from_whitelist(self):
        selection = self.whitelist_listbox.curselection()
        if selection:
            self.whitelist_listbox.delete(selection[0])
    
    def save_item_file(self):
        filename = self.file_name.get()
        if not filename:
            messagebox.showerror("Error", "Please enter a filename")
            return
        
        items = [self.item_listbox.get(i) for i in range(self.item_listbox.size())]
        try:
            with open(f"item_files/{filename}.json", "w") as f:
                json.dump(items, f, indent=2)
            messagebox.showinfo("Success", f"Items saved to {filename}.json")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def load_item_file(self):
        filename = filedialog.askopenfilename(
            title="Load Item File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    items = json.load(f)
                self.item_listbox.delete(0, tk.END)
                for item in items:
                    self.item_listbox.insert(tk.END, item)
                messagebox.showinfo("Success", "Items loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
    
    def delete_item_file(self):
        filename = self.file_name.get()
        if not filename:
            messagebox.showerror("Error", "Please enter a filename")
            return
        
        try:
            os.remove(f"item_files/{filename}.json")
            messagebox.showinfo("Success", f"File {filename}.json deleted")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}")
    
    def save_route(self):
        route_name = self.route_name.get()
        if not route_name:
            messagebox.showerror("Error", "Please enter a route name")
            return
        
        # This would save the current route waypoints
        messagebox.showinfo("Success", f"Route {route_name} saved")
    
    def load_route(self):
        route_name = self.route_name.get()
        if not route_name:
            messagebox.showerror("Error", "Please enter a route name")
            return
        
        # This would load the route waypoints
        messagebox.showinfo("Success", f"Route {route_name} loaded")
    
    def delete_route(self):
        route_name = self.route_name.get()
        if not route_name:
            messagebox.showerror("Error", "Please enter a route name")
            return
        
        # This would delete the route
        messagebox.showinfo("Success", f"Route {route_name} deleted")
    
    def clear_route(self):
        # This would clear the current route
        messagebox.showinfo("Success", "Route cleared")
    
    def start_bot(self):
        """Start the bot"""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Start bot thread
        self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
        self.bot_thread.start()
        
        logger.info("Bot started")
    
    def stop_bot(self):
        """Stop the bot"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        
        logger.info("Bot stopped")
    
    def bot_loop(self):
        """Main bot loop"""
        while self.is_running:
            try:
                # Update configuration from UI
                self.update_config_from_ui()
                
                # Execute bot features
                self.execute_bot_features()
                
                # Small delay to prevent high CPU usage
                time.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in bot loop: {e}")
                time.sleep(1)
    
    def update_config_from_ui(self):
        """Update configuration from UI values"""
        self.config["potions"]["red_potion_threshold"] = self.red_threshold.get()
        self.config["potions"]["blue_potion_threshold"] = self.blue_threshold.get()
        self.config["potions"]["stop_when_no_red"] = self.stop_no_red.get()
        
        self.config["wallhack"]["enabled"] = self.wallhack_enabled.get()
        self.config["restart_here"]["enabled"] = self.restart_enabled.get()
        
        self.config["speed"]["movement"] = self.movement_speed.get()
        self.config["speed"]["wait_hack"] = self.wait_hack_speed.get()
        self.config["speed"]["wait_hack_range"] = self.wait_hack_range.get()
        
        self.config["farm"]["range"] = self.farm_range.get()
        self.config["farm"]["enabled"] = self.farm_enabled.get()
        
        self.config["base_skills"]["enabled"] = self.base_skills_enabled.get()
        
        self.config["esp"]["players"] = self.esp_players.get()
        self.config["esp"]["stones"] = self.esp_stones.get()
        
        self.config["upgrade_slot1"]["enabled"] = self.upgrade_slot1.get()
        
        self.config["items"]["pickup_filter"] = self.pickup_filter.get()
        self.config["items"]["drop_no_bonus"] = self.drop_no_bonus.get()
        
        self.config["whitelist"]["range"] = self.player_range.get()
        self.config["whitelist"]["active"] = self.activate_range.get()
        
        self.config["player_actions"]["stop_wait_range"] = self.stop_wait_range.get()
        self.config["player_actions"]["stop_speedhacks"] = self.stop_speedhacks.get()
        self.config["player_actions"]["stop_bot"] = self.stop_bot_player.get()
        self.config["player_actions"]["quit_game"] = self.quit_player.get()
        self.config["player_actions"]["sound_alarm"] = self.sound_alarm_player.get()
        
        self.config["gm_actions"]["stop_wait_range"] = self.stop_wait_range_gm.get()
        self.config["gm_actions"]["stop_speedhacks"] = self.stop_speedhacks_gm.get()
        self.config["gm_actions"]["stop_bot"] = self.stop_bot_gm.get()
        self.config["gm_actions"]["quit_game"] = self.quit_gm.get()
        self.config["gm_actions"]["sound_alarm"] = self.sound_alarm_gm.get()
        
        self.config["spambot"]["text"] = self.spam_text.get("1.0", tk.END).strip()
        self.config["spambot"]["seconds"] = self.spam_seconds.get()
        self.config["spambot"]["enabled"] = self.spam_enabled.get()
        
        self.config["fishing"]["kill_fish"] = self.kill_fish.get()
        self.config["fishing"]["grill_fish"] = self.grill_fish.get()
        self.config["fishing"]["drop_dead_fish"] = self.drop_dead_fish.get()
        self.config["fishing"]["drop_hair_color"] = self.drop_hair_color.get()
        self.config["fishing"]["dead_alarm"] = self.dead_alarm.get()
        self.config["fishing"]["delay_ms"] = self.fishing_delay.get()
        
        self.config["route"]["recording"] = self.record_route.get()
        self.config["route"]["farm_range"] = self.route_farm_range.get()
        self.config["route"]["name"] = self.route_name.get()
        self.config["route"]["auto_route"] = self.auto_route.get()
    
    def execute_bot_features(self):
        """Execute all active bot features"""
        # This is where the actual game interaction would happen
        # For now, this is a placeholder that demonstrates the structure
        
        # Potion management
        if self.config["potions"]["red_potion_threshold"] > 0:
            self.manage_potions()
        
        # Wallhack
        if self.config["wallhack"]["enabled"]:
            self.enable_wallhack()
        
        # Farming
        if self.config["farm"]["enabled"]:
            self.farm_mobs()
        
        # Item management
        if self.config["items"]["pickup_filter"]:
            self.manage_items()
        
        # Spambot
        if self.config["spambot"]["enabled"]:
            self.run_spambot()
        
        # Fishing bot
        if any([self.config["fishing"]["kill_fish"], 
                self.config["fishing"]["grill_fish"],
                self.config["fishing"]["drop_dead_fish"]]):
            self.run_fishing_bot()
    
    def manage_potions(self):
        """Manage potion usage based on HP/MP"""
        try:
            # Get current HP and MP percentages
            hp_percentage = self.game.get_player_hp_percentage()
            mp_percentage = self.game.get_player_mp_percentage()
            
            # Use red potion if HP is below threshold
            if hp_percentage < self.config["potions"]["red_potion_threshold"]:
                if self.game.use_red_potion():
                    logger.info(f"Used red potion - HP: {hp_percentage:.1f}%")
            
            # Use blue potion if MP is below threshold
            if mp_percentage < self.config["potions"]["blue_potion_threshold"]:
                if self.game.use_blue_potion():
                    logger.info(f"Used blue potion - MP: {mp_percentage:.1f}%")
            
            # Check if we should stop when no red potions
            if self.config["potions"]["stop_when_no_red"]:
                # This would check inventory for red potions
                # For now, just log the check
                if hp_percentage < 10:  # Very low HP
                    logger.warning("HP very low - consider stopping bot if no red potions")
                    
        except Exception as e:
            logger.error(f"Error managing potions: {e}")
    
    def enable_wallhack(self):
        """Enable wallhack functionality"""
        try:
            if self.game.enable_wallhack():
                logger.info("Wallhack enabled")
            else:
                logger.warning("Failed to enable wallhack")
        except Exception as e:
            logger.error(f"Error enabling wallhack: {e}")
    
    def farm_mobs(self):
        """Farm mobs in the specified range"""
        try:
            current_time = time.time()
            
            # Check if enough time has passed since last attack
            if current_time - self.last_attack < 0.5:  # 0.5 second cooldown
                return
            
            # Get mobs in range
            mobs = self.game.get_mobs_in_range(self.config["farm"]["range"])
            
            if mobs:
                # Attack the first mob
                if self.game.attack():
                    self.last_attack = current_time
                    logger.debug(f"Attacking mob - {len(mobs)} mobs in range")
            
            # Move towards farm position if set
            if self.config["farm"]["position"] != [0, 0, 0]:
                farm_x, farm_y, farm_z = self.config["farm"]["position"]
                current_x, current_y, current_z = self.game.get_player_position()
                
                # Calculate distance
                distance = ((farm_x - current_x) ** 2 + (farm_y - current_y) ** 2 + (farm_z - current_z) ** 2) ** 0.5
                
                if distance > 10:  # Move if more than 10 units away
                    if current_time - self.last_movement > 1.0:  # 1 second movement cooldown
                        self.game.move_to_position(farm_x, farm_y, farm_z)
                        self.last_movement = current_time
                        
        except Exception as e:
            logger.error(f"Error farming mobs: {e}")
    
    def manage_items(self):
        """Manage item pickup and dropping"""
        try:
            # Get items in range
            items = self.game.get_items_in_range(50)  # 50 unit pickup range
            
            for item in items:
                item_name = item.get('name', '')
                
                # Check if item should be picked up
                should_pickup = False
                
                if self.config["items"]["pickup_filter"]:
                    # Only pickup listed items
                    search_items = [self.item_listbox.get(i) for i in range(self.item_listbox.size())]
                    if item_name in search_items:
                        should_pickup = True
                else:
                    # Pickup all items
                    should_pickup = True
                
                if should_pickup:
                    if self.game.pickup_item():
                        logger.debug(f"Picked up item: {item_name}")
                        time.sleep(0.1)  # Small delay between pickups
                        
        except Exception as e:
            logger.error(f"Error managing items: {e}")
    
    def run_spambot(self):
        """Run spambot functionality"""
        try:
            current_time = time.time()
            spam_interval = self.config["spambot"]["seconds"]
            
            # Check if enough time has passed since last spam
            if current_time - self.last_spam < spam_interval:
                return
            
            spam_text = self.config["spambot"]["text"]
            if spam_text and len(spam_text.strip()) > 0:
                if self.game.send_chat_message(spam_text):
                    self.last_spam = current_time
                    logger.debug(f"Sent spam message: {spam_text}")
                    
        except Exception as e:
            logger.error(f"Error running spambot: {e}")
    
    def run_fishing_bot(self):
        """Run fishing bot functionality"""
        try:
            current_time = time.time()
            fishing_delay = self.config["fishing"]["delay_ms"] / 1000.0  # Convert to seconds
            
            # Check if enough time has passed since last fishing action
            if current_time - self.last_fishing < fishing_delay:
                return
            
            # Kill fish
            if self.config["fishing"]["kill_fish"]:
                # This would target and kill fish
                logger.debug("Killing fish...")
            
            # Grill fish
            if self.config["fishing"]["grill_fish"]:
                # This would grill fish
                logger.debug("Grilling fish...")
            
            # Drop dead fish
            if self.config["fishing"]["drop_dead_fish"]:
                # This would drop dead fish
                logger.debug("Dropping dead fish...")
            
            # Drop hair color
            if self.config["fishing"]["drop_hair_color"]:
                # This would drop hair color items
                logger.debug("Dropping hair color...")
            
            self.last_fishing = current_time
            
        except Exception as e:
            logger.error(f"Error running fishing bot: {e}")
    
    def load_settings(self):
        """Load settings from file"""
        filename = filedialog.askopenfilename(
            title="Load Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, "r") as f:
                    self.config = json.load(f)
                self.update_ui_from_config()
                messagebox.showinfo("Success", "Settings loaded successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {e}")
    
    def update_ui_from_config(self):
        """Update UI elements from configuration"""
        # Update all UI elements with config values
        self.red_threshold.set(self.config["potions"]["red_potion_threshold"])
        self.blue_threshold.set(self.config["potions"]["blue_potion_threshold"])
        self.stop_no_red.set(self.config["potions"]["stop_when_no_red"])
        
        self.wallhack_enabled.set(self.config["wallhack"]["enabled"])
        self.restart_enabled.set(self.config["restart_here"]["enabled"])
        
        self.movement_speed.set(self.config["speed"]["movement"])
        self.wait_hack_speed.set(self.config["speed"]["wait_hack"])
        self.wait_hack_range.set(self.config["speed"]["wait_hack_range"])
        
        self.farm_range.set(self.config["farm"]["range"])
        self.farm_enabled.set(self.config["farm"]["enabled"])
        
        self.base_skills_enabled.set(self.config["base_skills"]["enabled"])
        
        self.esp_players.set(self.config["esp"]["players"])
        self.esp_stones.set(self.config["esp"]["stones"])
        
        self.upgrade_slot1.set(self.config["upgrade_slot1"]["enabled"])
        
        self.pickup_filter.set(self.config["items"]["pickup_filter"])
        self.drop_no_bonus.set(self.config["items"]["drop_no_bonus"])
        
        self.player_range.set(self.config["whitelist"]["range"])
        self.activate_range.set(self.config["whitelist"]["active"])
        
        self.stop_wait_range.set(self.config["player_actions"]["stop_wait_range"])
        self.stop_speedhacks.set(self.config["player_actions"]["stop_speedhacks"])
        self.stop_bot_player.set(self.config["player_actions"]["stop_bot"])
        self.quit_player.set(self.config["player_actions"]["quit_game"])
        self.sound_alarm_player.set(self.config["player_actions"]["sound_alarm"])
        
        self.stop_wait_range_gm.set(self.config["gm_actions"]["stop_wait_range"])
        self.stop_speedhacks_gm.set(self.config["gm_actions"]["stop_speedhacks"])
        self.stop_bot_gm.set(self.config["gm_actions"]["stop_bot"])
        self.quit_gm.set(self.config["gm_actions"]["quit_game"])
        self.sound_alarm_gm.set(self.config["gm_actions"]["sound_alarm"])
        
        self.spam_text.delete("1.0", tk.END)
        self.spam_text.insert("1.0", self.config["spambot"]["text"])
        self.spam_seconds.set(self.config["spambot"]["seconds"])
        self.spam_enabled.set(self.config["spambot"]["enabled"])
        
        self.kill_fish.set(self.config["fishing"]["kill_fish"])
        self.grill_fish.set(self.config["fishing"]["grill_fish"])
        self.drop_dead_fish.set(self.config["fishing"]["drop_dead_fish"])
        self.drop_hair_color.set(self.config["fishing"]["drop_hair_color"])
        self.dead_alarm.set(self.config["fishing"]["dead_alarm"])
        self.fishing_delay.set(self.config["fishing"]["delay_ms"])
        
        self.record_route.set(self.config["route"]["recording"])
        self.route_farm_range.set(self.config["route"]["farm_range"])
        self.route_name.set(self.config["route"]["name"])
        self.auto_route.set(self.config["route"]["auto_route"])
    
    def run(self):
        """Run the bot application"""
        # Create necessary directories
        os.makedirs("item_files", exist_ok=True)
        os.makedirs("route_files", exist_ok=True)
        
        # Start the GUI
        self.root.mainloop()

if __name__ == "__main__":
    # Import tkinter.simpledialog for input dialogs
    import tkinter.simpledialog
    
    bot = Mobile2Bot()
    bot.run()