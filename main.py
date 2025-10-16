#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GGBOT v2 - Mobile2 Global Oyun Botu
Öğretmen ödevi için geliştirilmiş kapsamlı oyun botu
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import threading
import time
import random
from datetime import datetime
import pygame
import cv2
import numpy as np
from PIL import Image, ImageTk
import pyautogui
import keyboard
import mouse

# Modülleri import et
from modules.potion_system import PotionSystem
from modules.attack_system import AttackSystem
from modules.esp_system import ESPSystem
from modules.speed_system import SpeedSystem
from modules.item_system import ItemSystem

class GGBot:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GGBOT v2 - Mobile2 Global Bot")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2b2b2b')
        
        # Bot durumu
        self.is_running = False
        self.settings = self.load_settings()
        
        # Ses sistemi
        pygame.mixer.init()
        
        # Bot thread'i
        self.bot_thread = None
        
        # Modülleri başlat
        self.potion_system = PotionSystem(self)
        self.attack_system = AttackSystem(self)
        self.esp_system = ESPSystem(self)
        self.speed_system = SpeedSystem(self)
        self.item_system = ItemSystem(self)
        
        self.setup_ui()
        self.load_default_settings()
        
    def setup_ui(self):
        """Ana arayüzü oluşturur"""
        # Ana notebook (sekmeler)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Sekmeler
        self.create_potion_tab(notebook)
        self.create_hack_tab(notebook)
        self.create_farm_tab(notebook)
        self.create_attack_tab(notebook)
        self.create_esp_tab(notebook)
        self.create_speed_tab(notebook)
        self.create_item_tab(notebook)
        self.create_whitelist_tab(notebook)
        self.create_spam_tab(notebook)
        self.create_fish_tab(notebook)
        self.create_route_tab(notebook)
        self.create_settings_tab(notebook)
        
        # Alt panel - Bot kontrolü
        control_frame = tk.Frame(self.root, bg='#2b2b2b')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Bot durumu
        self.status_label = tk.Label(control_frame, text="Bot Durumu: Durduruldu", 
                                   fg='red', bg='#2b2b2b', font=('Arial', 12, 'bold'))
        self.status_label.pack(side='left', padx=10)
        
        # Başlat/Durdur butonları
        self.start_btn = tk.Button(control_frame, text="Bot Başlat", command=self.start_bot,
                                 bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        self.start_btn.pack(side='right', padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="Bot Durdur", command=self.stop_bot,
                                bg='#f44336', fg='white', font=('Arial', 10, 'bold'))
        self.stop_btn.pack(side='right', padx=5)
        
    def create_potion_tab(self, notebook):
        """Potion sekmesi"""
        potion_frame = ttk.Frame(notebook)
        notebook.add(potion_frame, text="Potion Sistemi")
        
        # Red Potion
        red_frame = tk.LabelFrame(potion_frame, text="Red Potion", fg='red', bg='#2b2b2b')
        red_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(red_frame, text="Can Yüzdesi:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.red_potion_threshold = tk.Scale(red_frame, from_=10, to=100, orient='horizontal', 
                                           bg='#2b2b2b', fg='white')
        self.red_potion_threshold.set(30)
        self.red_potion_threshold.pack(side='left', padx=5)
        
        self.red_potion_enabled = tk.BooleanVar()
        tk.Checkbutton(red_frame, text="Red Potion Aktif", variable=self.red_potion_enabled,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=10)
        
        # Blue Potion
        blue_frame = tk.LabelFrame(potion_frame, text="Blue Potion", fg='blue', bg='#2b2b2b')
        blue_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(blue_frame, text="Mana Yüzdesi:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.blue_potion_threshold = tk.Scale(blue_frame, from_=10, to=100, orient='horizontal',
                                            bg='#2b2b2b', fg='white')
        self.blue_potion_threshold.set(30)
        self.blue_potion_threshold.pack(side='left', padx=5)
        
        self.blue_potion_enabled = tk.BooleanVar()
        tk.Checkbutton(blue_frame, text="Blue Potion Aktif", variable=self.blue_potion_enabled,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=10)
        
        # Stop bot when no red potions
        self.stop_no_red = tk.BooleanVar()
        tk.Checkbutton(potion_frame, text="Kırmızı pot bittiğinde bot durdur", 
                      variable=self.stop_no_red, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
    def create_hack_tab(self, notebook):
        """Hack sekmesi"""
        hack_frame = ttk.Frame(notebook)
        notebook.add(hack_frame, text="Hack Özellikleri")
        
        # Wallhack
        wallhack_frame = tk.LabelFrame(hack_frame, text="Wallhack", fg='yellow', bg='#2b2b2b')
        wallhack_frame.pack(fill='x', padx=10, pady=5)
        
        self.wallhack_enabled = tk.BooleanVar()
        tk.Checkbutton(wallhack_frame, text="Nesne, Obje ve Mobların içinden geç", 
                      variable=self.wallhack_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
        # Restart Here
        restart_frame = tk.LabelFrame(hack_frame, text="Restart Here", fg='orange', bg='#2b2b2b')
        restart_frame.pack(fill='x', padx=10, pady=5)
        
        self.restart_here_enabled = tk.BooleanVar()
        tk.Checkbutton(restart_frame, text="Öldüğünde burada yeniden başla", 
                      variable=self.restart_here_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
        # Upgrade Item Slot 1
        upgrade_frame = tk.LabelFrame(hack_frame, text="Upgrade Item Slot 1", fg='green', bg='#2b2b2b')
        upgrade_frame.pack(fill='x', padx=10, pady=5)
        
        self.upgrade_slot1_enabled = tk.BooleanVar()
        tk.Checkbutton(upgrade_frame, text="1. Slotta bulunan iteme uzaktan + bas", 
                      variable=self.upgrade_slot1_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
    def create_farm_tab(self, notebook):
        """Farm sekmesi"""
        farm_frame = ttk.Frame(notebook)
        notebook.add(farm_frame, text="Farm Sistemi")
        
        # Farm Range
        range_frame = tk.LabelFrame(farm_frame, text="Farm Range", fg='cyan', bg='#2b2b2b')
        range_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(range_frame, text="Farm Alanı:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.farm_range = tk.Scale(range_frame, from_=100, to=1000, orient='horizontal',
                                 bg='#2b2b2b', fg='white')
        self.farm_range.set(500)
        self.farm_range.pack(side='left', padx=5)
        
        # Fixed Position
        pos_frame = tk.LabelFrame(farm_frame, text="Fixed Position", fg='magenta', bg='#2b2b2b')
        pos_frame.pack(fill='x', padx=10, pady=5)
        
        self.fixed_position_enabled = tk.BooleanVar()
        tk.Checkbutton(pos_frame, text="Alanı belirle", variable=self.fixed_position_enabled,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Button(pos_frame, text="Pozisyonu Kaydet", command=self.save_position,
                 bg='#4CAF50', fg='white').pack(side='left', padx=10)
        
        self.position_label = tk.Label(pos_frame, text="Pozisyon: Kaydedilmedi", 
                                     bg='#2b2b2b', fg='white')
        self.position_label.pack(side='left', padx=10)
        
    def create_attack_tab(self, notebook):
        """Saldırı sekmesi"""
        attack_frame = ttk.Frame(notebook)
        notebook.add(attack_frame, text="Saldırı Sistemi")
        
        # Mob Selection
        mob_frame = tk.LabelFrame(attack_frame, text="Mob Seçimi", fg='red', bg='#2b2b2b')
        mob_frame.pack(fill='x', padx=10, pady=5)
        
        self.attack_mobs = tk.BooleanVar()
        tk.Checkbutton(mob_frame, text="Mob", variable=self.attack_mobs,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.attack_stones = tk.BooleanVar()
        tk.Checkbutton(mob_frame, text="Stone", variable=self.attack_stones,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        # Attack Groups
        group_frame = tk.LabelFrame(attack_frame, text="Grup Saldırısı", fg='orange', bg='#2b2b2b')
        group_frame.pack(fill='x', padx=10, pady=5)
        
        self.attack_groups_enabled = tk.BooleanVar()
        tk.Checkbutton(group_frame, text="Birden fazla gruba saldır", 
                      variable=self.attack_groups_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Label(group_frame, text="Grup Adedi:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.group_amount = tk.Scale(group_frame, from_=1, to=10, orient='horizontal',
                                   bg='#2b2b2b', fg='white')
        self.group_amount.set(3)
        self.group_amount.pack(side='left', padx=5)
        
        # Base Skills
        skills_frame = tk.LabelFrame(attack_frame, text="Base Skills", fg='yellow', bg='#2b2b2b')
        skills_frame.pack(fill='x', padx=10, pady=5)
        
        self.base_skills_enabled = tk.BooleanVar()
        tk.Checkbutton(skills_frame, text="Hava Öfke gibi hasar vermeyen base itemleri otomatik yak", 
                      variable=self.base_skills_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
    def create_esp_tab(self, notebook):
        """ESP sekmesi"""
        esp_frame = ttk.Frame(notebook)
        notebook.add(esp_frame, text="ESP Sistemi")
        
        # ESP Players
        player_esp_frame = tk.LabelFrame(esp_frame, text="ESP Player", fg='green', bg='#2b2b2b')
        player_esp_frame.pack(fill='x', padx=10, pady=5)
        
        self.esp_players_enabled = tk.BooleanVar()
        tk.Checkbutton(player_esp_frame, text="Oyuncuları göster", 
                      variable=self.esp_players_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
        # ESP Stones
        stone_esp_frame = tk.LabelFrame(esp_frame, text="ESP Stone", fg='blue', bg='#2b2b2b')
        stone_esp_frame.pack(fill='x', padx=10, pady=5)
        
        self.esp_stones_enabled = tk.BooleanVar()
        tk.Checkbutton(stone_esp_frame, text="Metinleri göster", 
                      variable=self.esp_stones_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(pady=5)
        
    def create_speed_tab(self, notebook):
        """Hız sekmesi"""
        speed_frame = ttk.Frame(notebook)
        notebook.add(speed_frame, text="Hız Ayarları")
        
        # Wait Hack
        wait_frame = tk.LabelFrame(speed_frame, text="Wait Hack", fg='red', bg='#2b2b2b')
        wait_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(wait_frame, text="Yakın Mesafe Hızı:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.wait_hack_speed = tk.Scale(wait_frame, from_=1, to=10, orient='horizontal',
                                      bg='#2b2b2b', fg='white')
        self.wait_hack_speed.set(5)
        self.wait_hack_speed.pack(side='left', padx=5)
        
        self.wait_hack_enabled = tk.BooleanVar()
        tk.Checkbutton(wait_frame, text="Wait Hack Aktif", variable=self.wait_hack_enabled,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=10)
        
        # Wait Hack Range
        range_frame = tk.LabelFrame(speed_frame, text="Wait Hack Range", fg='orange', bg='#2b2b2b')
        range_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(range_frame, text="Uzak Mesafe Hızı:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.wait_hack_range_speed = tk.Scale(range_frame, from_=1, to=10, orient='horizontal',
                                            bg='#2b2b2b', fg='white')
        self.wait_hack_range_speed.set(5)
        self.wait_hack_range_speed.pack(side='left', padx=5)
        
        self.wait_hack_range_enabled = tk.BooleanVar()
        tk.Checkbutton(range_frame, text="Wait Hack Range Aktif", variable=self.wait_hack_range_enabled,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=10)
        
        # Movement Speed
        move_frame = tk.LabelFrame(speed_frame, text="Movement Speed", fg='green', bg='#2b2b2b')
        move_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(move_frame, text="Hareket Hızı:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.movement_speed = tk.Scale(move_frame, from_=1, to=10, orient='horizontal',
                                     bg='#2b2b2b', fg='white')
        self.movement_speed.set(5)
        self.movement_speed.pack(side='left', padx=5)
        
        self.movement_speed_enabled = tk.BooleanVar()
        tk.Checkbutton(move_frame, text="Movement Speed Aktif", variable=self.movement_speed_enabled,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=10)
        
    def create_item_tab(self, notebook):
        """Item sekmesi"""
        item_frame = ttk.Frame(notebook)
        notebook.add(item_frame, text="Item Sistemi")
        
        # Search Item
        search_frame = tk.LabelFrame(item_frame, text="Search Item", fg='cyan', bg='#2b2b2b')
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Item Ara:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.item_search = tk.Entry(search_frame, bg='#3b3b3b', fg='white')
        self.item_search.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Add Item", command=self.add_item,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        # Item List
        list_frame = tk.LabelFrame(item_frame, text="Item Listesi", fg='yellow', bg='#2b2b2b')
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.item_listbox = tk.Listbox(list_frame, bg='#3b3b3b', fg='white')
        self.item_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Item Controls
        item_controls = tk.Frame(list_frame, bg='#2b2b2b')
        item_controls.pack(fill='x', padx=5, pady=5)
        
        tk.Button(item_controls, text="Delete Item", command=self.delete_item,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        tk.Button(item_controls, text="Clear Items", command=self.clear_items,
                 bg='#ff9800', fg='white').pack(side='left', padx=5)
        
        # Pickup Filter
        pickup_frame = tk.LabelFrame(item_frame, text="Pickup Filter", fg='magenta', bg='#2b2b2b')
        pickup_frame.pack(fill='x', padx=10, pady=5)
        
        self.pickup_filter_enabled = tk.BooleanVar()
        tk.Checkbutton(pickup_frame, text="Sadece listeye eklediğiniz itemleri topla", 
                      variable=self.pickup_filter_enabled, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.drop_no_bonus = tk.BooleanVar()
        tk.Checkbutton(pickup_frame, text="Efsunsuz itemleri yere at", 
                      variable=self.drop_no_bonus, bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=10)
        
    def create_whitelist_tab(self, notebook):
        """Whitelist sekmesi"""
        whitelist_frame = ttk.Frame(notebook)
        notebook.add(whitelist_frame, text="Whitelist Sistemi")
        
        # Add to Whitelist
        add_frame = tk.LabelFrame(whitelist_frame, text="Add to Whitelist", fg='green', bg='#2b2b2b')
        add_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(add_frame, text="Player Range:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.player_range = tk.Scale(add_frame, from_=100, to=1000, orient='horizontal',
                                   bg='#2b2b2b', fg='white')
        self.player_range.set(500)
        self.player_range.pack(side='left', padx=5)
        
        tk.Button(add_frame, text="Activate Range", command=self.activate_range,
                 bg='#4CAF50', fg='white').pack(side='left', padx=10)
        
        # Player Search
        search_frame = tk.LabelFrame(whitelist_frame, text="Player Search", fg='blue', bg='#2b2b2b')
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Player Name:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.player_name = tk.Entry(search_frame, bg='#3b3b3b', fg='white')
        self.player_name.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Add Player Manually", command=self.add_player_manually,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        # Whitelist
        whitelist_list_frame = tk.LabelFrame(whitelist_frame, text="Whitelist", fg='yellow', bg='#2b2b2b')
        whitelist_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.whitelist_listbox = tk.Listbox(whitelist_list_frame, bg='#3b3b3b', fg='white')
        self.whitelist_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        tk.Button(whitelist_list_frame, text="Delete from Whitelist", command=self.delete_from_whitelist,
                 bg='#f44336', fg='white').pack(pady=5)
        
        # If Player Actions
        actions_frame = tk.LabelFrame(whitelist_frame, text="If Player Actions", fg='red', bg='#2b2b2b')
        actions_frame.pack(fill='x', padx=10, pady=5)
        
        self.stop_wait_range = tk.BooleanVar()
        tk.Checkbutton(actions_frame, text="Stop Wait+Range", variable=self.stop_wait_range,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.stop_speedhacks = tk.BooleanVar()
        tk.Checkbutton(actions_frame, text="Stop Speedhacks", variable=self.stop_speedhacks,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.stop_bot = tk.BooleanVar()
        tk.Checkbutton(actions_frame, text="Stop Bot", variable=self.stop_bot,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.quit_game = tk.BooleanVar()
        tk.Checkbutton(actions_frame, text="Quit", variable=self.quit_game,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.sound_alarm = tk.BooleanVar()
        tk.Checkbutton(actions_frame, text="Sound Alarm", variable=self.sound_alarm,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
    def create_spam_tab(self, notebook):
        """Spam sekmesi"""
        spam_frame = ttk.Frame(notebook)
        notebook.add(spam_frame, text="Spam Bot")
        
        # Text Input
        text_frame = tk.LabelFrame(spam_frame, text="Text Input", fg='cyan', bg='#2b2b2b')
        text_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(text_frame, text="Text:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.spam_text = tk.Entry(text_frame, bg='#3b3b3b', fg='white')
        self.spam_text.pack(side='left', padx=5, fill='x', expand=True)
        
        # Seconds
        seconds_frame = tk.LabelFrame(spam_frame, text="Timing", fg='yellow', bg='#2b2b2b')
        seconds_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(seconds_frame, text="Seconds:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.spam_seconds = tk.Scale(seconds_frame, from_=1, to=60, orient='horizontal',
                                   bg='#2b2b2b', fg='white')
        self.spam_seconds.set(5)
        self.spam_seconds.pack(side='left', padx=5)
        
        # Spam Controls
        spam_controls = tk.Frame(spam_frame, bg='#2b2b2b')
        spam_controls.pack(fill='x', padx=10, pady=5)
        
        self.start_spam_btn = tk.Button(spam_controls, text="Start Spambot", command=self.start_spam,
                                      bg='#4CAF50', fg='white')
        self.start_spam_btn.pack(side='left', padx=5)
        
        self.stop_spam_btn = tk.Button(spam_controls, text="Stop Spambot", command=self.stop_spam,
                                     bg='#f44336', fg='white')
        self.stop_spam_btn.pack(side='left', padx=5)
        
        self.spam_running = False
        
    def create_fish_tab(self, notebook):
        """Fishing sekmesi"""
        fish_frame = ttk.Frame(notebook)
        notebook.add(fish_frame, text="Fishing Bot")
        
        # Fish Controls
        fish_controls_frame = tk.LabelFrame(fish_frame, text="Fish Controls", fg='blue', bg='#2b2b2b')
        fish_controls_frame.pack(fill='x', padx=10, pady=5)
        
        self.kill_fish = tk.BooleanVar()
        tk.Checkbutton(fish_controls_frame, text="Kill Fish", variable=self.kill_fish,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.grill_fish = tk.BooleanVar()
        tk.Checkbutton(fish_controls_frame, text="Grill Fish", variable=self.grill_fish,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.drop_dead_fish = tk.BooleanVar()
        tk.Checkbutton(fish_controls_frame, text="Drop Dead Fished", variable=self.drop_dead_fish,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.drop_hair_color = tk.BooleanVar()
        tk.Checkbutton(fish_controls_frame, text="Drop Hair Color", variable=self.drop_hair_color,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        # Fish Settings
        fish_settings_frame = tk.LabelFrame(fish_frame, text="Fish Settings", fg='green', bg='#2b2b2b')
        fish_settings_frame.pack(fill='x', padx=10, pady=5)
        
        self.dead_alarm = tk.BooleanVar()
        tk.Checkbutton(fish_settings_frame, text="Dead Alarm", variable=self.dead_alarm,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Label(fish_settings_frame, text="Delay ms:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.fish_delay = tk.Scale(fish_settings_frame, from_=1000, to=5000, orient='horizontal',
                                 bg='#2b2b2b', fg='white')
        self.fish_delay.set(2650)
        self.fish_delay.pack(side='left', padx=5)
        
    def create_route_tab(self, notebook):
        """Route sekmesi"""
        route_frame = ttk.Frame(notebook)
        notebook.add(route_frame, text="Route Sistemi")
        
        # Record Route
        record_frame = tk.LabelFrame(route_frame, text="Record Route", fg='purple', bg='#2b2b2b')
        record_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(record_frame, text="Start Recording", command=self.start_recording,
                 bg='#9C27B0', fg='white').pack(side='left', padx=5)
        
        tk.Button(record_frame, text="Stop Recording", command=self.stop_recording,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        # Route Range
        range_frame = tk.LabelFrame(route_frame, text="Route Range", fg='orange', bg='#2b2b2b')
        range_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(range_frame, text="Farm Range:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.route_farm_range = tk.Scale(range_frame, from_=100, to=1000, orient='horizontal',
                                       bg='#2b2b2b', fg='white')
        self.route_farm_range.set(500)
        self.route_farm_range.pack(side='left', padx=5)
        
        # Route Management
        management_frame = tk.LabelFrame(route_frame, text="Route Management", fg='cyan', bg='#2b2b2b')
        management_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(management_frame, text="Route Name:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.route_name = tk.Entry(management_frame, bg='#3b3b3b', fg='white')
        self.route_name.pack(side='left', padx=5)
        
        tk.Button(management_frame, text="Save", command=self.save_route,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        tk.Button(management_frame, text="Load", command=self.load_route,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        tk.Button(management_frame, text="Delete", command=self.delete_route,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        tk.Button(management_frame, text="Clear Route", command=self.clear_route,
                 bg='#ff9800', fg='white').pack(side='left', padx=5)
        
        # Route List
        route_list_frame = tk.LabelFrame(route_frame, text="Saved Routes", fg='yellow', bg='#2b2b2b')
        route_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.route_listbox = tk.Listbox(route_list_frame, bg='#3b3b3b', fg='white')
        self.route_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Auto Route
        auto_frame = tk.Frame(route_frame, bg='#2b2b2b')
        auto_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(auto_frame, text="Start Auto Route", command=self.start_auto_route,
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold')).pack(side='left', padx=5)
        
        self.recording = False
        self.recorded_route = []
        
    def create_settings_tab(self, notebook):
        """Ayarlar sekmesi"""
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Ayarlar")
        
        # Save/Load Settings
        save_frame = tk.LabelFrame(settings_frame, text="Settings Management", fg='green', bg='#2b2b2b')
        save_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(save_frame, text="Save Settings", command=self.save_settings,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        tk.Button(save_frame, text="Load Settings", command=self.load_settings_file,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        # File Management
        file_frame = tk.LabelFrame(settings_frame, text="File Management", fg='blue', bg='#2b2b2b')
        file_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(file_frame, text="File Name:", bg='#2b2b2b', fg='white').pack(side='left', padx=5)
        self.file_name = tk.Entry(file_frame, bg='#3b3b3b', fg='white')
        self.file_name.pack(side='left', padx=5)
        
        tk.Button(file_frame, text="Save File", command=self.save_file,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        tk.Button(file_frame, text="Load File", command=self.load_file,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        tk.Button(file_frame, text="Delete File", command=self.delete_file,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        # About
        about_frame = tk.LabelFrame(settings_frame, text="About", fg='yellow', bg='#2b2b2b')
        about_frame.pack(fill='x', padx=10, pady=5)
        
        about_text = """
        GGBOT v2 - Mobile2 Global Bot
        Öğretmen ödevi için geliştirilmiş kapsamlı oyun botu
        
        Özellikler:
        - Potion sistemi (Red/Blue)
        - Wallhack ve Restart Here
        - Farm ve saldırı sistemi
        - ESP (Player/Stone)
        - Hız ayarları
        - Item toplama sistemi
        - Whitelist ve oyuncu takibi
        - Spam bot
        - Fishing bot
        - Route kaydetme sistemi
        """
        
        tk.Label(about_frame, text=about_text, bg='#2b2b2b', fg='white', 
                justify='left').pack(padx=5, pady=5)
        
    def load_default_settings(self):
        """Varsayılan ayarları yükler"""
        self.settings = {
            'red_potion_threshold': 30,
            'blue_potion_threshold': 30,
            'red_potion_enabled': False,
            'blue_potion_enabled': False,
            'stop_no_red': False,
            'wallhack_enabled': False,
            'restart_here_enabled': False,
            'upgrade_slot1_enabled': False,
            'farm_range': 500,
            'fixed_position_enabled': False,
            'attack_mobs': True,
            'attack_stones': False,
            'attack_groups_enabled': False,
            'group_amount': 3,
            'base_skills_enabled': False,
            'esp_players_enabled': False,
            'esp_stones_enabled': False,
            'wait_hack_speed': 5,
            'wait_hack_enabled': False,
            'wait_hack_range_speed': 5,
            'wait_hack_range_enabled': False,
            'movement_speed': 5,
            'movement_speed_enabled': False,
            'pickup_filter_enabled': False,
            'drop_no_bonus': False,
            'player_range': 500,
            'stop_wait_range': False,
            'stop_speedhacks': False,
            'stop_bot': False,
            'quit_game': False,
            'sound_alarm': False,
            'spam_text': '',
            'spam_seconds': 5,
            'kill_fish': False,
            'grill_fish': False,
            'drop_dead_fish': False,
            'drop_hair_color': False,
            'dead_alarm': False,
            'fish_delay': 2650,
            'route_farm_range': 500
        }
        
    def load_settings(self):
        """Ayarları dosyadan yükler"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
        
    def save_settings(self):
        """Ayarları dosyaya kaydeder"""
        try:
            settings = {
                'red_potion_threshold': self.red_potion_threshold.get(),
                'blue_potion_threshold': self.blue_potion_threshold.get(),
                'red_potion_enabled': self.red_potion_enabled.get(),
                'blue_potion_enabled': self.blue_potion_enabled.get(),
                'stop_no_red': self.stop_no_red.get(),
                'wallhack_enabled': self.wallhack_enabled.get(),
                'restart_here_enabled': self.restart_here_enabled.get(),
                'upgrade_slot1_enabled': self.upgrade_slot1_enabled.get(),
                'farm_range': self.farm_range.get(),
                'fixed_position_enabled': self.fixed_position_enabled.get(),
                'attack_mobs': self.attack_mobs.get(),
                'attack_stones': self.attack_stones.get(),
                'attack_groups_enabled': self.attack_groups_enabled.get(),
                'group_amount': self.group_amount.get(),
                'base_skills_enabled': self.base_skills_enabled.get(),
                'esp_players_enabled': self.esp_players_enabled.get(),
                'esp_stones_enabled': self.esp_stones_enabled.get(),
                'wait_hack_speed': self.wait_hack_speed.get(),
                'wait_hack_enabled': self.wait_hack_enabled.get(),
                'wait_hack_range_speed': self.wait_hack_range_speed.get(),
                'wait_hack_range_enabled': self.wait_hack_range_enabled.get(),
                'movement_speed': self.movement_speed.get(),
                'movement_speed_enabled': self.movement_speed_enabled.get(),
                'pickup_filter_enabled': self.pickup_filter_enabled.get(),
                'drop_no_bonus': self.drop_no_bonus.get(),
                'player_range': self.player_range.get(),
                'stop_wait_range': self.stop_wait_range.get(),
                'stop_speedhacks': self.stop_speedhacks.get(),
                'stop_bot': self.stop_bot.get(),
                'quit_game': self.quit_game.get(),
                'sound_alarm': self.sound_alarm.get(),
                'spam_text': self.spam_text.get(),
                'spam_seconds': self.spam_seconds.get(),
                'kill_fish': self.kill_fish.get(),
                'grill_fish': self.grill_fish.get(),
                'drop_dead_fish': self.drop_dead_fish.get(),
                'drop_hair_color': self.drop_hair_color.get(),
                'dead_alarm': self.dead_alarm.get(),
                'fish_delay': self.fish_delay.get(),
                'route_farm_range': self.route_farm_range.get()
            }
            
            with open('settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
                
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilemedi: {str(e)}")
            
    def load_settings_file(self):
        """Ayarları dosyadan yükler"""
        try:
            filename = filedialog.askopenfilename(
                title="Ayarları Yükle",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                # Ayarları UI'ya yükle
                self.red_potion_threshold.set(settings.get('red_potion_threshold', 30))
                self.blue_potion_threshold.set(settings.get('blue_potion_threshold', 30))
                self.red_potion_enabled.set(settings.get('red_potion_enabled', False))
                self.blue_potion_enabled.set(settings.get('blue_potion_enabled', False))
                # ... diğer ayarlar
                
                messagebox.showinfo("Başarılı", "Ayarlar yüklendi!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar yüklenemedi: {str(e)}")
            
    def start_bot(self):
        """Botu başlatır"""
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Bot Durumu: Çalışıyor", fg='green')
            
            # Modülleri başlat
            self.potion_system.start()
            self.attack_system.start()
            self.esp_system.start()
            self.speed_system.start()
            self.item_system.start()
            
            self.bot_thread = threading.Thread(target=self.bot_loop, daemon=True)
            self.bot_thread.start()
            messagebox.showinfo("Bot", "Bot başlatıldı!")
            
    def stop_bot(self):
        """Botu durdurur"""
        self.is_running = False
        self.status_label.config(text="Bot Durumu: Durduruldu", fg='red')
        
        # Modülleri durdur
        self.potion_system.stop()
        self.attack_system.stop()
        self.esp_system.stop()
        self.speed_system.stop()
        self.item_system.stop()
        
        messagebox.showinfo("Bot", "Bot durduruldu!")
        
    def bot_loop(self):
        """Ana bot döngüsü"""
        while self.is_running:
            try:
                # Modüllerin durumunu güncelle
                self.potion_system.update_ui_status()
                self.attack_system.update_ui_status()
                self.esp_system.update_ui_status()
                self.speed_system.update_ui_status()
                self.item_system.update_ui_status()
                
                # Farm sistemi
                self.farm_system()
                
                # Fishing bot
                self.fishing_bot()
                
                # Route sistemi
                self.route_system()
                
                time.sleep(0.1)  # 100ms bekleme
                
            except Exception as e:
                print(f"Bot hatası: {e}")
                time.sleep(1)
                
    def farm_system(self):
        """Farm sistemi"""
        # Farm alanı ve pozisyon kontrolü
        pass
        
    def fishing_bot(self):
        """Fishing bot"""
        # Balık yakalama ve işleme
        pass
        
    def route_system(self):
        """Route sistemi"""
        # Kaydedilmiş rotayı takip etme
        pass
        
    # Diğer yardımcı fonksiyonlar
    def save_position(self):
        """Mevcut pozisyonu kaydeder"""
        # Mouse pozisyonunu veya oyun içi koordinatları kaydet
        self.position_label.config(text="Pozisyon: Kaydedildi")
        
    def add_item(self):
        """Item listesine item ekler"""
        item = self.item_search.get()
        if item:
            self.item_listbox.insert(tk.END, item)
            self.item_search.delete(0, tk.END)
            
    def delete_item(self):
        """Seçili itemi siler"""
        selection = self.item_listbox.curselection()
        if selection:
            self.item_listbox.delete(selection[0])
            
    def clear_items(self):
        """Tüm itemleri temizler"""
        self.item_listbox.delete(0, tk.END)
        
    def activate_range(self):
        """Oyuncu aralığını aktif eder"""
        messagebox.showinfo("Range", f"Oyuncu aralığı {self.player_range.get()} piksel olarak ayarlandı")
        
    def add_player_manually(self):
        """Oyuncuyu manuel olarak ekler"""
        player = self.player_name.get()
        if player:
            self.whitelist_listbox.insert(tk.END, player)
            self.player_name.delete(0, tk.END)
            
    def delete_from_whitelist(self):
        """Whitelist'ten oyuncu siler"""
        selection = self.whitelist_listbox.curselection()
        if selection:
            self.whitelist_listbox.delete(selection[0])
            
    def start_spam(self):
        """Spam botu başlatır"""
        if self.spam_text.get():
            self.spam_running = True
            threading.Thread(target=self.spam_loop, daemon=True).start()
            messagebox.showinfo("Spam", "Spam bot başlatıldı!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen spam metni girin!")
            
    def stop_spam(self):
        """Spam botu durdurur"""
        self.spam_running = False
        messagebox.showinfo("Spam", "Spam bot durduruldu!")
        
    def spam_loop(self):
        """Spam döngüsü"""
        while self.spam_running:
            # Spam metnini gönder
            pyautogui.typewrite(self.spam_text.get())
            pyautogui.press('enter')
            time.sleep(self.spam_seconds.get())
            
    def start_recording(self):
        """Route kaydını başlatır"""
        self.recording = True
        self.recorded_route = []
        messagebox.showinfo("Recording", "Route kaydı başlatıldı!")
        
    def stop_recording(self):
        """Route kaydını durdurur"""
        self.recording = False
        messagebox.showinfo("Recording", "Route kaydı durduruldu!")
        
    def save_route(self):
        """Route'u kaydeder"""
        if self.route_name.get() and self.recorded_route:
            filename = f"routes/{self.route_name.get()}.json"
            os.makedirs("routes", exist_ok=True)
            
            with open(filename, 'w') as f:
                json.dump(self.recorded_route, f)
                
            self.route_listbox.insert(tk.END, self.route_name.get())
            messagebox.showinfo("Route", "Route kaydedildi!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen route adı girin ve route kaydedin!")
            
    def load_route(self):
        """Route'u yükler"""
        selection = self.route_listbox.curselection()
        if selection:
            route_name = self.route_listbox.get(selection[0])
            filename = f"routes/{route_name}.json"
            
            try:
                with open(filename, 'r') as f:
                    self.recorded_route = json.load(f)
                messagebox.showinfo("Route", f"Route '{route_name}' yüklendi!")
            except:
                messagebox.showerror("Hata", "Route yüklenemedi!")
                
    def delete_route(self):
        """Route'u siler"""
        selection = self.route_listbox.curselection()
        if selection:
            route_name = self.route_listbox.get(selection[0])
            filename = f"routes/{route_name}.json"
            
            try:
                os.remove(filename)
                self.route_listbox.delete(selection[0])
                messagebox.showinfo("Route", "Route silindi!")
            except:
                messagebox.showerror("Hata", "Route silinemedi!")
                
    def clear_route(self):
        """Route'u temizler"""
        self.recorded_route = []
        messagebox.showinfo("Route", "Route temizlendi!")
        
    def start_auto_route(self):
        """Otomatik route'u başlatır"""
        if self.recorded_route:
            messagebox.showinfo("Auto Route", "Otomatik route başlatıldı!")
            # Route takip kodu buraya gelecek
        else:
            messagebox.showwarning("Uyarı", "Lütfen önce bir route yükleyin!")
            
    def save_file(self):
        """Dosyayı kaydeder"""
        filename = self.file_name.get()
        if filename:
            # Item listesini kaydet
            items = list(self.item_listbox.get(0, tk.END))
            data = {
                'items': items,
                'settings': self.settings
            }
            
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
            messagebox.showinfo("Dosya", "Dosya kaydedildi!")
        else:
            messagebox.showwarning("Uyarı", "Lütfen dosya adı girin!")
            
    def load_file(self):
        """Dosyayı yükler"""
        filename = filedialog.askopenfilename(
            title="Dosya Yükle",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Item listesini yükle
                self.item_listbox.delete(0, tk.END)
                for item in data.get('items', []):
                    self.item_listbox.insert(tk.END, item)
                    
                messagebox.showinfo("Dosya", "Dosya yüklendi!")
            except:
                messagebox.showerror("Hata", "Dosya yüklenemedi!")
                
    def delete_file(self):
        """Dosyayı siler"""
        filename = filedialog.askopenfilename(
            title="Dosya Sil",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                os.remove(filename)
                messagebox.showinfo("Dosya", "Dosya silindi!")
            except:
                messagebox.showerror("Hata", "Dosya silinemedi!")
                
    def run(self):
        """Botu çalıştırır"""
        self.root.mainloop()

if __name__ == "__main__":
    bot = GGBot()
    bot.run()