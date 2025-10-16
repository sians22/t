#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bot ana motoru - tüm bot işlevlerini yönetir
"""

import time
import threading
import keyboard
import pyautogui
import random
from typing import Dict, List, Tuple, Optional
import cv2
import numpy as np

from ..utils.game_utils import GameUtils
from ..utils.memory_utils import MemoryUtils
from ..utils.image_utils import ImageUtils
from ..config.settings import Settings

class BotEngine:
    """Bot ana motoru"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.game_utils = GameUtils()
        self.memory_utils = MemoryUtils()
        self.image_utils = ImageUtils()
        
        self.running = False
        self.paused = False
        
        # Bot durumları
        self.player_stats = {
            "health": 100,
            "mana": 100,
            "max_health": 100,
            "max_mana": 100
        }
        
        self.player_position = {"x": 0, "y": 0}
        self.target_position = {"x": 0, "y": 0}
        
        # Algılanan objeler
        self.detected_mobs = []
        self.detected_stones = []
        self.detected_players = []
        self.detected_items = []
        
        # Route sistemi
        self.current_route = []
        self.route_index = 0
        self.recording_route = False
        
        # Timing
        self.last_potion_time = {"red": 0, "blue": 0}
        self.last_attack_time = 0
        self.last_movement_time = 0
        
        # Hotkeys
        self.setup_hotkeys()
        
    def setup_hotkeys(self):
        """Hotkey'leri ayarla"""
        try:
            keyboard.add_hotkey('F9', self.toggle_bot)
            keyboard.add_hotkey('F10', self.toggle_pause)
            keyboard.add_hotkey('F11', self.emergency_stop)
        except Exception as e:
            print(f"Hotkey ayarlanırken hata: {e}")
            
    def start(self):
        """Bot'u başlat"""
        self.running = True
        print("Bot başlatıldı!")
        
        while self.running:
            try:
                if not self.paused:
                    self.main_loop()
                time.sleep(0.1)  # CPU kullanımını azalt
                
            except Exception as e:
                print(f"Bot döngüsünde hata: {e}")
                time.sleep(1)
                
    def stop(self):
        """Bot'u durdur"""
        self.running = False
        print("Bot durduruldu!")
        
    def toggle_bot(self):
        """Bot'u aç/kapat"""
        if self.running:
            self.stop()
        else:
            threading.Thread(target=self.start, daemon=True).start()
            
    def toggle_pause(self):
        """Bot'u duraklat/devam ettir"""
        self.paused = not self.paused
        print(f"Bot {'duraklatıldı' if self.paused else 'devam ediyor'}!")
        
    def emergency_stop(self):
        """Acil durdurma"""
        self.stop()
        print("ACİL DURDURMA!")
        
    def main_loop(self):
        """Ana bot döngüsü"""
        # Oyun penceresini kontrol et
        if not self.game_utils.is_game_active():
            return
            
        # Oyuncu istatistiklerini güncelle
        self.update_player_stats()
        
        # Potion kontrolü
        self.check_potions()
        
        # Player detection
        self.check_players()
        
        # Combat sistemi
        if self.settings.get("combat.enabled", False):
            self.combat_system()
            
        # Item pickup
        if self.settings.get("items.pickup_filter", False):
            self.pickup_items()
            
        # Auto route
        if self.settings.get("routes.auto_route_enabled", False):
            self.auto_route()
            
        # Fishing bot
        if self.settings.get("fishing.enabled", False):
            self.fishing_bot()
            
        # Spam bot
        if self.settings.get("spam_bot.enabled", False):
            self.spam_bot()
            
    def update_player_stats(self):
        """Oyuncu istatistiklerini güncelle"""
        try:
            # Memory'den HP/MP değerlerini oku
            # Bu kısım gerçek oyun için memory reading gerektirir
            # Şimdilik simüle ediyoruz
            
            # Simülasyon için rastgele değerler
            if random.random() < 0.1:  # %10 ihtimalle değişim
                self.player_stats["health"] = max(0, self.player_stats["health"] - random.randint(0, 10))
                self.player_stats["mana"] = max(0, self.player_stats["mana"] - random.randint(0, 5))
                
        except Exception as e:
            print(f"Player stats güncellenirken hata: {e}")
            
    def check_potions(self):
        """Potion kontrolü ve kullanımı"""
        current_time = time.time()
        
        # Red potion kontrolü
        if self.settings.get("red_potion.enabled", False):
            health_percent = (self.player_stats["health"] / self.player_stats["max_health"]) * 100
            threshold = self.settings.get("red_potion.health_percentage", 50)
            
            if health_percent <= threshold and current_time - self.last_potion_time["red"] > 1:
                self.use_red_potion()
                self.last_potion_time["red"] = current_time
                
        # Blue potion kontrolü
        if self.settings.get("blue_potion.enabled", False):
            mana_percent = (self.player_stats["mana"] / self.player_stats["max_mana"]) * 100
            threshold = self.settings.get("blue_potion.mana_percentage", 30)
            
            if mana_percent <= threshold and current_time - self.last_potion_time["blue"] > 1:
                self.use_blue_potion()
                self.last_potion_time["blue"] = current_time
                
    def use_red_potion(self):
        """Kırmızı potion kullan"""
        try:
            key = self.settings.get("red_potion.key", "F1")
            pyautogui.press(key)
            print("Kırmızı potion kullanıldı!")
            
            # HP'yi artır (simülasyon)
            self.player_stats["health"] = min(
                self.player_stats["max_health"],
                self.player_stats["health"] + 50
            )
        except Exception as e:
            print(f"Kırmızı potion kullanılırken hata: {e}")
            
    def use_blue_potion(self):
        """Mavi potion kullan"""
        try:
            key = self.settings.get("blue_potion.key", "F2")
            pyautogui.press(key)
            print("Mavi potion kullanıldı!")
            
            # MP'yi artır (simülasyon)
            self.player_stats["mana"] = min(
                self.player_stats["max_mana"],
                self.player_stats["mana"] + 30
            )
        except Exception as e:
            print(f"Mavi potion kullanılırken hata: {e}")
            
    def check_players(self):
        """Oyuncu algılama ve tepki sistemi"""
        try:
            # Oyuncuları algıla (simülasyon)
            self.detected_players = self.detect_players()
            
            # Whitelist kontrolü
            whitelist = self.settings.get("player_detection.whitelist", [])
            
            for player in self.detected_players:
                if player["name"] not in whitelist:
                    self.handle_player_detection(player)
                    
        except Exception as e:
            print(f"Player detection hatası: {e}")
            
    def detect_players(self) -> List[Dict]:
        """Oyuncuları algıla"""
        # Gerçek implementasyon için image recognition gerekli
        # Şimdilik simülasyon
        if random.random() < 0.05:  # %5 ihtimalle oyuncu algıla
            return [{"name": f"Player{random.randint(1, 100)}", "distance": random.randint(50, 200)}]
        return []
        
    def handle_player_detection(self, player: Dict):
        """Oyuncu algılandığında tepki ver"""
        print(f"Oyuncu algılandı: {player['name']}")
        
        # Ayarlara göre tepki ver
        player_settings = self.settings.get("player_detection.on_player", {})
        
        if player_settings.get("stop_bot", False):
            self.paused = True
            print("Bot durduruldu - oyuncu algılandı!")
            
        if player_settings.get("sound_alarm", False):
            self.play_alarm()
            
    def combat_system(self):
        """Savaş sistemi"""
        try:
            current_time = time.time()
            
            if current_time - self.last_attack_time < 1:  # 1 saniye cooldown
                return
                
            # Mob algılama
            if self.settings.get("combat.attack_mobs", False):
                mobs = self.detect_mobs()
                if mobs:
                    self.attack_target(mobs[0])
                    self.last_attack_time = current_time
                    
            # Stone algılama
            if self.settings.get("combat.attack_stones", False):
                stones = self.detect_stones()
                if stones:
                    self.attack_target(stones[0])
                    self.last_attack_time = current_time
                    
        except Exception as e:
            print(f"Combat system hatası: {e}")
            
    def detect_mobs(self) -> List[Dict]:
        """Mobları algıla"""
        # Simülasyon
        if random.random() < 0.3:
            return [{"name": "Mob", "position": {"x": random.randint(100, 500), "y": random.randint(100, 400)}}]
        return []
        
    def detect_stones(self) -> List[Dict]:
        """Metinleri algıla"""
        # Simülasyon
        if random.random() < 0.2:
            return [{"name": "Stone", "position": {"x": random.randint(100, 500), "y": random.randint(100, 400)}}]
        return []
        
    def attack_target(self, target: Dict):
        """Hedefe saldır"""
        try:
            # Hedefe tıkla
            pos = target["position"]
            pyautogui.click(pos["x"], pos["y"])
            print(f"Saldırı: {target['name']}")
            
        except Exception as e:
            print(f"Saldırı hatası: {e}")
            
    def pickup_items(self):
        """Item toplama sistemi"""
        try:
            items = self.detect_items()
            item_list = self.settings.get("items.item_list", [])
            
            for item in items:
                if not item_list or item["name"] in item_list:
                    self.pickup_item(item)
                    
        except Exception as e:
            print(f"Item pickup hatası: {e}")
            
    def detect_items(self) -> List[Dict]:
        """Itemları algıla"""
        # Simülasyon
        if random.random() < 0.1:
            items = ["Sword", "Potion", "Gold", "Armor"]
            return [{"name": random.choice(items), "position": {"x": random.randint(100, 500), "y": random.randint(100, 400)}}]
        return []
        
    def pickup_item(self, item: Dict):
        """Item topla"""
        try:
            pos = item["position"]
            pyautogui.click(pos["x"], pos["y"])
            print(f"Item toplandı: {item['name']}")
            
        except Exception as e:
            print(f"Item toplama hatası: {e}")
            
    def auto_route(self):
        """Otomatik rota sistemi"""
        try:
            if not self.current_route:
                return
                
            if self.route_index >= len(self.current_route):
                self.route_index = 0  # Rotayı tekrarla
                
            target = self.current_route[self.route_index]
            
            # Hedefe git
            if self.move_to_position(target["x"], target["y"]):
                self.route_index += 1
                
        except Exception as e:
            print(f"Auto route hatası: {e}")
            
    def move_to_position(self, x: int, y: int) -> bool:
        """Belirtilen pozisyona git"""
        try:
            # Hareket simülasyonu
            pyautogui.click(x, y)
            time.sleep(0.5)
            return True
            
        except Exception as e:
            print(f"Hareket hatası: {e}")
            return False
            
    def fishing_bot(self):
        """Balık botu"""
        try:
            # Balık botu implementasyonu
            # Gerçek oyun için özel algılama gerekli
            pass
            
        except Exception as e:
            print(f"Fishing bot hatası: {e}")
            
    def spam_bot(self):
        """Spam bot"""
        try:
            current_time = time.time()
            interval = self.settings.get("spam_bot.seconds", 5)
            
            if not hasattr(self, 'last_spam_time'):
                self.last_spam_time = 0
                
            if current_time - self.last_spam_time >= interval:
                text = self.settings.get("spam_bot.text", "")
                if text:
                    pyautogui.press('enter')
                    pyautogui.typewrite(text)
                    pyautogui.press('enter')
                    self.last_spam_time = current_time
                    
        except Exception as e:
            print(f"Spam bot hatası: {e}")
            
    def play_alarm(self):
        """Alarm çal"""
        try:
            # Sistem sesi çal
            import winsound
            winsound.Beep(1000, 500)
        except:
            print("ALARM! Oyuncu algılandı!")
            
    def record_position(self):
        """Mevcut pozisyonu kaydet (rota kaydı için)"""
        if self.recording_route:
            pos = {"x": self.player_position["x"], "y": self.player_position["y"], "timestamp": time.time()}
            self.current_route.append(pos)
            
    def start_route_recording(self):
        """Rota kaydını başlat"""
        self.recording_route = True
        self.current_route = []
        print("Rota kaydı başlatıldı!")
        
    def stop_route_recording(self):
        """Rota kaydını durdur"""
        self.recording_route = False
        print(f"Rota kaydı tamamlandı! {len(self.current_route)} nokta kaydedildi.")
        
    def load_route(self, route_name: str):
        """Rota yükle"""
        try:
            self.current_route = self.settings.load_route(route_name)
            self.route_index = 0
            print(f"Rota yüklendi: {route_name}")
        except Exception as e:
            print(f"Rota yükleme hatası: {e}")
            
    def save_current_route(self, route_name: str):
        """Mevcut rotayı kaydet"""
        try:
            self.settings.save_route(route_name, self.current_route)
            print(f"Rota kaydedildi: {route_name}")
        except Exception as e:
            print(f"Rota kaydetme hatası: {e}")