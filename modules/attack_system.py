#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Attack System Module for GGBOT v2
Mob ve Stone saldırı sistemi
"""

import cv2
import numpy as np
import pyautogui
import time
import threading
import random
from PIL import Image, ImageTk
import tkinter as tk

class AttackSystem:
    def __init__(self, parent_bot):
        self.parent_bot = parent_bot
        self.is_running = False
        
        # Saldırı ayarları
        self.attack_mobs = True
        self.attack_stones = False
        self.attack_groups_enabled = False
        self.group_amount = 3
        self.base_skills_enabled = False
        
        # Saldırı tuşları
        self.attack_key = 'space'  # Saldırı tuşu
        self.skill_keys = ['q', 'w', 'e', 'r']  # Skill tuşları
        
        # Mob/Stone tespit ayarları
        self.mob_color_range = {
            'lower': np.array([0, 0, 100]),     # Kırmızımsı renkler
            'upper': np.array([20, 255, 255])
        }
        
        self.stone_color_range = {
            'lower': np.array([100, 50, 50]),   # Gri renkler
            'upper': np.array([130, 255, 255])
        }
        
        # Saldırı aralığı
        self.attack_range = 200  # Piksel cinsinden
        self.attack_cooldown = 0.5  # Saniye
        
        # Son saldırı zamanı
        self.last_attack_time = 0
        
        # Hedef listesi
        self.targets = []
        self.current_target = None
        
    def start(self):
        """Saldırı sistemini başlatır"""
        self.is_running = True
        self.attack_thread = threading.Thread(target=self.attack_loop, daemon=True)
        self.attack_thread.start()
        print("Saldırı sistemi başlatıldı")
        
    def stop(self):
        """Saldırı sistemini durdurur"""
        self.is_running = False
        print("Saldırı sistemi durduruldu")
        
    def attack_loop(self):
        """Ana saldırı döngüsü"""
        while self.is_running:
            try:
                # Hedefleri tespit et
                self.detect_targets()
                
                # Saldırı yap
                if self.targets:
                    self.perform_attack()
                    
                # Base skill kullan
                if self.base_skills_enabled:
                    self.use_base_skills()
                    
                time.sleep(0.1)  # 100ms bekleme
                
            except Exception as e:
                print(f"Saldırı sistemi hatası: {e}")
                time.sleep(1)
                
    def detect_targets(self):
        """Hedefleri tespit eder"""
        try:
            # Ekran görüntüsü al
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            self.targets = []
            
            # Mob tespiti
            if self.attack_mobs:
                mobs = self.detect_mobs(img)
                self.targets.extend(mobs)
                
            # Stone tespiti
            if self.attack_stones:
                stones = self.detect_stones(img)
                self.targets.extend(stones)
                
            # Hedefleri mesafeye göre sırala
            self.targets.sort(key=lambda x: x['distance'])
            
        except Exception as e:
            print(f"Hedef tespit hatası: {e}")
            
    def detect_mobs(self, img):
        """Mob'ları tespit eder"""
        mobs = []
        try:
            # HSV'ye çevir
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Mob rengi aralığına göre maske oluştur
            mask = cv2.inRange(hsv, self.mob_color_range['lower'], self.mob_color_range['upper'])
            
            # Konturları bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Kontur alanını kontrol et
                area = cv2.contourArea(contour)
                if area > 100:  # Minimum alan
                    # Merkez noktasını hesapla
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Mesafeyi hesapla
                        distance = self.calculate_distance(cx, cy)
                        
                        if distance <= self.attack_range:
                            mobs.append({
                                'type': 'mob',
                                'x': cx,
                                'y': cy,
                                'distance': distance,
                                'area': area
                            })
                            
        except Exception as e:
            print(f"Mob tespit hatası: {e}")
            
        return mobs
        
    def detect_stones(self, img):
        """Stone'ları tespit eder"""
        stones = []
        try:
            # HSV'ye çevir
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Stone rengi aralığına göre maske oluştur
            mask = cv2.inRange(hsv, self.stone_color_range['lower'], self.stone_color_range['upper'])
            
            # Konturları bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Kontur alanını kontrol et
                area = cv2.contourArea(contour)
                if area > 50:  # Minimum alan
                    # Merkez noktasını hesapla
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Mesafeyi hesapla
                        distance = self.calculate_distance(cx, cy)
                        
                        if distance <= self.attack_range:
                            stones.append({
                                'type': 'stone',
                                'x': cx,
                                'y': cy,
                                'distance': distance,
                                'area': area
                            })
                            
        except Exception as e:
            print(f"Stone tespit hatası: {e}")
            
        return stones
        
    def calculate_distance(self, x, y):
        """Mesafeyi hesaplar"""
        # Ekran merkezinden mesafe
        screen_center_x = pyautogui.size().width // 2
        screen_center_y = pyautogui.size().height // 2
        
        distance = ((x - screen_center_x) ** 2 + (y - screen_center_y) ** 2) ** 0.5
        return distance
        
    def perform_attack(self):
        """Saldırı gerçekleştirir"""
        current_time = time.time()
        
        # Cooldown kontrolü
        if current_time - self.last_attack_time < self.attack_cooldown:
            return
            
        # Grup saldırısı
        if self.attack_groups_enabled:
            self.attack_groups()
        else:
            # Tek hedef saldırısı
            if self.targets:
                target = self.targets[0]
                self.attack_target(target)
                
        self.last_attack_time = current_time
        
    def attack_groups(self):
        """Grup saldırısı yapar"""
        try:
            # Belirtilen sayıda hedefe saldır
            targets_to_attack = self.targets[:self.group_amount]
            
            for target in targets_to_attack:
                self.attack_target(target)
                time.sleep(0.1)  # Hedefler arası kısa bekleme
                
        except Exception as e:
            print(f"Grup saldırı hatası: {e}")
            
    def attack_target(self, target):
        """Belirli bir hedefe saldırır"""
        try:
            # Hedefe odaklan
            self.focus_target(target)
            
            # Saldırı tuşuna bas
            pyautogui.press(self.attack_key)
            
            print(f"{target['type']} saldırısı: ({target['x']}, {target['y']}) - Mesafe: {target['distance']:.1f}")
            
        except Exception as e:
            print(f"Hedef saldırı hatası: {e}")
            
    def focus_target(self, target):
        """Hedefe odaklanır"""
        try:
            # Mouse'u hedefe yönlendir
            pyautogui.moveTo(target['x'], target['y'], duration=0.1)
            
            # Kısa süre bekle
            time.sleep(0.05)
            
        except Exception as e:
            print(f"Hedef odaklama hatası: {e}")
            
    def use_base_skills(self):
        """Base skill'leri kullanır"""
        try:
            # Rastgele skill tuşuna bas
            skill_key = random.choice(self.skill_keys)
            pyautogui.press(skill_key)
            
            print(f"Base skill kullanıldı: {skill_key}")
            
        except Exception as e:
            print(f"Base skill hatası: {e}")
            
    def update_settings(self, settings):
        """Ayarları günceller"""
        self.attack_mobs = settings.get('attack_mobs', True)
        self.attack_stones = settings.get('attack_stones', False)
        self.attack_groups_enabled = settings.get('attack_groups_enabled', False)
        self.group_amount = settings.get('group_amount', 3)
        self.base_skills_enabled = settings.get('base_skills_enabled', False)
        
    def set_attack_range(self, range_value):
        """Saldırı aralığını ayarlar"""
        self.attack_range = range_value
        print(f"Saldırı aralığı: {range_value} piksel")
        
    def set_attack_cooldown(self, cooldown):
        """Saldırı cooldown'unu ayarlar"""
        self.attack_cooldown = cooldown
        print(f"Saldırı cooldown: {cooldown} saniye")
        
    def create_attack_ui(self, parent_frame):
        """Saldırı sistemi için UI oluşturur"""
        attack_frame = tk.LabelFrame(parent_frame, text="Saldırı Sistemi", fg='red', bg='#2b2b2b')
        attack_frame.pack(fill='x', padx=10, pady=5)
        
        # Hedef seçimi
        target_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        target_frame.pack(fill='x', padx=5, pady=2)
        
        self.attack_mobs_var = tk.BooleanVar(value=self.attack_mobs)
        tk.Checkbutton(target_frame, text="Mob", variable=self.attack_mobs_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.attack_stones_var = tk.BooleanVar(value=self.attack_stones)
        tk.Checkbutton(target_frame, text="Stone", variable=self.attack_stones_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        # Grup saldırısı
        group_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        group_frame.pack(fill='x', padx=5, pady=2)
        
        self.attack_groups_var = tk.BooleanVar(value=self.attack_groups_enabled)
        tk.Checkbutton(group_frame, text="Grup Saldırısı", variable=self.attack_groups_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        tk.Label(group_frame, text="Grup Adedi:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.group_amount_var = tk.IntVar(value=self.group_amount)
        group_scale = tk.Scale(group_frame, from_=1, to=10, orient='horizontal',
                              variable=self.group_amount_var, bg='#2b2b2b', fg='white')
        group_scale.pack(side='left', padx=5)
        
        # Base Skills
        skills_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        skills_frame.pack(fill='x', padx=5, pady=2)
        
        self.base_skills_var = tk.BooleanVar(value=self.base_skills_enabled)
        tk.Checkbutton(skills_frame, text="Base Skills Otomatik", variable=self.base_skills_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        # Saldırı ayarları
        settings_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        settings_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(settings_frame, text="Saldırı Aralığı:", bg='#2b2b2b', fg='white').pack(side='left')
        self.attack_range_var = tk.IntVar(value=self.attack_range)
        range_scale = tk.Scale(settings_frame, from_=100, to=500, orient='horizontal',
                              variable=self.attack_range_var, bg='#2b2b2b', fg='white')
        range_scale.pack(side='left', padx=5)
        
        tk.Label(settings_frame, text="Cooldown:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.attack_cooldown_var = tk.DoubleVar(value=self.attack_cooldown)
        cooldown_scale = tk.Scale(settings_frame, from_=0.1, to=2.0, resolution=0.1, orient='horizontal',
                                 variable=self.attack_cooldown_var, bg='#2b2b2b', fg='white')
        cooldown_scale.pack(side='left', padx=5)
        
        # Durum gösterimi
        status_frame = tk.Frame(attack_frame, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="Saldırı Sistemi: Durduruldu", 
                                   bg='#2b2b2b', fg='white')
        self.status_label.pack(side='left')
        
        self.target_count_label = tk.Label(status_frame, text="Hedef: 0", 
                                         bg='#2b2b2b', fg='white')
        self.target_count_label.pack(side='right')
        
    def update_ui_status(self):
        """UI durumunu günceller"""
        if hasattr(self, 'status_label'):
            status = "Çalışıyor" if self.is_running else "Durduruldu"
            self.status_label.config(text=f"Saldırı Sistemi: {status}")
            
        if hasattr(self, 'target_count_label'):
            self.target_count_label.config(text=f"Hedef: {len(self.targets)}")
            
    def calibrate_colors(self):
        """Renk kalibrasyonu yapar"""
        print("Renk kalibrasyonu başlatılıyor...")
        print("Lütfen mob/stone rengini seçin")
        
        # Mob rengi kalibrasyonu
        mob_color = self.select_color("Mob rengini seçin")
        if mob_color:
            self.mob_color_range = self.create_color_range(mob_color)
            print(f"Mob rengi aralığı: {self.mob_color_range}")
            
        # Stone rengi kalibrasyonu
        stone_color = self.select_color("Stone rengini seçin")
        if stone_color:
            self.stone_color_range = self.create_color_range(stone_color)
            print(f"Stone rengi aralığı: {self.stone_color_range}")
            
        print("Renk kalibrasyonu tamamlandı!")
        
    def select_color(self, message):
        """Kullanıcıdan renk seçmesini ister"""
        print(message)
        print("Mouse ile rengi seçin (sol tık)")
        
        # Mouse event'ini dinle
        selected_color = None
        
        def on_click(x, y, button, pressed):
            nonlocal selected_color
            if pressed and button.name == 'left':
                # Ekran görüntüsü al ve renk al
                screenshot = pyautogui.screenshot()
                pixel_color = screenshot.getpixel((x, y))
                selected_color = pixel_color
                print(f"Seçilen renk: {selected_color}")
                return False
                
        # Mouse listener başlat
        import mouse
        mouse.on_click(on_click)
        
        # Kullanıcı seçim yapana kadar bekle
        while selected_color is None:
            time.sleep(0.1)
            
        mouse.unhook_all()
        return selected_color
        
    def create_color_range(self, color):
        """Renk aralığı oluşturur"""
        # RGB'yi HSV'ye çevir
        hsv_color = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_RGB2HSV)[0][0]
        
        # Tolerans ekle
        tolerance = 30
        lower = np.array([max(0, hsv_color[0] - tolerance), 
                         max(0, hsv_color[1] - tolerance), 
                         max(0, hsv_color[2] - tolerance)])
        upper = np.array([min(179, hsv_color[0] + tolerance), 
                         min(255, hsv_color[1] + tolerance), 
                         min(255, hsv_color[2] + tolerance)])
        
        return {'lower': lower, 'upper': upper}