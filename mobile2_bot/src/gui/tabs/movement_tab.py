#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Movement ve Speed hack sekmesi
"""

import tkinter as tk
from tkinter import ttk

class MovementTab:
    """Movement sekmesi"""
    
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
        
        # Wait Hack grubu
        wait_hack_group = ttk.LabelFrame(scrollable_frame, text="Wait Hack (Yakın Mesafe)", padding=10)
        wait_hack_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.wait_hack_enabled = tk.BooleanVar()
        wait_hack_check = ttk.Checkbutton(wait_hack_group, text="Wait Hack Aktif (Yakın mesafede animasyon olmadan saldırı)", 
                                         variable=self.wait_hack_enabled)
        wait_hack_check.pack(anchor=tk.W, pady=2)
        
        wait_hack_frame = ttk.Frame(wait_hack_group)
        wait_hack_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(wait_hack_frame, text="Amount (Hız değeri):").pack(side=tk.LEFT)
        self.wait_hack_amount = tk.IntVar(value=1000)
        wait_hack_spin = ttk.Spinbox(wait_hack_frame, from_=100, to=5000, width=10, 
                                    textvariable=self.wait_hack_amount)
        wait_hack_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(wait_hack_frame, text="ms").pack(side=tk.LEFT)
        
        # Wait Hack Range grubu
        wait_hack_range_group = ttk.LabelFrame(scrollable_frame, text="Wait Hack Range (Uzak Mesafe)", padding=10)
        wait_hack_range_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.wait_hack_range_enabled = tk.BooleanVar()
        wait_hack_range_check = ttk.Checkbutton(wait_hack_range_group, text="Wait Hack Range Aktif (Uzak mesafede animasyon olmadan saldırı)", 
                                               variable=self.wait_hack_range_enabled)
        wait_hack_range_check.pack(anchor=tk.W, pady=2)
        
        wait_hack_range_frame = ttk.Frame(wait_hack_range_group)
        wait_hack_range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(wait_hack_range_frame, text="Amount (Hız değeri):").pack(side=tk.LEFT)
        self.wait_hack_range_amount = tk.IntVar(value=1000)
        wait_hack_range_spin = ttk.Spinbox(wait_hack_range_frame, from_=100, to=5000, width=10, 
                                          textvariable=self.wait_hack_range_amount)
        wait_hack_range_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(wait_hack_range_frame, text="ms").pack(side=tk.LEFT)
        
        # Movement Speed grubu
        movement_speed_group = ttk.LabelFrame(scrollable_frame, text="Movement Speed", padding=10)
        movement_speed_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.movement_speed_enabled = tk.BooleanVar()
        movement_speed_check = ttk.Checkbutton(movement_speed_group, text="Movement Speed Aktif (Hareket hızını değiştir)", 
                                              variable=self.movement_speed_enabled)
        movement_speed_check.pack(anchor=tk.W, pady=2)
        
        movement_speed_frame = ttk.Frame(movement_speed_group)
        movement_speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(movement_speed_frame, text="Amount (Hız değeri):").pack(side=tk.LEFT)
        self.movement_speed_amount = tk.IntVar(value=100)
        movement_speed_spin = ttk.Spinbox(movement_speed_frame, from_=50, to=500, width=10, 
                                         textvariable=self.movement_speed_amount)
        movement_speed_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(movement_speed_frame, text="%").pack(side=tk.LEFT)
        
        # Uyarı mesajı
        warning_frame = ttk.Frame(movement_speed_group)
        warning_frame.pack(fill=tk.X, pady=10)
        
        warning_label = ttk.Label(warning_frame, 
                                 text="⚠️ UYARI: Yüksek hız değerleri oyundan atılmanıza neden olabilir!", 
                                 foreground="red", font=("Arial", 9, "bold"))
        warning_label.pack()
        
        # Speed Hack Presets
        presets_group = ttk.LabelFrame(scrollable_frame, text="Hız Ön Ayarları", padding=10)
        presets_group.pack(fill=tk.X, padx=5, pady=5)
        
        presets_frame = ttk.Frame(presets_group)
        presets_frame.pack(fill=tk.X)
        
        # Preset butonları
        preset_buttons_frame = ttk.Frame(presets_frame)
        preset_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(preset_buttons_frame, text="Güvenli (100%)", 
                  command=lambda: self.apply_preset(100, 1000, 1000)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_buttons_frame, text="Orta (150%)", 
                  command=lambda: self.apply_preset(150, 800, 800)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_buttons_frame, text="Hızlı (200%)", 
                  command=lambda: self.apply_preset(200, 600, 600)).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_buttons_frame, text="Çok Hızlı (300%)", 
                  command=lambda: self.apply_preset(300, 400, 400)).pack(side=tk.LEFT, padx=2)
        
        # Test butonları
        test_group = ttk.LabelFrame(scrollable_frame, text="Hız Testi", padding=10)
        test_group.pack(fill=tk.X, padx=5, pady=5)
        
        test_frame = ttk.Frame(test_group)
        test_frame.pack(fill=tk.X)
        
        ttk.Button(test_frame, text="Hız Testini Başlat", 
                  command=self.start_speed_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(test_frame, text="Hız Testini Durdur", 
                  command=self.stop_speed_test).pack(side=tk.LEFT, padx=5)
        
        # Test sonuçları
        self.test_result_label = ttk.Label(test_group, text="Test sonucu: Henüz test yapılmadı")
        self.test_result_label.pack(pady=5)
        
        # Gelişmiş ayarlar
        advanced_group = ttk.LabelFrame(scrollable_frame, text="Gelişmiş Ayarlar", padding=10)
        advanced_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Auto-adjust speed
        self.auto_adjust_enabled = tk.BooleanVar()
        auto_adjust_check = ttk.Checkbutton(advanced_group, text="Otomatik Hız Ayarı (Oyuncu algılandığında hızı düşür)", 
                                           variable=self.auto_adjust_enabled)
        auto_adjust_check.pack(anchor=tk.W, pady=2)
        
        # Speed randomization
        self.speed_randomization_enabled = tk.BooleanVar()
        randomization_check = ttk.Checkbutton(advanced_group, text="Hız Rastgeleleştirme (Algılanmayı zorlaştırır)", 
                                             variable=self.speed_randomization_enabled)
        randomization_check.pack(anchor=tk.W, pady=2)
        
        randomization_frame = ttk.Frame(advanced_group)
        randomization_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(randomization_frame, text="Rastgelelik Oranı:").pack(side=tk.LEFT)
        self.randomization_factor = tk.IntVar(value=10)
        randomization_spin = ttk.Spinbox(randomization_frame, from_=5, to=50, width=10, 
                                        textvariable=self.randomization_factor)
        randomization_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(randomization_frame, text="%").pack(side=tk.LEFT)
        
        # Movement pattern
        pattern_frame = ttk.Frame(advanced_group)
        pattern_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(pattern_frame, text="Hareket Deseni:").pack(side=tk.LEFT)
        self.movement_pattern = tk.StringVar(value="normal")
        pattern_combo = ttk.Combobox(pattern_frame, textvariable=self.movement_pattern, 
                                    values=["normal", "zigzag", "circular", "random"], 
                                    state="readonly", width=15)
        pattern_combo.pack(side=tk.LEFT, padx=5)
        
    def apply_preset(self, movement_speed, wait_hack, wait_hack_range):
        """Hız ön ayarını uygula"""
        self.movement_speed_amount.set(movement_speed)
        self.wait_hack_amount.set(wait_hack)
        self.wait_hack_range_amount.set(wait_hack_range)
        
        # Tüm hack'leri aktif et
        self.movement_speed_enabled.set(True)
        self.wait_hack_enabled.set(True)
        self.wait_hack_range_enabled.set(True)
        
        tk.messagebox.showinfo("Preset Uygulandı", 
                              f"Hız preset'i uygulandı:\n"
                              f"Movement Speed: {movement_speed}%\n"
                              f"Wait Hack: {wait_hack}ms\n"
                              f"Wait Hack Range: {wait_hack_range}ms")
        
    def start_speed_test(self):
        """Hız testini başlat"""
        # Bu fonksiyon gerçek implementasyonda oyun içinde hız testi yapacak
        import threading
        import time
        
        def test_thread():
            self.test_result_label.config(text="Test sonucu: Test çalışıyor...")
            
            # Simüle edilmiş test
            time.sleep(3)
            
            # Rastgele test sonucu
            import random
            fps = random.randint(45, 120)
            ping = random.randint(20, 100)
            
            result_text = f"Test sonucu: FPS: {fps}, Ping: {ping}ms, Durum: {'İyi' if fps > 60 else 'Orta'}"
            self.test_result_label.config(text=result_text)
            
        threading.Thread(target=test_thread, daemon=True).start()
        
    def stop_speed_test(self):
        """Hız testini durdur"""
        self.test_result_label.config(text="Test sonucu: Test durduruldu")
        
    def load_settings(self):
        """Ayarları yükle"""
        self.wait_hack_enabled.set(self.settings.get("speed_hacks.wait_hack.enabled", False))
        self.wait_hack_amount.set(self.settings.get("speed_hacks.wait_hack.amount", 1000))
        
        self.wait_hack_range_enabled.set(self.settings.get("speed_hacks.wait_hack_range.enabled", False))
        self.wait_hack_range_amount.set(self.settings.get("speed_hacks.wait_hack_range.amount", 1000))
        
        self.movement_speed_enabled.set(self.settings.get("speed_hacks.movement_speed.enabled", False))
        self.movement_speed_amount.set(self.settings.get("speed_hacks.movement_speed.amount", 100))
        
        # Gelişmiş ayarlar
        self.auto_adjust_enabled.set(self.settings.get("speed_hacks.auto_adjust", False))
        self.speed_randomization_enabled.set(self.settings.get("speed_hacks.randomization.enabled", False))
        self.randomization_factor.set(self.settings.get("speed_hacks.randomization.factor", 10))
        self.movement_pattern.set(self.settings.get("speed_hacks.movement_pattern", "normal"))
        
    def save_settings(self):
        """Ayarları kaydet"""
        self.settings.set("speed_hacks.wait_hack.enabled", self.wait_hack_enabled.get())
        self.settings.set("speed_hacks.wait_hack.amount", self.wait_hack_amount.get())
        
        self.settings.set("speed_hacks.wait_hack_range.enabled", self.wait_hack_range_enabled.get())
        self.settings.set("speed_hacks.wait_hack_range.amount", self.wait_hack_range_amount.get())
        
        self.settings.set("speed_hacks.movement_speed.enabled", self.movement_speed_enabled.get())
        self.settings.set("speed_hacks.movement_speed.amount", self.movement_speed_amount.get())
        
        # Gelişmiş ayarlar
        self.settings.set("speed_hacks.auto_adjust", self.auto_adjust_enabled.get())
        self.settings.set("speed_hacks.randomization.enabled", self.speed_randomization_enabled.get())
        self.settings.set("speed_hacks.randomization.factor", self.randomization_factor.get())
        self.settings.set("speed_hacks.movement_pattern", self.movement_pattern.get())