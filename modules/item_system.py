#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Item System Module for GGBOT v2
Item arama ve toplama sistemi
"""

import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from PIL import Image, ImageTk
import json
import os

class ItemSystem:
    def __init__(self, parent_bot):
        self.parent_bot = parent_bot
        self.is_running = False
        
        # Item ayarları
        self.pickup_filter_enabled = False
        self.drop_no_bonus = False
        self.item_list = []
        
        # Item tespit ayarları
        self.item_color_range = {
            'lower': np.array([0, 0, 200]),      # Parlak renkler
            'upper': np.array([180, 30, 255])
        }
        
        # Toplama aralığı
        self.pickup_range = 100  # Piksel cinsinden
        
        # Tespit edilen itemler
        self.detected_items = []
        
        # Item türleri
        self.item_types = {
            'weapon': 'Silah',
            'armor': 'Zırh',
            'accessory': 'Aksesuar',
            'potion': 'Potion',
            'material': 'Malzeme',
            'coin': 'Para',
            'gem': 'Mücevher'
        }
        
        # Item dosyası yolu
        self.items_file = 'data/items.json'
        self.load_items()
        
    def start(self):
        """Item sistemini başlatır"""
        self.is_running = True
        self.item_thread = threading.Thread(target=self.item_loop, daemon=True)
        self.item_thread.start()
        print("Item sistemi başlatıldı")
        
    def stop(self):
        """Item sistemini durdurur"""
        self.is_running = False
        print("Item sistemi durduruldu")
        
    def item_loop(self):
        """Ana item döngüsü"""
        while self.is_running:
            try:
                # Ekran görüntüsü al
                screenshot = pyautogui.screenshot()
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Item'ları tespit et
                self.detected_items = self.detect_items(img)
                
                # Item'ları topla
                if self.detected_items:
                    self.pickup_items()
                    
                time.sleep(0.5)  # 500ms bekleme
                
            except Exception as e:
                print(f"Item sistemi hatası: {e}")
                time.sleep(1)
                
    def detect_items(self, img):
        """Item'ları tespit eder"""
        items = []
        try:
            # HSV'ye çevir
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Item rengi aralığına göre maske oluştur
            mask = cv2.inRange(hsv, self.item_color_range['lower'], self.item_color_range['upper'])
            
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
                        
                        if distance <= self.pickup_range:
                            # Item türünü tespit et
                            item_type = self.detect_item_type(img, cx, cy)
                            
                            items.append({
                                'x': cx,
                                'y': cy,
                                'area': area,
                                'distance': distance,
                                'type': item_type,
                                'name': self.get_item_name(item_type)
                            })
                            
        except Exception as e:
            print(f"Item tespit hatası: {e}")
            
        return items
        
    def detect_item_type(self, img, x, y):
        """Item türünü tespit eder"""
        try:
            # Item bölgesini kes
            item_region = img[y-20:y+20, x-20:x+20]
            
            # Renk analizi yap
            avg_color = np.mean(item_region, axis=(0, 1))
            
            # Renk bazlı tür tespiti
            if avg_color[2] > 200:  # Mavi ağırlıklı
                return 'weapon'
            elif avg_color[1] > 200:  # Yeşil ağırlıklı
                return 'armor'
            elif avg_color[0] > 200:  # Kırmızı ağırlıklı
                return 'potion'
            else:
                return 'material'
                
        except Exception as e:
            print(f"Item tür tespit hatası: {e}")
            return 'unknown'
            
    def get_item_name(self, item_type):
        """Item adını döndürür"""
        return self.item_types.get(item_type, 'Bilinmeyen')
        
    def calculate_distance(self, x, y):
        """Mesafeyi hesaplar"""
        # Ekran merkezinden mesafe
        screen_center_x = pyautogui.size().width // 2
        screen_center_y = pyautogui.size().height // 2
        
        distance = ((x - screen_center_x) ** 2 + (y - screen_center_y) ** 2) ** 0.5
        return distance
        
    def pickup_items(self):
        """Item'ları toplar"""
        for item in self.detected_items:
            try:
                # Filtre kontrolü
                if self.pickup_filter_enabled:
                    if not self.is_item_in_list(item):
                        continue
                        
                # Item'a tıkla
                pyautogui.click(item['x'], item['y'])
                
                print(f"Item toplandı: {item['name']} ({item['type']})")
                
                # Kısa bekleme
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Item toplama hatası: {e}")
                
    def is_item_in_list(self, item):
        """Item'ın listede olup olmadığını kontrol eder"""
        return item['name'].lower() in [i.lower() for i in self.item_list]
        
    def add_item(self, item_name):
        """Item listesine item ekler"""
        if item_name and item_name not in self.item_list:
            self.item_list.append(item_name)
            self.save_items()
            print(f"Item eklendi: {item_name}")
            
    def remove_item(self, item_name):
        """Item listesinden item siler"""
        if item_name in self.item_list:
            self.item_list.remove(item_name)
            self.save_items()
            print(f"Item silindi: {item_name}")
            
    def clear_items(self):
        """Item listesini temizler"""
        self.item_list = []
        self.save_items()
        print("Item listesi temizlendi")
        
    def load_items(self):
        """Item'ları dosyadan yükler"""
        try:
            if os.path.exists(self.items_file):
                with open(self.items_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.item_list = data.get('items', [])
        except Exception as e:
            print(f"Item yükleme hatası: {e}")
            
    def save_items(self):
        """Item'ları dosyaya kaydeder"""
        try:
            os.makedirs(os.path.dirname(self.items_file), exist_ok=True)
            
            data = {
                'items': self.item_list,
                'last_updated': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            with open(self.items_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Item kaydetme hatası: {e}")
            
    def update_settings(self, settings):
        """Ayarları günceller"""
        self.pickup_filter_enabled = settings.get('pickup_filter_enabled', False)
        self.drop_no_bonus = settings.get('drop_no_bonus', False)
        
    def create_item_ui(self, parent_frame):
        """Item sistemi için UI oluşturur"""
        item_frame = tk.LabelFrame(parent_frame, text="Item Sistemi", fg='cyan', bg='#2b2b2b')
        item_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Item arama
        search_frame = tk.Frame(item_frame, bg='#2b2b2b')
        search_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(search_frame, text="Item Ara:", bg='#2b2b2b', fg='white').pack(side='left')
        self.item_search_var = tk.StringVar()
        item_search_entry = tk.Entry(search_frame, textvariable=self.item_search_var, 
                                   bg='#3b3b3b', fg='white')
        item_search_entry.pack(side='left', padx=5)
        
        tk.Button(search_frame, text="Ekle", command=self.add_item_from_ui,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        # Item listesi
        list_frame = tk.Frame(item_frame, bg='#2b2b2b')
        list_frame.pack(fill='both', expand=True, padx=5, pady=2)
        
        self.item_listbox = tk.Listbox(list_frame, bg='#3b3b3b', fg='white')
        self.item_listbox.pack(fill='both', expand=True)
        
        # Item kontrolleri
        control_frame = tk.Frame(item_frame, bg='#2b2b2b')
        control_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Button(control_frame, text="Sil", command=self.remove_selected_item,
                 bg='#f44336', fg='white').pack(side='left', padx=5)
        
        tk.Button(control_frame, text="Temizle", command=self.clear_items_ui,
                 bg='#ff9800', fg='white').pack(side='left', padx=5)
        
        tk.Button(control_frame, text="Yenile", command=self.refresh_item_list,
                 bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        # Filtre ayarları
        filter_frame = tk.Frame(item_frame, bg='#2b2b2b')
        filter_frame.pack(fill='x', padx=5, pady=2)
        
        self.pickup_filter_var = tk.BooleanVar(value=self.pickup_filter_enabled)
        tk.Checkbutton(filter_frame, text="Sadece listeye eklenen itemleri topla", 
                      variable=self.pickup_filter_var, bg='#2b2b2b', fg='white', 
                      selectcolor='#2b2b2b').pack(side='left', padx=5)
        
        self.drop_no_bonus_var = tk.BooleanVar(value=self.drop_no_bonus)
        tk.Checkbutton(filter_frame, text="Efsunsuz itemleri yere at", 
                      variable=self.drop_no_bonus_var, bg='#2b2b2b', fg='white', 
                      selectcolor='#2b2b2b').pack(side='left', padx=10)
        
        # Toplama ayarları
        pickup_frame = tk.Frame(item_frame, bg='#2b2b2b')
        pickup_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(pickup_frame, text="Toplama Aralığı:", bg='#2b2b2b', fg='white').pack(side='left')
        self.pickup_range_var = tk.IntVar(value=self.pickup_range)
        pickup_scale = tk.Scale(pickup_frame, from_=50, to=300, orient='horizontal',
                               variable=self.pickup_range_var, bg='#2b2b2b', fg='white')
        pickup_scale.pack(side='left', padx=5)
        
        # Durum gösterimi
        status_frame = tk.Frame(item_frame, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="Item Sistemi: Durduruldu", 
                                   bg='#2b2b2b', fg='white')
        self.status_label.pack(side='left')
        
        self.item_count_label = tk.Label(status_frame, text="Tespit Edilen: 0", 
                                       bg='#2b2b2b', fg='white')
        self.item_count_label.pack(side='right')
        
        # Item listesini yükle
        self.refresh_item_list()
        
    def add_item_from_ui(self):
        """UI'dan item ekler"""
        item_name = self.item_search_var.get().strip()
        if item_name:
            self.add_item(item_name)
            self.item_search_var.set("")
            self.refresh_item_list()
            
    def remove_selected_item(self):
        """Seçili item'i siler"""
        selection = self.item_listbox.curselection()
        if selection:
            item_name = self.item_listbox.get(selection[0])
            self.remove_item(item_name)
            self.refresh_item_list()
            
    def clear_items_ui(self):
        """UI'dan item listesini temizler"""
        self.clear_items()
        self.refresh_item_list()
        
    def refresh_item_list(self):
        """Item listesini yeniler"""
        self.item_listbox.delete(0, tk.END)
        for item in self.item_list:
            self.item_listbox.insert(tk.END, item)
            
    def update_ui_status(self):
        """UI durumunu günceller"""
        if hasattr(self, 'status_label'):
            status = "Çalışıyor" if self.is_running else "Durduruldu"
            self.status_label.config(text=f"Item Sistemi: {status}")
            
        if hasattr(self, 'item_count_label'):
            self.item_count_label.config(text=f"Tespit Edilen: {len(self.detected_items)}")
            
    def get_detected_items(self):
        """Tespit edilen item'ları döndürür"""
        return self.detected_items
        
    def set_pickup_range(self, range_value):
        """Toplama aralığını ayarlar"""
        self.pickup_range = range_value
        print(f"Toplama aralığı: {range_value} piksel")
        
    def calibrate_item_colors(self):
        """Item renk kalibrasyonu yapar"""
        print("Item renk kalibrasyonu başlatılıyor...")
        print("Lütfen item rengini seçin")
        
        # Item rengi seçimi
        item_color = self.select_color("Item rengini seçin")
        if item_color:
            self.item_color_range = self.create_color_range(item_color)
            print(f"Item rengi aralığı: {self.item_color_range}")
            
        print("Item renk kalibrasyonu tamamlandı!")
        
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
        
    def export_items(self, filename):
        """Item listesini dışa aktarır"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.item_list, f, indent=4, ensure_ascii=False)
            print(f"Item listesi dışa aktarıldı: {filename}")
        except Exception as e:
            print(f"Dışa aktarma hatası: {e}")
            
    def import_items(self, filename):
        """Item listesini içe aktarır"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_items = json.load(f)
                self.item_list.extend(imported_items)
                self.save_items()
                self.refresh_item_list()
            print(f"Item listesi içe aktarıldı: {filename}")
        except Exception as e:
            print(f"İçe aktarma hatası: {e}")