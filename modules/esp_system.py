#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ESP System Module for GGBOT v2
Player ve Stone görüntüleme sistemi
"""

import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import math

class ESPSystem:
    def __init__(self, parent_bot):
        self.parent_bot = parent_bot
        self.is_running = False
        
        # ESP ayarları
        self.esp_players_enabled = False
        self.esp_stones_enabled = False
        
        # Player tespit ayarları
        self.player_color_range = {
            'lower': np.array([0, 0, 200]),      # Beyazımsı renkler
            'upper': np.array([180, 30, 255])
        }
        
        # Stone tespit ayarları
        self.stone_color_range = {
            'lower': np.array([100, 50, 50]),    # Gri renkler
            'upper': np.array([130, 255, 255])
        }
        
        # ESP görüntüleme ayarları
        self.esp_window = None
        self.esp_canvas = None
        self.esp_overlay = None
        
        # Tespit edilen nesneler
        self.detected_players = []
        self.detected_stones = []
        
        # ESP renkleri
        self.player_color = (0, 255, 0)  # Yeşil
        self.stone_color = (255, 0, 0)   # Mavi
        
    def start(self):
        """ESP sistemini başlatır"""
        self.is_running = True
        self.esp_thread = threading.Thread(target=self.esp_loop, daemon=True)
        self.esp_thread.start()
        self.create_esp_window()
        print("ESP sistemi başlatıldı")
        
    def stop(self):
        """ESP sistemini durdurur"""
        self.is_running = False
        if self.esp_window:
            self.esp_window.destroy()
            self.esp_window = None
        print("ESP sistemi durduruldu")
        
    def esp_loop(self):
        """Ana ESP döngüsü"""
        while self.is_running:
            try:
                # Ekran görüntüsü al
                screenshot = pyautogui.screenshot()
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Player tespiti
                if self.esp_players_enabled:
                    self.detected_players = self.detect_players(img)
                    
                # Stone tespiti
                if self.esp_stones_enabled:
                    self.detected_stones = self.detect_stones(img)
                    
                # ESP overlay'i güncelle
                self.update_esp_overlay(img)
                
                time.sleep(0.1)  # 100ms bekleme
                
            except Exception as e:
                print(f"ESP sistemi hatası: {e}")
                time.sleep(1)
                
    def detect_players(self, img):
        """Oyuncuları tespit eder"""
        players = []
        try:
            # HSV'ye çevir
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Player rengi aralığına göre maske oluştur
            mask = cv2.inRange(hsv, self.player_color_range['lower'], self.player_color_range['upper'])
            
            # Konturları bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Kontur alanını kontrol et
                area = cv2.contourArea(contour)
                if area > 200:  # Minimum alan
                    # Merkez noktasını hesapla
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Bounding box hesapla
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        players.append({
                            'x': cx,
                            'y': cy,
                            'width': w,
                            'height': h,
                            'area': area,
                            'distance': self.calculate_distance(cx, cy)
                        })
                        
        except Exception as e:
            print(f"Player tespit hatası: {e}")
            
        return players
        
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
                if area > 100:  # Minimum alan
                    # Merkez noktasını hesapla
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Bounding box hesapla
                        x, y, w, h = cv2.boundingRect(contour)
                        
                        stones.append({
                            'x': cx,
                            'y': cy,
                            'width': w,
                            'height': h,
                            'area': area,
                            'distance': self.calculate_distance(cx, cy)
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
        
    def create_esp_window(self):
        """ESP penceresi oluşturur"""
        try:
            self.esp_window = tk.Toplevel()
            self.esp_window.title("ESP Overlay")
            self.esp_window.geometry("800x600")
            self.esp_window.configure(bg='black')
            
            # Canvas oluştur
            self.esp_canvas = tk.Canvas(self.esp_window, bg='black', highlightthickness=0)
            self.esp_canvas.pack(fill='both', expand=True)
            
            # Pencereyi şeffaf yap
            self.esp_window.attributes('-alpha', 0.7)
            self.esp_window.attributes('-topmost', True)
            
        except Exception as e:
            print(f"ESP pencere oluşturma hatası: {e}")
            
    def update_esp_overlay(self, img):
        """ESP overlay'ini günceller"""
        if not self.esp_canvas:
            return
            
        try:
            # Canvas'ı temizle
            self.esp_canvas.delete("all")
            
            # Player'ları çiz
            if self.esp_players_enabled:
                for player in self.detected_players:
                    self.draw_player_esp(player)
                    
            # Stone'ları çiz
            if self.esp_stones_enabled:
                for stone in self.detected_stones:
                    self.draw_stone_esp(stone)
                    
            # Canvas'ı güncelle
            self.esp_canvas.update()
            
        except Exception as e:
            print(f"ESP overlay güncelleme hatası: {e}")
            
    def draw_player_esp(self, player):
        """Player ESP'sini çizer"""
        try:
            x, y = player['x'], player['y']
            w, h = player['width'], player['height']
            distance = player['distance']
            
            # Bounding box çiz
            self.esp_canvas.create_rectangle(
                x - w//2, y - h//2, x + w//2, y + h//2,
                outline=self.player_color, width=2, fill=""
            )
            
            # Merkez nokta çiz
            self.esp_canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill=self.player_color, outline=""
            )
            
            # Mesafe bilgisi
            self.esp_canvas.create_text(
                x, y - h//2 - 10,
                text=f"Player ({distance:.0f}px)",
                fill=self.player_color, font=('Arial', 8)
            )
            
        except Exception as e:
            print(f"Player ESP çizim hatası: {e}")
            
    def draw_stone_esp(self, stone):
        """Stone ESP'sini çizer"""
        try:
            x, y = stone['x'], stone['y']
            w, h = stone['width'], stone['height']
            distance = stone['distance']
            
            # Bounding box çiz
            self.esp_canvas.create_rectangle(
                x - w//2, y - h//2, x + w//2, y + h//2,
                outline=self.stone_color, width=2, fill=""
            )
            
            # Merkez nokta çiz
            self.esp_canvas.create_oval(
                x - 2, y - 2, x + 2, y + 2,
                fill=self.stone_color, outline=""
            )
            
            # Mesafe bilgisi
            self.esp_canvas.create_text(
                x, y - h//2 - 10,
                text=f"Stone ({distance:.0f}px)",
                fill=self.stone_color, font=('Arial', 8)
            )
            
        except Exception as e:
            print(f"Stone ESP çizim hatası: {e}")
            
    def update_settings(self, settings):
        """Ayarları günceller"""
        self.esp_players_enabled = settings.get('esp_players_enabled', False)
        self.esp_stones_enabled = settings.get('esp_stones_enabled', False)
        
    def create_esp_ui(self, parent_frame):
        """ESP sistemi için UI oluşturur"""
        esp_frame = tk.LabelFrame(parent_frame, text="ESP Sistemi", fg='cyan', bg='#2b2b2b')
        esp_frame.pack(fill='x', padx=10, pady=5)
        
        # Player ESP
        player_frame = tk.Frame(esp_frame, bg='#2b2b2b')
        player_frame.pack(fill='x', padx=5, pady=2)
        
        self.esp_players_var = tk.BooleanVar(value=self.esp_players_enabled)
        tk.Checkbutton(player_frame, text="Player ESP", variable=self.esp_players_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        # Stone ESP
        stone_frame = tk.Frame(esp_frame, bg='#2b2b2b')
        stone_frame.pack(fill='x', padx=5, pady=2)
        
        self.esp_stones_var = tk.BooleanVar(value=self.esp_stones_enabled)
        tk.Checkbutton(stone_frame, text="Stone ESP", variable=self.esp_stones_var,
                      bg='#2b2b2b', fg='white', selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        # Renk ayarları
        color_frame = tk.Frame(esp_frame, bg='#2b2b2b')
        color_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(color_frame, text="Player Rengi:", bg='#2b2b2b', fg='white').pack(side='left')
        self.player_color_var = tk.StringVar(value="Green")
        player_color_combo = tk.OptionMenu(color_frame, self.player_color_var, 
                                         "Green", "Red", "Blue", "Yellow", "Cyan", "Magenta")
        player_color_combo.pack(side='left', padx=5)
        
        tk.Label(color_frame, text="Stone Rengi:", bg='#2b2b2b', fg='white').pack(side='left', padx=10)
        self.stone_color_var = tk.StringVar(value="Blue")
        stone_color_combo = tk.OptionMenu(color_frame, self.stone_color_var, 
                                        "Green", "Red", "Blue", "Yellow", "Cyan", "Magenta")
        stone_color_combo.pack(side='left', padx=5)
        
        # Kontroller
        control_frame = tk.Frame(esp_frame, bg='#2b2b2b')
        control_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(control_frame, text="Renk Kalibre Et", command=self.calibrate_colors,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        tk.Button(control_frame, text="ESP Pencereyi Göster", command=self.show_esp_window,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        tk.Button(control_frame, text="ESP Pencereyi Gizle", command=self.hide_esp_window,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        # Durum gösterimi
        status_frame = tk.Frame(esp_frame, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="ESP Sistemi: Durduruldu", 
                                   bg='#2b2b2b', fg='white')
        self.status_label.pack(side='left')
        
        self.player_count_label = tk.Label(status_frame, text="Player: 0", 
                                         bg='#2b2b2b', fg='white')
        self.player_count_label.pack(side='left', padx=20)
        
        self.stone_count_label = tk.Label(status_frame, text="Stone: 0", 
                                        bg='#2b2b2b', fg='white')
        self.stone_count_label.pack(side='left', padx=20)
        
    def update_ui_status(self):
        """UI durumunu günceller"""
        if hasattr(self, 'status_label'):
            status = "Çalışıyor" if self.is_running else "Durduruldu"
            self.status_label.config(text=f"ESP Sistemi: {status}")
            
        if hasattr(self, 'player_count_label'):
            self.player_count_label.config(text=f"Player: {len(self.detected_players)}")
            
        if hasattr(self, 'stone_count_label'):
            self.stone_count_label.config(text=f"Stone: {len(self.detected_stones)}")
            
    def calibrate_colors(self):
        """Renk kalibrasyonu yapar"""
        print("ESP renk kalibrasyonu başlatılıyor...")
        
        # Player rengi kalibrasyonu
        if self.esp_players_enabled:
            player_color = self.select_color("Player rengini seçin")
            if player_color:
                self.player_color_range = self.create_color_range(player_color)
                print(f"Player rengi aralığı: {self.player_color_range}")
                
        # Stone rengi kalibrasyonu
        if self.esp_stones_enabled:
            stone_color = self.select_color("Stone rengini seçin")
            if stone_color:
                self.stone_color_range = self.create_color_range(stone_color)
                print(f"Stone rengi aralığı: {self.stone_color_range}")
                
        print("ESP renk kalibrasyonu tamamlandı!")
        
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
        
    def show_esp_window(self):
        """ESP penceresini gösterir"""
        if not self.esp_window:
            self.create_esp_window()
        else:
            self.esp_window.deiconify()
            
    def hide_esp_window(self):
        """ESP penceresini gizler"""
        if self.esp_window:
            self.esp_window.withdraw()
            
    def set_player_color(self, color_name):
        """Player rengini ayarlar"""
        color_map = {
            'Green': (0, 255, 0),
            'Red': (0, 0, 255),
            'Blue': (255, 0, 0),
            'Yellow': (0, 255, 255),
            'Cyan': (255, 255, 0),
            'Magenta': (255, 0, 255)
        }
        
        if color_name in color_map:
            self.player_color = color_map[color_name]
            print(f"Player rengi: {color_name}")
            
    def set_stone_color(self, color_name):
        """Stone rengini ayarlar"""
        color_map = {
            'Green': (0, 255, 0),
            'Red': (0, 0, 255),
            'Blue': (255, 0, 0),
            'Yellow': (0, 255, 255),
            'Cyan': (255, 255, 0),
            'Magenta': (255, 0, 255)
        }
        
        if color_name in color_map:
            self.stone_color = color_map[color_name]
            print(f"Stone rengi: {color_name}")
            
    def get_detected_objects(self):
        """Tespit edilen nesneleri döndürür"""
        return {
            'players': self.detected_players,
            'stones': self.detected_stones
        }