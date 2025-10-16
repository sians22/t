#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ana GUI penceresi
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Dict, Any

from .tabs.potion_tab import PotionTab
from .tabs.combat_tab import CombatTab
from .tabs.movement_tab import MovementTab
from .tabs.items_tab import ItemsTab
from .tabs.player_tab import PlayerTab
from .tabs.route_tab import RouteTab
from .tabs.fishing_tab import FishingTab
from .tabs.settings_tab import SettingsTab

class MainWindow:
    """Ana GUI penceresi"""
    
    def __init__(self, root: tk.Tk, bot_engine, settings):
        self.root = root
        self.bot_engine = bot_engine
        self.settings = settings
        
        self.setup_ui()
        self.setup_status_bar()
        self.setup_menu()
        
        # Bot durumu
        self.bot_running = False
        
        # Status güncelleme thread'i
        self.status_thread = threading.Thread(target=self.update_status_loop, daemon=True)
        self.status_thread.start()
        
    def setup_ui(self):
        """UI'yi kur"""
        # Ana frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Başlık
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="GGBOT v2 - Mobile2 Global Bot", 
                               font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Bot kontrol butonları
        control_frame = ttk.Frame(title_frame)
        control_frame.pack(side=tk.RIGHT)
        
        self.start_button = ttk.Button(control_frame, text="Bot Başlat", 
                                      command=self.toggle_bot, style="Accent.TButton")
        self.start_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.pause_button = ttk.Button(control_frame, text="Duraklat", 
                                      command=self.pause_bot, state=tk.DISABLED)
        self.pause_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.save_button = ttk.Button(control_frame, text="Ayarları Kaydet", 
                                     command=self.save_settings)
        self.save_button.pack(side=tk.LEFT)
        
        # Notebook (sekmeler)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Sekmeleri oluştur
        self.create_tabs()
        
    def create_tabs(self):
        """Sekmeleri oluştur"""
        # Potion sekmesi
        self.potion_tab = PotionTab(self.notebook, self.settings)
        self.notebook.add(self.potion_tab.frame, text="Potions & Basic")
        
        # Combat sekmesi
        self.combat_tab = CombatTab(self.notebook, self.settings)
        self.notebook.add(self.combat_tab.frame, text="Combat & ESP")
        
        # Movement sekmesi
        self.movement_tab = MovementTab(self.notebook, self.settings)
        self.notebook.add(self.movement_tab.frame, text="Movement & Speed")
        
        # Items sekmesi
        self.items_tab = ItemsTab(self.notebook, self.settings)
        self.notebook.add(self.items_tab.frame, text="Items & Pickup")
        
        # Player sekmesi
        self.player_tab = PlayerTab(self.notebook, self.settings)
        self.notebook.add(self.player_tab.frame, text="Player Detection")
        
        # Route sekmesi
        self.route_tab = RouteTab(self.notebook, self.settings, self.bot_engine)
        self.notebook.add(self.route_tab.frame, text="Auto Route")
        
        # Fishing sekmesi
        self.fishing_tab = FishingTab(self.notebook, self.settings)
        self.notebook.add(self.fishing_tab.frame, text="Fishing Bot")
        
        # Settings sekmesi
        self.settings_tab = SettingsTab(self.notebook, self.settings)
        self.notebook.add(self.settings_tab.frame, text="Settings & Spam")
        
    def setup_status_bar(self):
        """Durum çubuğunu kur"""
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        # Bot durumu
        self.status_label = ttk.Label(self.status_frame, text="Bot: Durduruldu")
        self.status_label.pack(side=tk.LEFT)
        
        # Ayırıcı
        ttk.Separator(self.status_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Oyun durumu
        self.game_status_label = ttk.Label(self.status_frame, text="Oyun: Bulunamadı")
        self.game_status_label.pack(side=tk.LEFT)
        
        # Ayırıcı
        ttk.Separator(self.status_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Player stats
        self.stats_label = ttk.Label(self.status_frame, text="HP: 100% | MP: 100%")
        self.stats_label.pack(side=tk.LEFT)
        
        # Hotkey bilgisi
        hotkey_label = ttk.Label(self.status_frame, text="F9: Bot Aç/Kapat | F10: Duraklat | F11: Acil Durdur")
        hotkey_label.pack(side=tk.RIGHT)
        
    def setup_menu(self):
        """Menü çubuğunu kur"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Ayarları Yükle", command=self.load_settings_file)
        file_menu.add_command(label="Ayarları Kaydet", command=self.save_settings_file)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
        # Bot menüsü
        bot_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bot", menu=bot_menu)
        bot_menu.add_command(label="Başlat/Durdur", command=self.toggle_bot)
        bot_menu.add_command(label="Duraklat", command=self.pause_bot)
        bot_menu.add_command(label="Acil Durdur", command=self.emergency_stop)
        bot_menu.add_separator()
        bot_menu.add_command(label="Varsayılan Ayarlar", command=self.reset_to_defaults)
        
        # Yardım menüsü
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Hotkey'ler", command=self.show_hotkeys)
        help_menu.add_command(label="Hakkında", command=self.show_about)
        
    def toggle_bot(self):
        """Bot'u başlat/durdur"""
        try:
            if not self.bot_running:
                # Bot'u başlat
                self.bot_engine.start_bot()
                self.bot_running = True
                self.start_button.config(text="Bot Durdur")
                self.pause_button.config(state=tk.NORMAL)
                self.status_label.config(text="Bot: Çalışıyor")
                print("Bot başlatıldı!")
            else:
                # Bot'u durdur
                self.bot_engine.stop_bot()
                self.bot_running = False
                self.start_button.config(text="Bot Başlat")
                self.pause_button.config(state=tk.DISABLED)
                self.status_label.config(text="Bot: Durduruldu")
                print("Bot durduruldu!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Bot başlatılırken/durdurulurken hata:\n{e}")
            
    def pause_bot(self):
        """Bot'u duraklat/devam ettir"""
        try:
            if self.bot_running:
                if not self.bot_engine.paused:
                    self.bot_engine.paused = True
                    self.pause_button.config(text="Devam Et")
                    self.status_label.config(text="Bot: Duraklatıldı")
                else:
                    self.bot_engine.paused = False
                    self.pause_button.config(text="Duraklat")
                    self.status_label.config(text="Bot: Çalışıyor")
                    
        except Exception as e:
            messagebox.showerror("Hata", f"Bot duraklatılırken hata:\n{e}")
            
    def emergency_stop(self):
        """Acil durdurma"""
        try:
            if self.bot_running:
                self.bot_engine.stop()
                self.bot_running = False
                self.start_button.config(text="Bot Başlat")
                self.pause_button.config(state=tk.DISABLED)
                self.status_label.config(text="Bot: ACİL DURDURULDU")
                messagebox.showwarning("Acil Durdurma", "Bot acil olarak durduruldu!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Acil durdurma hatası:\n{e}")
            
    def save_settings(self):
        """Ayarları kaydet"""
        try:
            # Tüm sekmelerden ayarları al
            self.potion_tab.save_settings()
            self.combat_tab.save_settings()
            self.movement_tab.save_settings()
            self.items_tab.save_settings()
            self.player_tab.save_settings()
            self.route_tab.save_settings()
            self.fishing_tab.save_settings()
            self.settings_tab.save_settings()
            
            # Ayarları dosyaya kaydet
            self.settings.save_settings()
            
            messagebox.showinfo("Başarılı", "Ayarlar kaydedildi!")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Ayarlar kaydedilirken hata:\n{e}")
            
    def load_settings_file(self):
        """Ayar dosyası yükle"""
        try:
            filename = filedialog.askopenfilename(
                title="Ayar Dosyası Seç",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                import json
                with open(filename, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    
                self.settings.settings.update(loaded_settings)
                
                # UI'yi güncelle
                self.refresh_ui()
                
                messagebox.showinfo("Başarılı", "Ayarlar yüklendi!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ayar dosyası yüklenirken hata:\n{e}")
            
    def save_settings_file(self):
        """Ayarları dosyaya kaydet"""
        try:
            filename = filedialog.asksaveasfilename(
                title="Ayarları Kaydet",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if filename:
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.settings.settings, f, indent=4, ensure_ascii=False)
                    
                messagebox.showinfo("Başarılı", "Ayarlar dosyaya kaydedildi!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Ayar dosyası kaydedilirken hata:\n{e}")
            
    def reset_to_defaults(self):
        """Varsayılan ayarlara dön"""
        try:
            result = messagebox.askyesno("Onay", "Tüm ayarları varsayılan değerlere döndürmek istiyor musunuz?")
            
            if result:
                self.settings.settings = self.settings.default_settings.copy()
                self.refresh_ui()
                messagebox.showinfo("Başarılı", "Ayarlar varsayılan değerlere döndürüldü!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Varsayılan ayarlara dönerken hata:\n{e}")
            
    def refresh_ui(self):
        """UI'yi yenile"""
        try:
            # Tüm sekmeleri yenile
            self.potion_tab.load_settings()
            self.combat_tab.load_settings()
            self.movement_tab.load_settings()
            self.items_tab.load_settings()
            self.player_tab.load_settings()
            self.route_tab.load_settings()
            self.fishing_tab.load_settings()
            self.settings_tab.load_settings()
            
        except Exception as e:
            print(f"UI yenilenirken hata: {e}")
            
    def update_status_loop(self):
        """Durum güncellemesi döngüsü"""
        import time
        
        while True:
            try:
                # Oyun durumunu kontrol et
                if hasattr(self.bot_engine, 'game_utils'):
                    if self.bot_engine.game_utils.is_game_active():
                        self.game_status_label.config(text="Oyun: Aktif")
                    else:
                        self.game_status_label.config(text="Oyun: Bulunamadı")
                        
                # Player stats'ı güncelle
                if hasattr(self.bot_engine, 'player_stats'):
                    stats = self.bot_engine.player_stats
                    hp_percent = int((stats['health'] / stats['max_health']) * 100)
                    mp_percent = int((stats['mana'] / stats['max_mana']) * 100)
                    self.stats_label.config(text=f"HP: {hp_percent}% | MP: {mp_percent}%")
                    
            except Exception as e:
                print(f"Status güncelleme hatası: {e}")
                
            time.sleep(1)  # 1 saniyede bir güncelle
            
    def show_hotkeys(self):
        """Hotkey bilgilerini göster"""
        hotkey_info = \"\"\"\nHotkey Bilgileri:\n\nF9: Bot'u Başlat/Durdur\nF10: Bot'u Duraklat/Devam Ettir\nF11: Acil Durdurma\n\nBot Kontrolleri:\n- Bot çalışırken oyun penceresinin aktif olması gerekir\n- Bot durdurulduğunda tüm otomatik işlemler durur\n- Acil durdurma tüm işlemleri anında sonlandırır\n\"\"\"
        
        messagebox.showinfo("Hotkey Bilgileri", hotkey_info)
        
    def show_about(self):
        \"\"\"Hakkında bilgilerini göster\"\"\"
        about_info = \"\"\"\nGGBOT v2 - Mobile2 Global Bot\n\nÖğretmen ödevi için geliştirilmiştir.\n\nÖzellikler:\n- Otomatik potion kullanımı\n- Savaş sistemi\n- Hareket hack'leri\n- Item toplama\n- Oyuncu algılama\n- Rota sistemi\n- Balık botu\n\nGeliştirici: Öğrenci\nTarih: 2025\n\"\"\"
        
        messagebox.showinfo("Hakkında", about_info)