#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Potion System Module for GGBOT v2
Red ve Blue potion otomatik kullanım sistemi
"""

import cv2
import numpy as np
import pyautogui
import time
import threading
from PIL import Image, ImageTk
import tkinter as tk

class PotionSystem:
    def __init__(self, parent_bot):
        self.parent_bot = parent_bot
        self.is_running = False
        self.red_potion_threshold = 30
        self.blue_potion_threshold = 30
        self.red_potion_enabled = False
        self.blue_potion_enabled = False
        self.stop_no_red = False
        
        # Potion tuşları (oyuna göre ayarlanmalı)
        self.red_potion_key = '1'  # Kırmızı potion tuşu
        self.blue_potion_key = '2'  # Mavi potion tuşu
        
        # HP/MP bar koordinatları (oyuna göre ayarlanmalı)
        self.hp_bar_region = (100, 50, 200, 70)  # x, y, width, height
        self.mp_bar_region = (100, 80, 200, 100)
        
        # Renk aralıkları (HP/MP bar renkleri)
        self.hp_color_range = {
            'lower': np.array([0, 100, 100]),    # Kırmızı alt sınır
            'upper': np.array([10, 255, 255])    # Kırmızı üst sınır
        }
        
        self.mp_color_range = {
            'lower': np.array([100, 100, 100]),  # Mavi alt sınır
            'upper': np.array([130, 255, 255])   # Mavi üst sınır
        }
        
        # Potion sayısı takibi
        self.red_potion_count = 0
        self.blue_potion_count = 0
        
    def start(self):
        """Potion sistemini başlatır"""
        self.is_running = True
        self.potion_thread = threading.Thread(target=self.potion_loop, daemon=True)
        self.potion_thread.start()
        print("Potion sistemi başlatıldı")
        
    def stop(self):
        """Potion sistemini durdurur"""
        self.is_running = False
        print("Potion sistemi durduruldu")
        
    def potion_loop(self):
        """Ana potion kontrol döngüsü"""
        while self.is_running:
            try:
                # HP kontrolü ve red potion kullanımı
                if self.red_potion_enabled:
                    hp_percentage = self.get_hp_percentage()
                    if hp_percentage is not None and hp_percentage <= self.red_potion_threshold:
                        self.use_red_potion()
                        
                # MP kontrolü ve blue potion kullanımı
                if self.blue_potion_enabled:
                    mp_percentage = self.get_mp_percentage()
                    if mp_percentage is not None and mp_percentage <= self.blue_potion_threshold:
                        self.use_blue_potion()
                        
                # Red potion bittiğinde botu durdur
                if self.stop_no_red and self.red_potion_count <= 0:
                    self.parent_bot.stop_bot()
                    break
                    
                time.sleep(0.5)  # 500ms bekleme
                
            except Exception as e:
                print(f"Potion sistemi hatası: {e}")
                time.sleep(1)
                
    def get_hp_percentage(self):
        """HP yüzdesini hesaplar"""
        try:
            # Ekran görüntüsü al
            screenshot = pyautogui.screenshot(region=self.hp_bar_region)
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # HP bar'ı bul
            hp_percentage = self.analyze_bar_percentage(img, self.hp_color_range)
            return hp_percentage
            
        except Exception as e:
            print(f"HP analiz hatası: {e}")
            return None
            
    def get_mp_percentage(self):
        """MP yüzdesini hesaplar"""
        try:
            # Ekran görüntüsü al
            screenshot = pyautogui.screenshot(region=self.mp_bar_region)
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # MP bar'ı bul
            mp_percentage = self.analyze_bar_percentage(img, self.mp_color_range)
            return mp_percentage
            
        except Exception as e:
            print(f"MP analiz hatası: {e}")
            return None
            
    def analyze_bar_percentage(self, img, color_range):
        """Bar yüzdesini analiz eder"""
        try:
            # HSV'ye çevir
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Renk aralığına göre maske oluştur
            mask = cv2.inRange(hsv, color_range['lower'], color_range['upper'])
            
            # Konturları bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # En büyük konturu al
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Konturun genişliğini hesapla
                x, y, w, h = cv2.boundingRect(largest_contour)
                bar_width = w
                total_width = img.shape[1]
                
                # Yüzde hesapla
                percentage = (bar_width / total_width) * 100
                return min(100, max(0, percentage))
                
        except Exception as e:
            print(f"Bar analiz hatası: {e}")
            
        return None
        
    def use_red_potion(self):
        """Red potion kullanır"""
        try:
            pyautogui.press(self.red_potion_key)
            self.red_potion_count = max(0, self.red_potion_count - 1)
            print(f"Red potion kullanıldı. Kalan: {self.red_potion_count}")
            time.sleep(0.1)  # Kısa bekleme
            
        except Exception as e:
            print(f"Red potion kullanım hatası: {e}")
            
    def use_blue_potion(self):
        """Blue potion kullanır"""
        try:
            pyautogui.press(self.blue_potion_key)
            self.blue_potion_count = max(0, self.blue_potion_count - 1)
            print(f"Blue potion kullanıldı. Kalan: {self.blue_potion_count}")
            time.sleep(0.1)  # Kısa bekleme
            
        except Exception as e:
            print(f"Blue potion kullanım hatası: {e}")
            
    def update_settings(self, settings):
        """Ayarları günceller"""
        self.red_potion_threshold = settings.get('red_potion_threshold', 30)
        self.blue_potion_threshold = settings.get('blue_potion_threshold', 30)
        self.red_potion_enabled = settings.get('red_potion_enabled', False)
        self.blue_potion_enabled = settings.get('blue_potion_enabled', False)
        self.stop_no_red = settings.get('stop_no_red', False)
        
    def calibrate_bars(self):
        """HP/MP bar'larını kalibre eder"""
        print("HP/MP bar kalibrasyonu başlatılıyor...")
        print("Lütfen oyun penceresini HP/MP bar'ları görünecek şekilde ayarlayın")
        
        # HP bar kalibrasyonu
        hp_region = self.select_region("HP Bar'ını seçin")
        if hp_region:
            self.hp_bar_region = hp_region
            print(f"HP bar bölgesi: {hp_region}")
            
        # MP bar kalibrasyonu
        mp_region = self.select_region("MP Bar'ını seçin")
        if mp_region:
            self.mp_bar_region = mp_region
            print(f"MP bar bölgesi: {mp_region}")
            
        print("Kalibrasyon tamamlandı!")
        
    def select_region(self, message):
        """Kullanıcıdan bölge seçmesini ister"""
        print(message)
        print("Mouse ile bölgeyi seçin (sol tık başlangıç, sağ tık bitiş)")
        
        # Mouse event'lerini dinle
        start_pos = None
        end_pos = None
        
        def on_click(x, y, button, pressed):
            nonlocal start_pos, end_pos
            if pressed and button.name == 'left':
                start_pos = (x, y)
                print(f"Başlangıç: {start_pos}")
            elif not pressed and button.name == 'right' and start_pos:
                end_pos = (x, y)
                print(f"Bitiş: {end_pos}")
                return False
                
        # Mouse listener başlat
        import mouse
        mouse.on_click(on_click)
        
        # Kullanıcı seçim yapana kadar bekle
        while start_pos is None or end_pos is None:
            time.sleep(0.1)
            
        mouse.unhook_all()
        
        # Bölge koordinatlarını hesapla
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Sol üst ve sağ alt koordinatları düzenle
        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        return (x, y, width, height)
        
    def get_potion_count(self):
        """Mevcut potion sayılarını döndürür"""
        return {
            'red_potion_count': self.red_potion_count,
            'blue_potion_count': self.blue_potion_count
        }
        
    def set_potion_count(self, red_count, blue_count):
        """Potion sayılarını ayarlar"""
        self.red_potion_count = red_count
        self.blue_potion_count = blue_count
        print(f"Potion sayıları güncellendi - Red: {red_count}, Blue: {blue_count}")
        
    def detect_potion_inventory(self):
        """Envanterdeki potion sayısını tespit eder"""
        try:
            # Envanter bölgesini tarayarak potion sayısını tespit et
            # Bu fonksiyon OCR veya görüntü işleme ile geliştirilebilir
            pass
        except Exception as e:
            print(f"Potion tespit hatası: {e}")
            
    def create_potion_ui(self, parent_frame):
        """Potion sistemi için UI oluşturur"""
        potion_frame = tk.LabelFrame(parent_frame, text="Potion Sistemi", fg='red', bg='#2b2b2b')
        potion_frame.pack(fill='x', padx=10, pady=5)
        
        # HP Threshold
        hp_frame = tk.Frame(potion_frame, bg='#2b2b2b')
        hp_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(hp_frame, text="HP Threshold:", bg='#2b2b2b', fg='white').pack(side='left')
        self.hp_threshold_var = tk.IntVar(value=self.red_potion_threshold)
        hp_scale = tk.Scale(hp_frame, from_=10, to=100, orient='horizontal',
                           variable=self.hp_threshold_var, bg='#2b2b2b', fg='white')
        hp_scale.pack(side='left', padx=5)
        
        # MP Threshold
        mp_frame = tk.Frame(potion_frame, bg='#2b2b2b')
        mp_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(mp_frame, text="MP Threshold:", bg='#2b2b2b', fg='white').pack(side='left')
        self.mp_threshold_var = tk.IntVar(value=self.blue_potion_threshold)
        mp_scale = tk.Scale(mp_frame, from_=10, to=100, orient='horizontal',
                           variable=self.mp_threshold_var, bg='#2b2b2b', fg='white')
        mp_scale.pack(side='left', padx=5)
        
        # Kontroller
        control_frame = tk.Frame(potion_frame, bg='#2b2b2b')
        control_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Button(control_frame, text="Kalibre Et", command=self.calibrate_bars,
                 bg='#4CAF50', fg='white').pack(side='left', padx=5)
        
        tk.Button(control_frame, text="Potion Sayısını Ayarla", 
                 command=self.set_potion_count_dialog, bg='#2196F3', fg='white').pack(side='left', padx=5)
        
        # Durum gösterimi
        status_frame = tk.Frame(potion_frame, bg='#2b2b2b')
        status_frame.pack(fill='x', padx=5, pady=2)
        
        self.status_label = tk.Label(status_frame, text="Potion Sistemi: Durduruldu", 
                                   bg='#2b2b2b', fg='white')
        self.status_label.pack(side='left')
        
    def set_potion_count_dialog(self):
        """Potion sayısı ayarlama dialogu"""
        dialog = tk.Toplevel()
        dialog.title("Potion Sayısı Ayarla")
        dialog.geometry("300x150")
        dialog.configure(bg='#2b2b2b')
        
        tk.Label(dialog, text="Red Potion Sayısı:", bg='#2b2b2b', fg='white').pack(pady=5)
        red_entry = tk.Entry(dialog, bg='#3b3b3b', fg='white')
        red_entry.pack(pady=5)
        red_entry.insert(0, str(self.red_potion_count))
        
        tk.Label(dialog, text="Blue Potion Sayısı:", bg='#2b2b2b', fg='white').pack(pady=5)
        blue_entry = tk.Entry(dialog, bg='#3b3b3b', fg='white')
        blue_entry.pack(pady=5)
        blue_entry.insert(0, str(self.blue_potion_count))
        
        def save_counts():
            try:
                red_count = int(red_entry.get())
                blue_count = int(blue_entry.get())
                self.set_potion_count(red_count, blue_count)
                dialog.destroy()
            except ValueError:
                tk.messagebox.showerror("Hata", "Lütfen geçerli sayılar girin!")
                
        tk.Button(dialog, text="Kaydet", command=save_counts,
                 bg='#4CAF50', fg='white').pack(pady=10)