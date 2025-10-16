#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oyun ile ilgili yardımcı fonksiyonlar
"""

import win32gui
import win32con
import win32api
import psutil
import time
from typing import Optional, Tuple, List

class GameUtils:
    """Oyun yardımcı fonksiyonları"""
    
    def __init__(self):
        self.game_window_title = "Mobile2 Global"  # Oyun pencere başlığı
        self.game_process_name = "mobile2.exe"    # Oyun process adı
        self.game_hwnd = None
        
    def find_game_window(self) -> Optional[int]:
        """Oyun penceresini bul"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if self.game_window_title.lower() in window_title.lower():
                        windows.append(hwnd)
                return True
                
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.game_hwnd = windows[0]
                return self.game_hwnd
                
        except Exception as e:
            print(f"Oyun penceresi aranırken hata: {e}")
            
        return None
        
    def is_game_active(self) -> bool:
        """Oyun aktif mi kontrol et"""
        try:
            if not self.game_hwnd:
                self.game_hwnd = self.find_game_window()
                
            if self.game_hwnd:
                # Pencere görünür mü?
                if not win32gui.IsWindowVisible(self.game_hwnd):
                    return False
                    
                # Pencere minimize edilmiş mi?
                if win32gui.IsIconic(self.game_hwnd):
                    return False
                    
                return True
                
        except Exception as e:
            print(f"Oyun aktiflik kontrolünde hata: {e}")
            
        return False
        
    def get_game_window_rect(self) -> Optional[Tuple[int, int, int, int]]:
        """Oyun penceresi koordinatlarını al"""
        try:
            if not self.game_hwnd:
                self.game_hwnd = self.find_game_window()
                
            if self.game_hwnd:
                rect = win32gui.GetWindowRect(self.game_hwnd)
                return rect  # (left, top, right, bottom)
                
        except Exception as e:
            print(f"Pencere koordinatları alınırken hata: {e}")
            
        return None
        
    def activate_game_window(self) -> bool:
        """Oyun penceresini aktif et"""
        try:
            if not self.game_hwnd:
                self.game_hwnd = self.find_game_window()
                
            if self.game_hwnd:
                # Pencereyi öne getir
                win32gui.SetForegroundWindow(self.game_hwnd)
                
                # Minimize edilmişse geri yükle
                if win32gui.IsIconic(self.game_hwnd):
                    win32gui.ShowWindow(self.game_hwnd, win32con.SW_RESTORE)
                    
                return True
                
        except Exception as e:
            print(f"Oyun penceresi aktif edilirken hata: {e}")
            
        return False
        
    def is_game_process_running(self) -> bool:
        """Oyun process'i çalışıyor mu kontrol et"""
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'].lower() == self.game_process_name.lower():
                    return True
        except Exception as e:
            print(f"Process kontrolünde hata: {e}")
            
        return False
        
    def get_game_process_id(self) -> Optional[int]:
        """Oyun process ID'sini al"""
        try:
            for process in psutil.process_iter(['pid', 'name']):
                if process.info['name'].lower() == self.game_process_name.lower():
                    return process.info['pid']
        except Exception as e:
            print(f"Process ID alınırken hata: {e}")
            
        return None
        
    def click_in_game(self, x: int, y: int, button: str = 'left') -> bool:
        """Oyun içinde tıklama yap"""
        try:
            if not self.activate_game_window():
                return False
                
            # Oyun penceresi koordinatlarını al
            rect = self.get_game_window_rect()
            if not rect:
                return False
                
            # Relatif koordinatları mutlak koordinatlara çevir
            abs_x = rect[0] + x
            abs_y = rect[1] + y
            
            # Tıklama yap
            if button.lower() == 'left':
                win32api.SetCursorPos((abs_x, abs_y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, abs_x, abs_y, 0, 0)
                time.sleep(0.05)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, abs_x, abs_y, 0, 0)
            elif button.lower() == 'right':
                win32api.SetCursorPos((abs_x, abs_y))
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, abs_x, abs_y, 0, 0)
                time.sleep(0.05)
                win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, abs_x, abs_y, 0, 0)
                
            return True
            
        except Exception as e:
            print(f"Oyun içi tıklama hatası: {e}")
            return False
            
    def send_key_to_game(self, key: str) -> bool:
        """Oyuna tuş gönder"""
        try:
            if not self.activate_game_window():
                return False
                
            # Virtual key code'ları
            key_codes = {
                'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
                'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77,
                'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
                'SPACE': 0x20, 'ENTER': 0x0D, 'ESC': 0x1B,
                'TAB': 0x09, 'SHIFT': 0x10, 'CTRL': 0x11, 'ALT': 0x12,
                '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34, '5': 0x35,
                '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39, '0': 0x30,
                'A': 0x41, 'B': 0x42, 'C': 0x43, 'D': 0x44, 'E': 0x45,
                'F': 0x46, 'G': 0x47, 'H': 0x48, 'I': 0x49, 'J': 0x4A,
                'K': 0x4B, 'L': 0x4C, 'M': 0x4D, 'N': 0x4E, 'O': 0x4F,
                'P': 0x50, 'Q': 0x51, 'R': 0x52, 'S': 0x53, 'T': 0x54,
                'U': 0x55, 'V': 0x56, 'W': 0x57, 'X': 0x58, 'Y': 0x59, 'Z': 0x5A
            }
            
            key_upper = key.upper()
            if key_upper in key_codes:
                vk_code = key_codes[key_upper]
                
                # Tuşa bas
                win32api.keybd_event(vk_code, 0, 0, 0)
                time.sleep(0.05)
                # Tuşu bırak
                win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
                
                return True
            else:
                print(f"Bilinmeyen tuş: {key}")
                return False
                
        except Exception as e:
            print(f"Tuş gönderme hatası: {e}")
            return False
            
    def send_text_to_game(self, text: str) -> bool:
        """Oyuna metin gönder"""
        try:
            if not self.activate_game_window():
                return False
                
            for char in text:
                if char == ' ':
                    self.send_key_to_game('SPACE')
                elif char.isalnum():
                    self.send_key_to_game(char)
                time.sleep(0.02)  # Karakterler arası bekleme
                
            return True
            
        except Exception as e:
            print(f"Metin gönderme hatası: {e}")
            return False
            
    def get_pixel_color(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Belirtilen koordinattaki pixel rengini al"""
        try:
            rect = self.get_game_window_rect()
            if not rect:
                return None
                
            abs_x = rect[0] + x
            abs_y = rect[1] + y
            
            # Desktop DC'sini al
            hdc = win32gui.GetDC(0)
            pixel = win32gui.GetPixel(hdc, abs_x, abs_y)
            win32gui.ReleaseDC(0, hdc)
            
            # RGB değerlerini ayır
            r = pixel & 0xFF
            g = (pixel >> 8) & 0xFF
            b = (pixel >> 16) & 0xFF
            
            return (r, g, b)
            
        except Exception as e:
            print(f"Pixel rengi alınırken hata: {e}")
            return None
            
    def wait_for_color_change(self, x: int, y: int, timeout: float = 5.0) -> bool:
        """Belirtilen koordinatta renk değişimini bekle"""
        try:
            initial_color = self.get_pixel_color(x, y)
            if not initial_color:
                return False
                
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                current_color = self.get_pixel_color(x, y)
                if current_color and current_color != initial_color:
                    return True
                time.sleep(0.1)
                
            return False
            
        except Exception as e:
            print(f"Renk değişimi beklenirken hata: {e}")
            return False
            
    def is_color_at_position(self, x: int, y: int, target_color: Tuple[int, int, int], tolerance: int = 10) -> bool:
        """Belirtilen koordinatta belirtilen renk var mı kontrol et"""
        try:
            current_color = self.get_pixel_color(x, y)
            if not current_color:
                return False
                
            # Renk toleransı ile karşılaştır
            r_diff = abs(current_color[0] - target_color[0])
            g_diff = abs(current_color[1] - target_color[1])
            b_diff = abs(current_color[2] - target_color[2])
            
            return r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance
            
        except Exception as e:
            print(f"Renk kontrolünde hata: {e}")
            return False