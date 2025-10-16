#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Potion ve temel özellikler sekmesi
"""

import tkinter as tk
from tkinter import ttk

class PotionTab:
    """Potion sekmesi"""
    
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """UI'yi kur"""
        # Ana scroll frame
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Red Potion grubu
        red_group = ttk.LabelFrame(scrollable_frame, text="Red Potion", padding=10)
        red_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.red_enabled = tk.BooleanVar()
        red_check = ttk.Checkbutton(red_group, text="Red Potion Aktif", 
                                   variable=self.red_enabled)
        red_check.pack(anchor=tk.W)
        
        red_frame = ttk.Frame(red_group)
        red_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(red_frame, text="Can Yüzdesi:").pack(side=tk.LEFT)
        self.red_percentage = tk.IntVar(value=50)
        red_spin = ttk.Spinbox(red_frame, from_=1, to=99, width=10, 
                              textvariable=self.red_percentage)
        red_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(red_frame, text="%").pack(side=tk.LEFT)
        
        key_frame = ttk.Frame(red_group)
        key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(key_frame, text="Tuş:").pack(side=tk.LEFT)
        self.red_key = tk.StringVar(value="F1")
        red_key_entry = ttk.Entry(key_frame, width=10, textvariable=self.red_key)
        red_key_entry.pack(side=tk.LEFT, padx=5)
        
        # Blue Potion grubu
        blue_group = ttk.LabelFrame(scrollable_frame, text="Blue Potion", padding=10)
        blue_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.blue_enabled = tk.BooleanVar()
        blue_check = ttk.Checkbutton(blue_group, text="Blue Potion Aktif", 
                                    variable=self.blue_enabled)
        blue_check.pack(anchor=tk.W)
        
        blue_frame = ttk.Frame(blue_group)
        blue_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(blue_frame, text="Mana Yüzdesi:").pack(side=tk.LEFT)
        self.blue_percentage = tk.IntVar(value=30)
        blue_spin = ttk.Spinbox(blue_frame, from_=1, to=99, width=10, 
                               textvariable=self.blue_percentage)
        blue_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(blue_frame, text="%").pack(side=tk.LEFT)
        
        blue_key_frame = ttk.Frame(blue_group)
        blue_key_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(blue_key_frame, text="Tuş:").pack(side=tk.LEFT)
        self.blue_key = tk.StringVar(value="F2")
        blue_key_entry = ttk.Entry(blue_key_frame, width=10, textvariable=self.blue_key)
        blue_key_entry.pack(side=tk.LEFT, padx=5)
        
        # Wallhack grubu
        hack_group = ttk.LabelFrame(scrollable_frame, text="Hack Özellikleri", padding=10)
        hack_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.wallhack_enabled = tk.BooleanVar()
        wallhack_check = ttk.Checkbutton(hack_group, text="Wallhack (Nesnelerin içinden geçme)", 
                                        variable=self.wallhack_enabled)
        wallhack_check.pack(anchor=tk.W, pady=2)
        
        self.restart_here_enabled = tk.BooleanVar()
        restart_check = ttk.Checkbutton(hack_group, text="Restart Here (Öldüğünde burada yeniden başla)", 
                                       variable=self.restart_here_enabled)
        restart_check.pack(anchor=tk.W, pady=2)
        
        # Restart Here pozisyon ayarları
        restart_frame = ttk.Frame(hack_group)
        restart_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(restart_frame, text="Pozisyon X:").pack(side=tk.LEFT)
        self.restart_x = tk.IntVar(value=0)
        restart_x_entry = ttk.Entry(restart_frame, width=10, textvariable=self.restart_x)
        restart_x_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(restart_frame, text="Y:").pack(side=tk.LEFT, padx=(10, 0))
        self.restart_y = tk.IntVar(value=0)
        restart_y_entry = ttk.Entry(restart_frame, width=10, textvariable=self.restart_y)
        restart_y_entry.pack(side=tk.LEFT, padx=5)
        
        set_pos_btn = ttk.Button(restart_frame, text="Mevcut Pozisyonu Ayarla", 
                                command=self.set_current_position)
        set_pos_btn.pack(side=tk.LEFT, padx=10)
        
        # Upgrade Item Slot 1
        self.upgrade_slot1_enabled = tk.BooleanVar()
        upgrade_check = ttk.Checkbutton(hack_group, text="Upgrade Item Slot 1 (1. slotta bulunan iteme uzaktan + bas)", 
                                       variable=self.upgrade_slot1_enabled)
        upgrade_check.pack(anchor=tk.W, pady=2)
        
        upgrade_frame = ttk.Frame(hack_group)
        upgrade_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(upgrade_frame, text="Upgrade Tuşu:").pack(side=tk.LEFT)
        self.upgrade_key = tk.StringVar(value="+")
        upgrade_key_entry = ttk.Entry(upgrade_frame, width=10, textvariable=self.upgrade_key)
        upgrade_key_entry.pack(side=tk.LEFT, padx=5)
        
        # Farm ayarları
        farm_group = ttk.LabelFrame(scrollable_frame, text="Farm Ayarları", padding=10)
        farm_group.pack(fill=tk.X, padx=5, pady=5)
        
        farm_range_frame = ttk.Frame(farm_group)
        farm_range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(farm_range_frame, text="Farm Range:").pack(side=tk.LEFT)
        self.farm_range = tk.IntVar(value=100)
        farm_range_spin = ttk.Spinbox(farm_range_frame, from_=50, to=500, width=10, 
                                     textvariable=self.farm_range)
        farm_range_spin.pack(side=tk.LEFT, padx=5)
        
        # Fixed Position
        self.fixed_position_enabled = tk.BooleanVar()
        fixed_pos_check = ttk.Checkbutton(farm_group, text="Fixed Position (Alanı belirle)", 
                                         variable=self.fixed_position_enabled)
        fixed_pos_check.pack(anchor=tk.W, pady=2)
        
        fixed_pos_frame = ttk.Frame(farm_group)
        fixed_pos_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fixed_pos_frame, text="X:").pack(side=tk.LEFT)
        self.fixed_x = tk.IntVar(value=0)
        fixed_x_entry = ttk.Entry(fixed_pos_frame, width=10, textvariable=self.fixed_x)
        fixed_x_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(fixed_pos_frame, text="Y:").pack(side=tk.LEFT, padx=(10, 0))
        self.fixed_y = tk.IntVar(value=0)
        fixed_y_entry = ttk.Entry(fixed_pos_frame, width=10, textvariable=self.fixed_y)
        fixed_y_entry.pack(side=tk.LEFT, padx=5)
        
        set_fixed_btn = ttk.Button(fixed_pos_frame, text="Mevcut Pozisyonu Ayarla", 
                                  command=self.set_fixed_position)
        set_fixed_btn.pack(side=tk.LEFT, padx=10)
        
    def set_current_position(self):
        """Mevcut pozisyonu restart pozisyonu olarak ayarla"""
        # Bu fonksiyon gerçek oyunda mouse pozisyonunu alacak
        # Şimdilik simüle ediyoruz
        import pyautogui
        x, y = pyautogui.position()
        self.restart_x.set(x)
        self.restart_y.set(y)
        tk.messagebox.showinfo("Pozisyon Ayarlandı", f"Restart pozisyonu: ({x}, {y})")
        
    def set_fixed_position(self):
        """Mevcut pozisyonu fixed pozisyon olarak ayarla"""
        import pyautogui
        x, y = pyautogui.position()
        self.fixed_x.set(x)
        self.fixed_y.set(y)
        tk.messagebox.showinfo("Pozisyon Ayarlandı", f"Fixed pozisyon: ({x}, {y})")
        
    def load_settings(self):
        """Ayarları yükle"""
        # Red Potion
        self.red_enabled.set(self.settings.get("red_potion.enabled", True))
        self.red_percentage.set(self.settings.get("red_potion.health_percentage", 50))
        self.red_key.set(self.settings.get("red_potion.key", "F1"))
        
        # Blue Potion
        self.blue_enabled.set(self.settings.get("blue_potion.enabled", True))
        self.blue_percentage.set(self.settings.get("blue_potion.mana_percentage", 30))
        self.blue_key.set(self.settings.get("blue_potion.key", "F2"))
        
        # Hack özellikleri
        self.wallhack_enabled.set(self.settings.get("wallhack.enabled", False))
        self.restart_here_enabled.set(self.settings.get("restart_here.enabled", False))
        self.restart_x.set(self.settings.get("restart_here.position.x", 0))
        self.restart_y.set(self.settings.get("restart_here.position.y", 0))
        
        self.upgrade_slot1_enabled.set(self.settings.get("upgrade_item_slot1.enabled", False))
        self.upgrade_key.set(self.settings.get("upgrade_item_slot1.key", "+"))
        
        # Farm ayarları
        self.farm_range.set(self.settings.get("farm.range", 100))
        self.fixed_position_enabled.set(self.settings.get("farm.fixed_position.enabled", False))
        self.fixed_x.set(self.settings.get("farm.fixed_position.x", 0))
        self.fixed_y.set(self.settings.get("farm.fixed_position.y", 0))
        
    def save_settings(self):
        """Ayarları kaydet"""
        # Red Potion
        self.settings.set("red_potion.enabled", self.red_enabled.get())
        self.settings.set("red_potion.health_percentage", self.red_percentage.get())
        self.settings.set("red_potion.key", self.red_key.get())
        
        # Blue Potion
        self.settings.set("blue_potion.enabled", self.blue_enabled.get())
        self.settings.set("blue_potion.mana_percentage", self.blue_percentage.get())
        self.settings.set("blue_potion.key", self.blue_key.get())
        
        # Hack özellikleri
        self.settings.set("wallhack.enabled", self.wallhack_enabled.get())
        self.settings.set("restart_here.enabled", self.restart_here_enabled.get())
        self.settings.set("restart_here.position.x", self.restart_x.get())
        self.settings.set("restart_here.position.y", self.restart_y.get())
        
        self.settings.set("upgrade_item_slot1.enabled", self.upgrade_slot1_enabled.get())
        self.settings.set("upgrade_item_slot1.key", self.upgrade_key.get())
        
        # Farm ayarları
        self.settings.set("farm.range", self.farm_range.get())
        self.settings.set("farm.fixed_position.enabled", self.fixed_position_enabled.get())
        self.settings.set("farm.fixed_position.x", self.fixed_x.get())
        self.settings.set("farm.fixed_position.y", self.fixed_y.get())