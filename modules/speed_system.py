#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Speed System Module for GGBOT v2
Wait Hack ve Movement Speed hızlandırma sistemi
"""

import time
import threading
import pyautogui
import keyboard
import mouse
import tkinter as tk
from ctypes import windll, c_long, c_ulong, c_short, c_ushort, byref, Structure, Union, c_char, c_uint, sizeof, c_void_p

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

class SpeedSystem:
    def __init__(self, parent_bot):
        self.parent_bot = parent_bot
        self.is_running = False
        
        # Wait Hack ayarları
        self.wait_hack_enabled = False
        self.wait_hack_speed = 5
        self.wait_hack_range_enabled = False
        self.wait_hack_range_speed = 5
        
        # Movement Speed ayarları
        self.movement_speed_enabled = False
        self.movement_speed = 5
        
        # Hız çarpanları
        self.speed_multipliers = {
            1: 0.1,
            2: 0.2,
            3: 0.3,
            4: 0.4,
            5: 0.5,
            6: 0.6,
            7: 0.7,
            8: 0.8,
            9: 0.9,
            10: 1.0
        }
        
        # Windows API fonksiyonları
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        
        # Saldırı hızı ayarları
        self.attack_speed_multiplier = 1.0
        self.movement_speed_multiplier = 1.0
        
        # Thread'ler
        self.wait_hack_thread = None
        self.movement_thread = None
        
    def start(self):
        """Hız sistemini başlatır"""
        self.is_running = True
        
        if self.wait_hack_enabled:
            self.start_wait_hack()
            
        if self.movement_speed_enabled:
            self.start_movement_speed()
            
        print("Hız sistemi başlatıldı")
        
    def stop(self):
        """Hız sistemini durdurur"""
        self.is_running = False
        
        if self.wait_hack_thread:
            self.wait_hack_thread.join()
            
        if self.movement_thread:
            self.movement_thread.join()
            
        print("Hız sistemi durduruldu")
        
    def start_wait_hack(self):
        """Wait Hack'i başlatır"""
        self.wait_hack_thread = threading.Thread(target=self.wait_hack_loop, daemon=True)
        self.wait_hack_thread.start()
        print("Wait Hack başlatıldı")
        
    def start_movement_speed(self):
        """Movement Speed'i başlatır"""
        self.movement_thread = threading.Thread(target=self.movement_speed_loop, daemon=True)
        self.movement_thread.start()
        print("Movement Speed başlatıldı")
        
    def wait_hack_loop(self):
        """Wait Hack döngüsü"""
        while self.is_running and self.wait_hack_enabled:
            try:
                # Saldırı tuşuna basılıp basılmadığını kontrol et
                if keyboard.is_pressed('space'):  # Saldırı tuşu
                    self.apply_wait_hack()
                    
                time.sleep(0.01)  # 10ms bekleme
                
            except Exception as e:
                print(f"Wait Hack hatası: {e}")
                time.sleep(0.1)
                
    def movement_speed_loop(self):
        """Movement Speed döngüsü"""
        while self.is_running and self.movement_speed_enabled:
            try:
                # Hareket tuşlarına basılıp basılmadığını kontrol et
                if (keyboard.is_pressed('w') or keyboard.is_pressed('a') or 
                    keyboard.is_pressed('s') or keyboard.is_pressed('d')):
                    self.apply_movement_speed()
                    
                time.sleep(0.01)  # 10ms bekleme
                
            except Exception as e:
                print(f"Movement Speed hatası: {e}")
                time.sleep(0.1)
                
    def apply_wait_hack(self):
        """Wait Hack'i uygular"""
        try:
            # Saldırı hızını artır
            speed_multiplier = self.speed_multipliers.get(self.wait_hack_speed, 0.5)
            
            # Animasyon süresini kısalt
            time.sleep(0.01 * speed_multiplier)
            
            # Hızlı saldırı tuşu basma
            pyautogui.press('space')
            
        except Exception as e:
            print(f"Wait Hack uygulama hatası: {e}")
            
    def apply_movement_speed(self):
        """Movement Speed'i uygular"""
        try:
            # Hareket hızını artır
            speed_multiplier = self.speed_multipliers.get(self.movement_speed, 0.5)
            
            # Hareket tuşlarını hızlı basma
            if keyboard.is_pressed('w'):
                self.rapid_key_press('w', speed_multiplier)
            if keyboard.is_pressed('a'):
                self.rapid_key_press('a', speed_multiplier)
            if keyboard.is_pressed('s'):
                self.rapid_key_press('s', speed_multiplier)
            if keyboard.is_pressed('d'):
                self.rapid_key_press('d', speed_multiplier)
                
        except Exception as e:
            print(f"Movement Speed uygulama hatası: {e}")
            
    def rapid_key_press(self, key, multiplier):
        """Hızlı tuş basma"""
        try:
            # Tuşu hızlı basma
            for _ in range(int(5 * multiplier)):
                pyautogui.press(key)
                time.sleep(0.001)  # 1ms bekleme
                
        except Exception as e:
            print(f"Hızlı tuş basma hatası: {e}")
            
    def set_wait_hack_speed(self, speed):
        """Wait Hack hızını ayarlar"""
        self.wait_hack_speed = speed
        print(f"Wait Hack hızı: {speed}")
        
    def set_movement_speed(self, speed):
        """Movement Speed'i ayarlar"""
        self.movement_speed = speed
        print(f"Movement Speed: {speed}")
        
    def update_settings(self, settings):
        """Ayarları günceller"""
        self.wait_hack_enabled = settings.get('wait_hack_enabled', False)
        self.wait_hack_speed = settings.get('wait_hack_speed', 5)
        self.wait_hack_range_enabled = settings.get('wait_hack_range_enabled', False)
        self.wait_hack_range_speed = settings.get('wait_hack_range_speed', 5)
        self.movement_speed_enabled = settings.get('movement_speed_enabled', False)
        self.movement_speed = settings.get('movement_speed', 5)
        
    def create_speed_ui(self, parent_frame):
        """Hız sistemi için UI oluşturur"""
        speed_frame = tk.LabelFrame(parent_frame, text="Hız Sistemi", fg='yellow', bg='#2b2b2b')
        speed_frame.pack(fill='x', padx=10, pady=5)
        
        # Wait Hack
        wait_frame = tk.LabelFrame(speed_frame, text="Wait Hack", fg='red', bg='#2b2b2b')
        wait_frame.pack(fill='x', padx=5, pady=2)
        
        self.wait_hack_var = tk.BooleanVar(value=self.wait_hack_enabled)
        tk.Checkbutton(wait_frame, text="Wait Hack Aktif", variable=self.wait_hack_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Label(wait_frame, text="Hız:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.wait_hack_speed_var = tk.IntVar(value=self.wait_hack_speed)
        wait_scale = tk.Scale(wait_frame, from_=1, to=10, orient='horizontal',
                             variable=self.wait_hack_speed_var, bg='#2b2b2b', fg='white')
        wait_scale.pack(side='left', padx=5)
        
        # Wait Hack Range
        wait_range_frame = tk.LabelFrame(speed_frame, text="Wait Hack Range", fg='orange', bg='#2b2b2b')
        wait_range_frame.pack(fill='x', padx=5, pady=2)
        
        self.wait_hack_range_var = tk.BooleanVar(value=self.wait_hack_range_enabled)
        tk.Checkbutton(wait_range_frame, text="Wait Hack Range Aktif", variable=self.wait_hack_range_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Label(wait_range_frame, text="Hız:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.wait_hack_range_speed_var = tk.IntVar(value=self.wait_hack_range_speed)
        wait_range_scale = tk.Scale(wait_range_frame, from_=1, to=10, orient='horizontal',
                                   variable=self.wait_hack_range_speed_var, bg='#2b2b2b', fg='white')
        wait_range_scale.pack(side='left', padx=5)
        
        # Movement Speed
        movement_frame = tk.LabelFrame(speed_frame, text="Movement Speed", fg='green', bg='#2b2b2b')
        movement_frame.pack(fill='x', padx=5, pady=2)
        
        self.movement_speed_var = tk.BooleanVar(value=self.movement_speed_enabled)
        tk.Checkbutton(movement_frame, text="Movement Speed Aktif", variable=self.movement_speed_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Label(movement_frame, text="Hız:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.movement_speed_scale_var = tk.IntVar(value=self.movement_speed)
        movement_scale = tk.Scale(movement_frame, from_=1, to=10, orient='horizontal',
                                 variable=self.movement_speed_scale_var, bg='#2b2b2b', fg='white')
        movement_scale.pack(side='left', padx=5)
        
        # Kontroller
        control_frame = tk.Frame(speed_frame, bg='#2b2b2b')
        control_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(control_frame, text="Hız Testi", command=self.speed_test,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        tk.Button(control_frame, text="Ayarları Uygula", command=self.apply_speed_settings,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        # Durum gösterimi
        status_frame = tk.Frame(speed_frame, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="Hız Sistemi: Durduruldu", 
                                   bg='#2b2b2b', fg='white')
        self.status_label.pack(side='left')
        
    def speed_test(self):
        """Hız testi yapar"""
        print("Hız testi başlatılıyor...")
        
        # Test mesajı
        test_message = "Hız testi - 5 saniye boyunca tuşlara basın"
        print(test_message)
        
        # Test süresi
        test_duration = 5
        start_time = time.time()
        
        while time.time() - start_time < test_duration:
            if keyboard.is_pressed('space'):
                print("Saldırı tuşu test ediliyor...")
                time.sleep(0.1)
                
            if (keyboard.is_pressed('w') or keyboard.is_pressed('a') or 
                keyboard.is_pressed('s') or keyboard.is_pressed('d')):
                print("Hareket tuşları test ediliyor...")
                time.sleep(0.1)
                
        print("Hız testi tamamlandı!")
        
    def apply_speed_settings(self):
        """Hız ayarlarını uygular"""
        self.wait_hack_enabled = self.wait_hack_var.get()
        self.wait_hack_speed = self.wait_hack_speed_var.get()
        self.wait_hack_range_enabled = self.wait_hack_range_var.get()
        self.wait_hack_range_speed = self.wait_hack_range_speed_var.get()
        self.movement_speed_enabled = self.movement_speed_var.get()
        self.movement_speed = self.movement_speed_scale_var.get()
        
        print("Hız ayarları uygulandı!")
        
    def update_ui_status(self):
        """UI durumunu günceller"""
        if hasattr(self, 'status_label'):
            status = "Çalışıyor" if self.is_running else "Durduruldu"
            self.status_label.config(text=f"Hız Sistemi: {status}")
            
    def get_speed_info(self):
        """Hız bilgilerini döndürür"""
        return {
            'wait_hack_enabled': self.wait_hack_enabled,
            'wait_hack_speed': self.wait_hack_speed,
            'wait_hack_range_enabled': self.wait_hack_range_enabled,
            'wait_hack_range_speed': self.wait_hack_range_speed,
            'movement_speed_enabled': self.movement_speed_enabled,
            'movement_speed': self.movement_speed
        }
        
    def set_attack_key(self, key):
        """Saldırı tuşunu ayarlar"""
        self.attack_key = key
        print(f"Saldırı tuşu: {key}")
        
    def set_movement_keys(self, keys):
        """Hareket tuşlarını ayarlar"""
        self.movement_keys = keys
        print(f"Hareket tuşları: {keys}")
        
    def enable_auto_speed(self):
        """Otomatik hız ayarını etkinleştirir"""
        # Oyun durumuna göre otomatik hız ayarı
        pass
        
    def disable_auto_speed(self):
        """Otomatik hız ayarını devre dışı bırakır"""
        pass
        
    def reset_speed_settings(self):
        """Hız ayarlarını sıfırlar"""
        self.wait_hack_enabled = False
        self.wait_hack_speed = 5
        self.wait_hack_range_enabled = False
        self.wait_hack_range_speed = 5
        self.movement_speed_enabled = False
        self.movement_speed = 5
        
        print("Hız ayarları sıfırlandı!")
        
    def create_speed_presets(self):
        """Hız ön ayarları oluşturur"""
        presets = {
            'Yavaş': {
                'wait_hack_speed': 3,
                'movement_speed': 3
            },
            'Normal': {
                'wait_hack_speed': 5,
                'movement_speed': 5
            },
            'Hızlı': {
                'wait_hack_speed': 7,
                'movement_speed': 7
            },
            'Çok Hızlı': {
                'wait_hack_speed': 9,
                'movement_speed': 9
            }
        }
        
        return presets
        
    def apply_preset(self, preset_name):
        """Ön ayarı uygular"""
        presets = self.create_speed_presets()
        
        if preset_name in presets:
            preset = presets[preset_name]
            self.wait_hack_speed = preset['wait_hack_speed']
            self.movement_speed = preset['movement_speed']
            print(f"Ön ayar uygulandı: {preset_name}")
        else:
            print(f"Ön ayar bulunamadı: {preset_name}")