#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GGBOT v2 Demo - Tkinter olmadan çalışan demo sürüm
"""

import sys
import os
import time
import json
from threading import Thread

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config.settings import Settings

class DemoBot:
    """Demo bot sınıfı - GUI olmadan çalışır"""
    
    def __init__(self):
        print("🎮 GGBOT v2 - Mobile2 Global Bot Demo")
        print("=" * 50)
        print("Öğretmen ödevi için geliştirilmiştir.")
        print("=" * 50)
        
        self.settings = Settings()
        self.running = False
        
        # Demo ayarları
        self.demo_stats = {
            "health": 100,
            "mana": 100,
            "potions_used": 0,
            "mobs_killed": 0,
            "items_collected": 0
        }
        
    def start_demo(self):
        """Demo'yu başlat"""
        print("\n📋 Mevcut Ayarlar:")
        print("-" * 30)
        
        # Red Potion ayarları
        red_enabled = self.settings.get("red_potion.enabled", True)
        red_threshold = self.settings.get("red_potion.health_percentage", 50)
        red_key = self.settings.get("red_potion.key", "F1")
        print(f"🔴 Red Potion: {'Aktif' if red_enabled else 'Pasif'} - {red_threshold}% - {red_key}")
        
        # Blue Potion ayarları
        blue_enabled = self.settings.get("blue_potion.enabled", True)
        blue_threshold = self.settings.get("blue_potion.mana_percentage", 30)
        blue_key = self.settings.get("blue_potion.key", "F2")
        print(f"🔵 Blue Potion: {'Aktif' if blue_enabled else 'Pasif'} - {blue_threshold}% - {blue_key}")
        
        # Combat ayarları
        attack_mobs = self.settings.get("combat.attack_mobs", True)
        attack_stones = self.settings.get("combat.attack_stones", False)
        print(f"⚔️  Combat: Mobs={'Aktif' if attack_mobs else 'Pasif'}, Stones={'Aktif' if attack_stones else 'Pasif'}")
        
        # Speed hack ayarları
        speed_enabled = self.settings.get("speed_hacks.movement_speed.enabled", False)
        speed_amount = self.settings.get("speed_hacks.movement_speed.amount", 100)
        print(f"🏃 Speed Hack: {'Aktif' if speed_enabled else 'Pasif'} - {speed_amount}%")
        
        print("\n🚀 Demo başlatılıyor...")
        print("Ctrl+C ile durdurun")
        print("-" * 50)
        
        self.running = True
        
        try:
            # Demo döngüsü
            while self.running:
                self.demo_loop()
                time.sleep(2)  # 2 saniyede bir güncelle
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Demo durduruldu!")
            self.running = False
            
    def demo_loop(self):
        """Demo döngüsü - bot işlemlerini simüle eder"""
        
        # Rastgele olaylar simüle et
        import random
        
        # HP/MP azaltma simülasyonu
        if random.random() < 0.3:  # %30 ihtimal
            self.demo_stats["health"] -= random.randint(5, 15)
            self.demo_stats["mana"] -= random.randint(3, 10)
            
        # Potion kullanımı kontrolü
        red_threshold = self.settings.get("red_potion.health_percentage", 50)
        blue_threshold = self.settings.get("blue_potion.mana_percentage", 30)
        
        if self.demo_stats["health"] <= red_threshold and self.settings.get("red_potion.enabled", True):
            self.use_red_potion()
            
        if self.demo_stats["mana"] <= blue_threshold and self.settings.get("blue_potion.enabled", True):
            self.use_blue_potion()
            
        # Combat simülasyonu
        if self.settings.get("combat.attack_mobs", True) and random.random() < 0.2:
            self.attack_mob()
            
        # Item toplama simülasyonu
        if random.random() < 0.15:
            self.collect_item()
            
        # Durumu göster
        self.show_status()
        
    def use_red_potion(self):
        """Kırmızı potion kullan"""
        key = self.settings.get("red_potion.key", "F1")
        self.demo_stats["health"] = min(100, self.demo_stats["health"] + 50)
        self.demo_stats["potions_used"] += 1
        print(f"🔴 Red Potion kullanıldı ({key}) - HP: {self.demo_stats['health']}%")
        
    def use_blue_potion(self):
        """Mavi potion kullan"""
        key = self.settings.get("blue_potion.key", "F2")
        self.demo_stats["mana"] = min(100, self.demo_stats["mana"] + 40)
        self.demo_stats["potions_used"] += 1
        print(f"🔵 Blue Potion kullanıldı ({key}) - MP: {self.demo_stats['mana']}%")
        
    def attack_mob(self):
        """Mob'a saldır"""
        import random
        mobs = ["Orc", "Goblin", "Skeleton", "Wolf", "Spider"]
        mob = random.choice(mobs)
        self.demo_stats["mobs_killed"] += 1
        print(f"⚔️  {mob} öldürüldü! Toplam: {self.demo_stats['mobs_killed']}")
        
    def collect_item(self):
        """Item topla"""
        import random
        items = ["Gold", "Potion", "Sword", "Shield", "Ring"]
        item = random.choice(items)
        self.demo_stats["items_collected"] += 1
        print(f"📦 {item} toplandı! Toplam: {self.demo_stats['items_collected']}")
        
    def show_status(self):
        """Durumu göster"""
        hp = self.demo_stats["health"]
        mp = self.demo_stats["mana"]
        
        # HP/MP barları
        hp_bar = "█" * (hp // 10) + "░" * (10 - hp // 10)
        mp_bar = "█" * (mp // 10) + "░" * (10 - mp // 10)
        
        print(f"\r💚 HP: [{hp_bar}] {hp:3d}% | 💙 MP: [{mp_bar}] {mp:3d}% | "
              f"🧪 Potions: {self.demo_stats['potions_used']} | "
              f"⚔️ Kills: {self.demo_stats['mobs_killed']} | "
              f"📦 Items: {self.demo_stats['items_collected']}", end="", flush=True)

def main():
    """Ana fonksiyon"""
    try:
        demo = DemoBot()
        demo.start_demo()
        
        print("\n\n📊 Demo İstatistikleri:")
        print("-" * 30)
        print(f"🧪 Kullanılan Potion: {demo.demo_stats['potions_used']}")
        print(f"⚔️  Öldürülen Mob: {demo.demo_stats['mobs_killed']}")
        print(f"📦 Toplanan Item: {demo.demo_stats['items_collected']}")
        print(f"💚 Son HP: {demo.demo_stats['health']}%")
        print(f"💙 Son MP: {demo.demo_stats['mana']}%")
        
        print("\n🎯 Demo tamamlandı!")
        print("Gerçek bot için Windows'ta 'python main.py' çalıştırın.")
        
    except Exception as e:
        print(f"\n❌ Demo hatası: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()