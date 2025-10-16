#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GGBOT v2 - Mobile2 Global Bot
Öğretmen ödevi için geliştirilmiş oyun botu

Author: Student
Date: 2025
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.bot_engine import BotEngine
from src.gui.main_window import MainWindow
from src.config.settings import Settings

class GGBOT:
    """Ana bot sınıfı"""
    
    def __init__(self):
        self.settings = Settings()
        self.bot_engine = BotEngine(self.settings)
        self.gui = None
        self.running = False
        
    def start_gui(self):
        """GUI'yi başlat"""
        root = tk.Tk()
        root.title("GGBOT v2 - Mobile2 Global Bot")
        root.geometry("800x600")
        root.resizable(True, True)
        
        # Icon ayarla (varsa)
        try:
            root.iconbitmap("assets/icon.ico")
        except:
            pass
            
        self.gui = MainWindow(root, self.bot_engine, self.settings)
        
        # Kapanış eventi
        root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # GUI'yi başlat
        root.mainloop()
        
    def on_closing(self):
        """Uygulama kapatılırken çağrılır"""
        if self.running:
            self.stop_bot()
        
        # Ayarları kaydet
        self.settings.save_settings()
        
        if self.gui:
            self.gui.root.quit()
            self.gui.root.destroy()
            
    def start_bot(self):
        """Bot'u başlat"""
        if not self.running:
            self.running = True
            self.bot_thread = threading.Thread(target=self.bot_engine.start, daemon=True)
            self.bot_thread.start()
            print("Bot başlatıldı!")
            
    def stop_bot(self):
        """Bot'u durdur"""
        if self.running:
            self.running = False
            self.bot_engine.stop()
            print("Bot durduruldu!")

def main():
    """Ana fonksiyon"""
    print("GGBOT v2 - Mobile2 Global Bot")
    print("=" * 40)
    print("Öğretmen ödevi için geliştirilmiştir.")
    print("=" * 40)
    
    try:
        # Bot'u başlat
        bot = GGBOT()
        bot.start_gui()
        
    except KeyboardInterrupt:
        print("\nBot kapatılıyor...")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        messagebox.showerror("Hata", f"Bot başlatılırken hata oluştu:\n{e}")
    finally:
        print("Bot kapatıldı.")

if __name__ == "__main__":
    main()