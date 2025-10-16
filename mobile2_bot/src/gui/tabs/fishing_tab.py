#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fishing Bot sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox

class FishingTab:
    """Fishing Bot sekmesi"""
    
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """UI'yi kur"""
        # Ana scroll frame
        canvas = tk.Canvas(self.frame)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Fishing Bot Kontrolleri
        control_group = ttk.LabelFrame(scrollable_frame, text="Balık Botu Kontrolleri", padding=10)
        control_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Bot durumu
        self.fishing_status_label = ttk.Label(control_group, text="Durum: Durduruldu", 
                                             font=("Arial", 10, "bold"))
        self.fishing_status_label.pack(pady=5)
        
        # Kontrol butonları
        control_buttons_frame = ttk.Frame(control_group)
        control_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.start_fishing_btn = ttk.Button(control_buttons_frame, text="Balık Botunu Başlat", 
                                           command=self.start_fishing_bot)
        self.start_fishing_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_fishing_btn = ttk.Button(control_buttons_frame, text="Balık Botunu Durdur", 
                                          command=self.stop_fishing_bot, state=tk.DISABLED)
        self.stop_fishing_btn.pack(side=tk.LEFT, padx=2)
        
        # Fishing Özellikleri
        features_group = ttk.LabelFrame(scrollable_frame, text="Balık Botu Özellikleri", padding=10)
        features_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.kill_fish = tk.BooleanVar()
        kill_fish_check = ttk.Checkbutton(features_group, text="Kill Fish (Balıkları öldür)", 
                                         variable=self.kill_fish)
        kill_fish_check.pack(anchor=tk.W, pady=2)
        
        self.grill_fish = tk.BooleanVar()
        grill_fish_check = ttk.Checkbutton(features_group, text="Grill Fish (Balıkları ızgara yap)", 
                                          variable=self.grill_fish)
        grill_fish_check.pack(anchor=tk.W, pady=2)
        
        self.drop_dead_fish = tk.BooleanVar()
        drop_dead_check = ttk.Checkbutton(features_group, text="Drop Dead Fish (Ölü balıkları yere at)", 
                                         variable=self.drop_dead_fish)
        drop_dead_check.pack(anchor=tk.W, pady=2)
        
        self.drop_hair_color = tk.BooleanVar()
        drop_hair_check = ttk.Checkbutton(features_group, text="Drop Hair Color (Saç boyalarını yere at)", 
                                         variable=self.drop_hair_color)
        drop_hair_check.pack(anchor=tk.W, pady=2)
        
        self.dead_alarm = tk.BooleanVar()
        dead_alarm_check = ttk.Checkbutton(features_group, text="Dead Alarm (Öldüğünüzde alarm öter - Sadece balık botu açıkken çalışır)", 
                                          variable=self.dead_alarm)
        dead_alarm_check.pack(anchor=tk.W, pady=2)
        
        # Delay ayarı
        delay_frame = ttk.Frame(features_group)
        delay_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(delay_frame, text="Delay ms (Milisaniye bazında süre - önerilen: 2650):").pack(side=tk.LEFT)
        self.delay_ms = tk.IntVar(value=2650)
        delay_spin = ttk.Spinbox(delay_frame, from_=1000, to=10000, width=10, 
                                textvariable=self.delay_ms)
        delay_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(delay_frame, text="ms").pack(side=tk.LEFT)
        
        # Fishing Ayarları
        settings_group = ttk.LabelFrame(scrollable_frame, text="Balık Botu Ayarları", padding=10)
        settings_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Fishing area
        area_frame = ttk.Frame(settings_group)
        area_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(area_frame, text="Balık Tutma Alanı:").pack(anchor=tk.W)
        
        area_coords_frame = ttk.Frame(area_frame)
        area_coords_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(area_coords_frame, text="X1:").pack(side=tk.LEFT)
        self.fishing_x1 = tk.IntVar(value=100)
        x1_entry = ttk.Entry(area_coords_frame, width=8, textvariable=self.fishing_x1)
        x1_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(area_coords_frame, text="Y1:").pack(side=tk.LEFT, padx=(10, 0))
        self.fishing_y1 = tk.IntVar(value=100)
        y1_entry = ttk.Entry(area_coords_frame, width=8, textvariable=self.fishing_y1)
        y1_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(area_coords_frame, text="X2:").pack(side=tk.LEFT, padx=(10, 0))
        self.fishing_x2 = tk.IntVar(value=500)
        x2_entry = ttk.Entry(area_coords_frame, width=8, textvariable=self.fishing_x2)
        x2_entry.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(area_coords_frame, text="Y2:").pack(side=tk.LEFT, padx=(10, 0))
        self.fishing_y2 = tk.IntVar(value=400)
        y2_entry = ttk.Entry(area_coords_frame, width=8, textvariable=self.fishing_y2)
        y2_entry.pack(side=tk.LEFT, padx=2)
        
        set_area_btn = ttk.Button(area_frame, text="Mevcut Ekran Alanını Ayarla", 
                                 command=self.set_fishing_area)
        set_area_btn.pack(pady=5)
        
        # Fishing hotkeys
        hotkeys_frame = ttk.Frame(settings_group)
        hotkeys_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(hotkeys_frame, text="Balık Tutma Tuşu:").pack(side=tk.LEFT)
        self.fishing_key = tk.StringVar(value="SPACE")
        fishing_key_entry = ttk.Entry(hotkeys_frame, width=10, textvariable=self.fishing_key)
        fishing_key_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(hotkeys_frame, text="Olta Atma Tuşu:").pack(side=tk.LEFT, padx=(20, 0))
        self.cast_key = tk.StringVar(value="F")
        cast_key_entry = ttk.Entry(hotkeys_frame, width=10, textvariable=self.cast_key)
        cast_key_entry.pack(side=tk.LEFT, padx=5)
        
        # Fishing İstatistikleri
        stats_group = ttk.LabelFrame(scrollable_frame, text="Balık Botu İstatistikleri", padding=10)
        stats_group.pack(fill=tk.X, padx=5, pady=5)
        
        stats_frame = ttk.Frame(stats_group)
        stats_frame.pack(fill=tk.X)
        
        # Sol kolon
        left_stats = ttk.Frame(stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_stats, text="Tutulan Balık:").pack(anchor=tk.W)
        self.caught_fish_label = ttk.Label(left_stats, text="0", font=("Arial", 12, "bold"))
        self.caught_fish_label.pack(anchor=tk.W, padx=10)
        
        ttk.Label(left_stats, text="Yapılan Izgara:").pack(anchor=tk.W, pady=(10, 0))
        self.grilled_fish_label = ttk.Label(left_stats, text="0", font=("Arial", 12, "bold"))
        self.grilled_fish_label.pack(anchor=tk.W, padx=10)
        
        # Sağ kolon
        right_stats = ttk.Frame(stats_frame)
        right_stats.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_stats, text="Atılan Dead Fish:").pack(anchor=tk.W)
        self.dropped_dead_fish_label = ttk.Label(right_stats, text="0", font=("Arial", 12, "bold"))
        self.dropped_dead_fish_label.pack(anchor=tk.W, padx=10)
        
        ttk.Label(right_stats, text="Çalışma Süresi:").pack(anchor=tk.W, pady=(10, 0))
        self.fishing_time_label = ttk.Label(right_stats, text="00:00:00", font=("Arial", 12, "bold"))
        self.fishing_time_label.pack(anchor=tk.W, padx=10)
        
        # Stats reset butonu
        reset_stats_btn = ttk.Button(stats_group, text="İstatistikleri Sıfırla", 
                                    command=self.reset_fishing_stats)
        reset_stats_btn.pack(pady=5)
        
        # Fishing Log
        log_group = ttk.LabelFrame(scrollable_frame, text="Balık Botu Kayıtları", padding=10)
        log_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        log_frame = ttk.Frame(log_group)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.fishing_log = tk.Text(log_frame, height=10, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.fishing_log.yview)
        self.fishing_log.configure(yscrollcommand=log_scrollbar.set)
        
        self.fishing_log.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Log kontrol butonları
        log_control_frame = ttk.Frame(log_group)
        log_control_frame.pack(fill=tk.X, pady=5)
        
        clear_log_btn = ttk.Button(log_control_frame, text="Kayıtları Temizle", 
                                  command=self.clear_fishing_log)
        clear_log_btn.pack(side=tk.LEFT)
        
        save_log_btn = ttk.Button(log_control_frame, text="Kayıtları Kaydet", 
                                 command=self.save_fishing_log)
        save_log_btn.pack(side=tk.LEFT, padx=5)
        
        # Test butonu
        test_fishing_btn = ttk.Button(log_control_frame, text="Balık Testi", 
                                     command=self.test_fishing)
        test_fishing_btn.pack(side=tk.LEFT, padx=5)
        
        # Gelişmiş Ayarlar
        advanced_group = ttk.LabelFrame(scrollable_frame, text="Gelişmiş Balık Ayarları", padding=10)
        advanced_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Auto bait
        self.auto_bait = tk.BooleanVar()
        auto_bait_check = ttk.Checkbutton(advanced_group, text="Otomatik Yem Kullan", 
                                         variable=self.auto_bait)
        auto_bait_check.pack(anchor=tk.W, pady=2)
        
        # Fish type filter
        fish_filter_frame = ttk.Frame(advanced_group)
        fish_filter_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(fish_filter_frame, text="Balık Türü Filtresi:").pack(side=tk.LEFT)
        self.fish_filter = tk.StringVar(value="all")
        fish_filter_combo = ttk.Combobox(fish_filter_frame, textvariable=self.fish_filter, 
                                        values=["all", "small", "medium", "large", "rare"], 
                                        state="readonly", width=15)
        fish_filter_combo.pack(side=tk.LEFT, padx=5)
        
        # Auto repair rod
        self.auto_repair = tk.BooleanVar()
        auto_repair_check = ttk.Checkbutton(advanced_group, text="Oltayı Otomatik Onar", 
                                           variable=self.auto_repair)
        auto_repair_check.pack(anchor=tk.W, pady=2)
        
        # Safe fishing (stop on player)
        self.safe_fishing = tk.BooleanVar(value=True)
        safe_fishing_check = ttk.Checkbutton(advanced_group, text="Güvenli Balık Tutma (Oyuncu geldiğinde dur)", 
                                            variable=self.safe_fishing)
        safe_fishing_check.pack(anchor=tk.W, pady=2)
        
    def start_fishing_bot(self):
        """Balık botunu başlat"""
        try:
            self.fishing_status_label.config(text="Durum: Çalışıyor", foreground="green")
            self.start_fishing_btn.config(state=tk.DISABLED)
            self.stop_fishing_btn.config(state=tk.NORMAL)
            
            self.add_fishing_log("Balık botu başlatıldı")
            
            # Timer başlat
            self.start_fishing_timer()
            
            # Bot işlemlerini başlat (simülasyon)
            self.simulate_fishing()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Balık botu başlatılırken hata:\n{e}")
            
    def stop_fishing_bot(self):
        """Balık botunu durdur"""
        try:
            self.fishing_status_label.config(text="Durum: Durduruldu", foreground="black")
            self.start_fishing_btn.config(state=tk.NORMAL)
            self.stop_fishing_btn.config(state=tk.DISABLED)
            
            self.add_fishing_log("Balık botu durduruldu")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Balık botu durdurulurken hata:\n{e}")
            
    def set_fishing_area(self):
        """Balık tutma alanını ayarla"""
        # Gerçek implementasyonda mouse ile alan seçimi yapılacak
        # Şimdilik mevcut ekran boyutlarını kullan
        try:
            import pyautogui
            screen_width, screen_height = pyautogui.size()
            
            # Ekranın ortasında bir alan ayarla
            margin = 100
            self.fishing_x1.set(margin)
            self.fishing_y1.set(margin)
            self.fishing_x2.set(screen_width - margin)
            self.fishing_y2.set(screen_height - margin)
            
            messagebox.showinfo("Alan Ayarlandı", 
                              f"Balık tutma alanı ayarlandı:\n"
                              f"({margin}, {margin}) - ({screen_width - margin}, {screen_height - margin})")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Alan ayarlanırken hata:\n{e}")
            
    def simulate_fishing(self):
        """Balık tutma simülasyonu"""
        if self.fishing_status_label.cget("text") == "Durum: Çalışıyor":
            import random
            
            # Rastgele balık tutma olayları
            if random.random() < 0.3:  # %30 ihtimalle balık tut
                fish_types = ["Küçük Balık", "Orta Balık", "Büyük Balık", "Nadir Balık"]
                caught_fish = random.choice(fish_types)
                
                self.add_fishing_log(f"🐟 {caught_fish} tutuldu!")
                
                # İstatistikleri güncelle
                current_count = int(self.caught_fish_label.cget("text"))
                self.caught_fish_label.config(text=str(current_count + 1))
                
                # Grill fish aktifse
                if self.grill_fish.get() and random.random() < 0.7:
                    self.add_fishing_log(f"🔥 {caught_fish} ızgara yapıldı")
                    current_grilled = int(self.grilled_fish_label.cget("text"))
                    self.grilled_fish_label.config(text=str(current_grilled + 1))
                    
            # Dead fish drop
            if self.drop_dead_fish.get() and random.random() < 0.1:
                self.add_fishing_log("💀 Ölü balık yere atıldı")
                current_dropped = int(self.dropped_dead_fish_label.cget("text"))
                self.dropped_dead_fish_label.config(text=str(current_dropped + 1))
                
            # Bir sonraki simülasyon
            delay = self.delay_ms.get()
            self.frame.after(delay, self.simulate_fishing)
            
    def test_fishing(self):
        """Balık testi yap"""
        import random
        
        test_events = [
            "🐟 Test balığı tutuldu!",
            "🔥 Test balığı ızgara yapıldı",
            "💀 Test ölü balık atıldı",
            "🎣 Olta yeniden atıldı",
            "⚠️ Oyuncu algılandı - balık botu duraklatıldı",
            "✅ Balık botu normale döndü"
        ]
        
        event = random.choice(test_events)
        self.add_fishing_log(event)
        
    def start_fishing_timer(self):
        """Balık botu timer'ını başlat"""
        import time
        self.fishing_start_time = time.time()
        self.update_fishing_timer()
        
    def update_fishing_timer(self):
        """Balık botu timer'ını güncelle"""
        if self.fishing_status_label.cget("text") == "Durum: Çalışıyor":
            import time
            elapsed = int(time.time() - getattr(self, 'fishing_start_time', time.time()))
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            
            self.fishing_time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # 1 saniye sonra tekrar güncelle
            self.frame.after(1000, self.update_fishing_timer)
            
    def reset_fishing_stats(self):
        """Balık botu istatistiklerini sıfırla"""
        self.caught_fish_label.config(text="0")
        self.grilled_fish_label.config(text="0")
        self.dropped_dead_fish_label.config(text="0")
        self.fishing_time_label.config(text="00:00:00")
        
        messagebox.showinfo("Sıfırlandı", "Balık botu istatistikleri sıfırlandı!")
        
    def add_fishing_log(self, message):
        """Balık botu log'una mesaj ekle"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.fishing_log.insert(tk.END, log_entry)
        self.fishing_log.see(tk.END)
        
        # Log boyutunu sınırla
        lines = self.fishing_log.get(1.0, tk.END).split('\n')
        if len(lines) > 500:
            self.fishing_log.delete(1.0, f"{len(lines) - 500}.0")
            
    def clear_fishing_log(self):
        """Balık botu kayıtlarını temizle"""
        self.fishing_log.delete(1.0, tk.END)
        
    def save_fishing_log(self):
        """Balık botu kayıtlarını dosyaya kaydet"""
        from tkinter import filedialog
        import datetime
        
        filename = filedialog.asksaveasfilename(
            title="Balık Botu Kayıtlarını Kaydet",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"GGBOT v2 - Balık Botu Kayıtları\n")
                    f.write(f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(self.fishing_log.get(1.0, tk.END))
                    
                messagebox.showinfo("Kaydedildi", "Balık botu kayıtları dosyaya kaydedildi!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya kaydedilirken hata:\n{e}")
                
    def load_settings(self):
        """Ayarları yükle"""
        self.kill_fish.set(self.settings.get("fishing.kill_fish", False))
        self.grill_fish.set(self.settings.get("fishing.grill_fish", False))
        self.drop_dead_fish.set(self.settings.get("fishing.drop_dead_fish", False))
        self.drop_hair_color.set(self.settings.get("fishing.drop_hair_color", False))
        self.dead_alarm.set(self.settings.get("fishing.dead_alarm", False))
        self.delay_ms.set(self.settings.get("fishing.delay_ms", 2650))
        
        # Alan ayarları
        self.fishing_x1.set(self.settings.get("fishing.area.x1", 100))
        self.fishing_y1.set(self.settings.get("fishing.area.y1", 100))
        self.fishing_x2.set(self.settings.get("fishing.area.x2", 500))
        self.fishing_y2.set(self.settings.get("fishing.area.y2", 400))
        
        # Tuş ayarları
        self.fishing_key.set(self.settings.get("fishing.fishing_key", "SPACE"))
        self.cast_key.set(self.settings.get("fishing.cast_key", "F"))
        
        # Gelişmiş ayarlar
        self.auto_bait.set(self.settings.get("fishing.auto_bait", False))
        self.fish_filter.set(self.settings.get("fishing.fish_filter", "all"))
        self.auto_repair.set(self.settings.get("fishing.auto_repair", False))
        self.safe_fishing.set(self.settings.get("fishing.safe_fishing", True))
        
    def save_settings(self):
        """Ayarları kaydet"""
        self.settings.set("fishing.kill_fish", self.kill_fish.get())
        self.settings.set("fishing.grill_fish", self.grill_fish.get())
        self.settings.set("fishing.drop_dead_fish", self.drop_dead_fish.get())
        self.settings.set("fishing.drop_hair_color", self.drop_hair_color.get())
        self.settings.set("fishing.dead_alarm", self.dead_alarm.get())
        self.settings.set("fishing.delay_ms", self.delay_ms.get())
        
        # Alan ayarları
        self.settings.set("fishing.area.x1", self.fishing_x1.get())
        self.settings.set("fishing.area.y1", self.fishing_y1.get())
        self.settings.set("fishing.area.x2", self.fishing_x2.get())
        self.settings.set("fishing.area.y2", self.fishing_y2.get())
        
        # Tuş ayarları
        self.settings.set("fishing.fishing_key", self.fishing_key.get())
        self.settings.set("fishing.cast_key", self.cast_key.get())
        
        # Gelişmiş ayarlar
        self.settings.set("fishing.auto_bait", self.auto_bait.get())
        self.settings.set("fishing.fish_filter", self.fish_filter.get())
        self.settings.set("fishing.auto_repair", self.auto_repair.get())
        self.settings.set("fishing.safe_fishing", self.safe_fishing.get())