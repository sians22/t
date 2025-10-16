#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ayarlar ve konfigürasyon yönetimi
"""

import json
import os
from typing import Dict, Any, List

class Settings:
    """Bot ayarları sınıfı"""
    
    def __init__(self):
        self.config_file = "config/bot_settings.json"
        self.config_dir = "config"
        self.routes_dir = "config/routes"
        self.items_dir = "config/items"
        
        # Varsayılan ayarlar
        self.default_settings = {
            # Potion ayarları
            "red_potion": {
                "enabled": True,
                "health_percentage": 50,
                "key": "F1"
            },
            "blue_potion": {
                "enabled": True,
                "mana_percentage": 30,
                "key": "F2"
            },
            
            # Hack ayarları
            "wallhack": {
                "enabled": False
            },
            "restart_here": {
                "enabled": False,
                "position": {"x": 0, "y": 0}
            },
            "upgrade_item_slot1": {
                "enabled": False,
                "key": "+"
            },
            
            # Farm ayarları
            "farm": {
                "enabled": False,
                "range": 100,
                "fixed_position": {"x": 0, "y": 0, "enabled": False}
            },
            
            # Combat ayarları
            "combat": {
                "attack_mobs": True,
                "attack_stones": False,
                "attack_mob_groups": False,
                "group_amount": 1,
                "base_skills": False,
                "stop_on_no_red_potions": True
            },
            
            # ESP ayarları
            "esp": {
                "players": False,
                "stones": False
            },
            
            # Speed hacks
            "speed_hacks": {
                "wait_hack": {
                    "enabled": False,
                    "amount": 1000
                },
                "wait_hack_range": {
                    "enabled": False,
                    "amount": 1000
                },
                "movement_speed": {
                    "enabled": False,
                    "amount": 100
                }
            },
            
            # Item sistemi
            "items": {
                "pickup_filter": False,
                "drop_no_bonus": False,
                "item_list": []
            },
            
            # Player detection
            "player_detection": {
                "whitelist": [],
                "range": 100,
                "range_enabled": False,
                "on_player": {
                    "stop_wait_range": False,
                    "stop_speedhacks": False,
                    "stop_bot": False,
                    "quit_game": False,
                    "sound_alarm": False
                },
                "on_gm": {
                    "stop_wait_range": True,
                    "stop_speedhacks": True,
                    "stop_bot": True,
                    "quit_game": False,
                    "sound_alarm": True
                }
            },
            
            # Spam bot
            "spam_bot": {
                "enabled": False,
                "text": "",
                "seconds": 5
            },
            
            # Fishing bot
            "fishing": {
                "kill_fish": False,
                "grill_fish": False,
                "drop_dead_fish": False,
                "drop_hair_color": False,
                "dead_alarm": False,
                "delay_ms": 2650
            },
            
            # Route sistemi
            "routes": {
                "current_route": "",
                "auto_route_enabled": False,
                "recording": False
            }
        }
        
        self.settings = self.default_settings.copy()
        self.create_directories()
        self.load_settings()
        
    def create_directories(self):
        """Gerekli dizinleri oluştur"""
        directories = [self.config_dir, self.routes_dir, self.items_dir]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                
    def load_settings(self):
        """Ayarları dosyadan yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
                print("Ayarlar yüklendi.")
            else:
                print("Ayar dosyası bulunamadı, varsayılan ayarlar kullanılıyor.")
        except Exception as e:
            print(f"Ayarlar yüklenirken hata: {e}")
            
    def save_settings(self):
        """Ayarları dosyaya kaydet"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
            print("Ayarlar kaydedildi.")
        except Exception as e:
            print(f"Ayarlar kaydedilirken hata: {e}")
            
    def get(self, key: str, default=None):
        """Ayar değeri al"""
        keys = key.split('.')
        value = self.settings
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """Ayar değeri belirle"""
        keys = key.split('.')
        setting = self.settings
        
        for k in keys[:-1]:
            if k not in setting:
                setting[k] = {}
            setting = setting[k]
            
        setting[keys[-1]] = value
        
    def save_route(self, name: str, route_data: List[Dict]):
        """Rota kaydet"""
        try:
            route_file = os.path.join(self.routes_dir, f"{name}.json")
            with open(route_file, 'w', encoding='utf-8') as f:
                json.dump(route_data, f, indent=4, ensure_ascii=False)
            print(f"Rota kaydedildi: {name}")
        except Exception as e:
            print(f"Rota kaydedilirken hata: {e}")
            
    def load_route(self, name: str) -> List[Dict]:
        """Rota yükle"""
        try:
            route_file = os.path.join(self.routes_dir, f"{name}.json")
            if os.path.exists(route_file):
                with open(route_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Rota yüklenirken hata: {e}")
        return []
        
    def delete_route(self, name: str):
        """Rota sil"""
        try:
            route_file = os.path.join(self.routes_dir, f"{name}.json")
            if os.path.exists(route_file):
                os.remove(route_file)
                print(f"Rota silindi: {name}")
        except Exception as e:
            print(f"Rota silinirken hata: {e}")
            
    def get_routes(self) -> List[str]:
        """Mevcut rotaları listele"""
        try:
            routes = []
            if os.path.exists(self.routes_dir):
                for file in os.listdir(self.routes_dir):
                    if file.endswith('.json'):
                        routes.append(file[:-5])  # .json uzantısını kaldır
            return routes
        except Exception as e:
            print(f"Rotalar listelenirken hata: {e}")
            return []
            
    def save_item_list(self, name: str, items: List[str]):
        """Item listesi kaydet"""
        try:
            items_file = os.path.join(self.items_dir, f"{name}.json")
            with open(items_file, 'w', encoding='utf-8') as f:
                json.dump(items, f, indent=4, ensure_ascii=False)
            print(f"Item listesi kaydedildi: {name}")
        except Exception as e:
            print(f"Item listesi kaydedilirken hata: {e}")
            
    def load_item_list(self, name: str) -> List[str]:
        """Item listesi yükle"""
        try:
            items_file = os.path.join(self.items_dir, f"{name}.json")
            if os.path.exists(items_file):
                with open(items_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Item listesi yüklenirken hata: {e}")
        return []
        
    def get_item_lists(self) -> List[str]:
        """Mevcut item listelerini getir"""
        try:
            lists = []
            if os.path.exists(self.items_dir):
                for file in os.listdir(self.items_dir):
                    if file.endswith('.json'):
                        lists.append(file[:-5])
            return lists
        except Exception as e:
            print(f"Item listeleri listelenirken hata: {e}")
            return []