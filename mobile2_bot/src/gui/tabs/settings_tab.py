#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings ve Spam Bot sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class SettingsTab:
    """Settings sekmesi"""
    
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
        
        # Spam Bot grubu
        spam_group = ttk.LabelFrame(scrollable_frame, text="Spam Bot", padding=10)
        spam_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Spam bot durumu
        self.spam_status_label = ttk.Label(spam_group, text="Durum: Durduruldu", 
                                          font=("Arial", 10, "bold"))
        self.spam_status_label.pack(pady=5)
        
        # Text girişi
        text_frame = ttk.Frame(spam_group)
        text_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(text_frame, text="Text (Otomatik yazılacak metin):").pack(anchor=tk.W)
        self.spam_text = tk.StringVar()
        text_entry = ttk.Entry(text_frame, textvariable=self.spam_text, width=50)
        text_entry.pack(fill=tk.X, pady=2)
        
        # Süre ayarı
        seconds_frame = ttk.Frame(spam_group)
        seconds_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(seconds_frame, text="Seconds (Yazılacak mesajın süresini belirle):").pack(side=tk.LEFT)
        self.spam_seconds = tk.IntVar(value=5)
        seconds_spin = ttk.Spinbox(seconds_frame, from_=1, to=300, width=10, 
                                  textvariable=self.spam_seconds)
        seconds_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(seconds_frame, text="saniye").pack(side=tk.LEFT)
        
        # Spam bot kontrolleri
        spam_control_frame = ttk.Frame(spam_group)
        spam_control_frame.pack(fill=tk.X, pady=5)
        
        self.start_spam_btn = ttk.Button(spam_control_frame, text="Start Spambot", 
                                        command=self.start_spam_bot)
        self.start_spam_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_spam_btn = ttk.Button(spam_control_frame, text="Stop Spambot", 
                                       command=self.stop_spam_bot, state=tk.DISABLED)
        self.stop_spam_btn.pack(side=tk.LEFT, padx=2)
        
        # Spam ayarları
        spam_settings_frame = ttk.Frame(spam_group)
        spam_settings_frame.pack(fill=tk.X, pady=5)
        
        self.spam_random_delay = tk.BooleanVar()
        ttk.Checkbutton(spam_settings_frame, text="Rastgele Gecikme (Algılanmayı zorlaştırır)", 
                       variable=self.spam_random_delay).pack(anchor=tk.W)
        
        self.spam_auto_stop = tk.BooleanVar()
        ttk.Checkbutton(spam_settings_frame, text="Oyuncu Geldiğinde Durdur", 
                       variable=self.spam_auto_stop).pack(anchor=tk.W)
        
        # Spam mesaj şablonları
        templates_frame = ttk.Frame(spam_group)
        templates_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(templates_frame, text="Mesaj Şablonları:").pack(anchor=tk.W)
        
        template_buttons_frame = ttk.Frame(templates_frame)
        template_buttons_frame.pack(fill=tk.X, pady=2)
        
        templates = [
            "Selam herkese!",
            "Trade var mı?",
            "Guild arıyorum",
            "Yardım lazım",
            "İyi oyunlar!"
        ]
        
        for template in templates:
            btn = ttk.Button(template_buttons_frame, text=template, width=15,
                           command=lambda t=template: self.spam_text.set(t))
            btn.pack(side=tk.LEFT, padx=2, pady=1)
            
        # Genel Ayarlar grubu
        general_group = ttk.LabelFrame(scrollable_frame, text="Genel Ayarlar", padding=10)
        general_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Dil ayarları
        language_frame = ttk.Frame(general_group)
        language_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(language_frame, text="Dil / Language:").pack(side=tk.LEFT)
        self.language = tk.StringVar(value="tr")
        language_combo = ttk.Combobox(language_frame, textvariable=self.language, 
                                     values=["tr", "en"], state="readonly", width=10)
        language_combo.pack(side=tk.LEFT, padx=5)
        
        # Tema ayarları
        theme_frame = ttk.Frame(general_group)
        theme_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(theme_frame, text="Tema / Theme:").pack(side=tk.LEFT)
        self.theme = tk.StringVar(value="default")
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme, 
                                  values=["default", "dark", "light"], state="readonly", width=10)
        theme_combo.pack(side=tk.LEFT, padx=5)
        
        # Başlangıç ayarları
        startup_frame = ttk.Frame(general_group)
        startup_frame.pack(fill=tk.X, pady=5)
        
        self.auto_start_bot = tk.BooleanVar()
        ttk.Checkbutton(startup_frame, text="Programla birlikte bot'u başlat", 
                       variable=self.auto_start_bot).pack(anchor=tk.W)
        
        self.minimize_to_tray = tk.BooleanVar()
        ttk.Checkbutton(startup_frame, text="System tray'e minimize et", 
                       variable=self.minimize_to_tray).pack(anchor=tk.W)
        
        self.save_logs = tk.BooleanVar(value=True)
        ttk.Checkbutton(startup_frame, text="Logları otomatik kaydet", 
                       variable=self.save_logs).pack(anchor=tk.W)
        
        # Güvenlik Ayarları grubu
        security_group = ttk.LabelFrame(scrollable_frame, text="Güvenlik Ayarları", padding=10)
        security_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Güvenlik seçenekleri
        security_frame = ttk.Frame(security_group)
        security_frame.pack(fill=tk.X, pady=5)
        
        self.anti_detection = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Anti-Detection (Algılanma karşıtı özellikler)", 
                       variable=self.anti_detection).pack(anchor=tk.W)
        
        self.randomize_timings = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="Zamanlamaları Rastgeleleştir", 
                       variable=self.randomize_timings).pack(anchor=tk.W)
        
        self.human_like_movement = tk.BooleanVar(value=True)
        ttk.Checkbutton(security_frame, text="İnsan Benzeri Hareket", 
                       variable=self.human_like_movement).pack(anchor=tk.W)
        
        # Güvenlik seviyeleri
        security_level_frame = ttk.Frame(security_group)
        security_level_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(security_level_frame, text="Güvenlik Seviyesi:").pack(side=tk.LEFT)
        self.security_level = tk.StringVar(value="medium")
        security_combo = ttk.Combobox(security_level_frame, textvariable=self.security_level, 
                                     values=["low", "medium", "high", "paranoid"], 
                                     state="readonly", width=15)
        security_combo.pack(side=tk.LEFT, padx=5)
        
        # Performans Ayarları grubu
        performance_group = ttk.LabelFrame(scrollable_frame, text="Performans Ayarları", padding=10)
        performance_group.pack(fill=tk.X, padx=5, pady=5)
        
        # CPU kullanımı
        cpu_frame = ttk.Frame(performance_group)
        cpu_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cpu_frame, text="CPU Kullanım Limiti:").pack(side=tk.LEFT)
        self.cpu_limit = tk.IntVar(value=50)
        cpu_spin = ttk.Spinbox(cpu_frame, from_=10, to=100, width=10, 
                              textvariable=self.cpu_limit)
        cpu_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(cpu_frame, text="%").pack(side=tk.LEFT)
        
        # Güncelleme sıklığı
        update_frame = ttk.Frame(performance_group)
        update_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(update_frame, text="Güncelleme Sıklığı:").pack(side=tk.LEFT)
        self.update_frequency = tk.IntVar(value=100)
        update_spin = ttk.Spinbox(update_frame, from_=50, to=1000, width=10, 
                                 textvariable=self.update_frequency)
        update_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(update_frame, text="ms").pack(side=tk.LEFT)
        
        # Bellek yönetimi
        memory_frame = ttk.Frame(performance_group)
        memory_frame.pack(fill=tk.X, pady=5)
        
        self.auto_cleanup = tk.BooleanVar(value=True)
        ttk.Checkbutton(memory_frame, text="Otomatik Bellek Temizleme", 
                       variable=self.auto_cleanup).pack(anchor=tk.W)
        
        # Dosya İşlemleri grubu
        file_group = ttk.LabelFrame(scrollable_frame, text="Dosya İşlemleri", padding=10)
        file_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Ayar dosyası işlemleri
        file_buttons_frame = ttk.Frame(file_group)
        file_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(file_buttons_frame, text="Ayarları Dışa Aktar", 
                  command=self.export_settings).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons_frame, text="Ayarları İçe Aktar", 
                  command=self.import_settings).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_buttons_frame, text="Varsayılan Ayarlar", 
                  command=self.reset_to_defaults).pack(side=tk.LEFT, padx=2)
        
        # Backup ayarları
        backup_frame = ttk.Frame(file_group)
        backup_frame.pack(fill=tk.X, pady=5)
        
        self.auto_backup = tk.BooleanVar(value=True)
        ttk.Checkbutton(backup_frame, text="Otomatik Yedekleme", 
                       variable=self.auto_backup).pack(anchor=tk.W)
        
        backup_interval_frame = ttk.Frame(backup_frame)
        backup_interval_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(backup_interval_frame, text="Yedekleme Aralığı:").pack(side=tk.LEFT)
        self.backup_interval = tk.IntVar(value=24)
        backup_spin = ttk.Spinbox(backup_interval_frame, from_=1, to=168, width=10, 
                                 textvariable=self.backup_interval)
        backup_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(backup_interval_frame, text="saat").pack(side=tk.LEFT)
        
        # Hakkında grubu
        about_group = ttk.LabelFrame(scrollable_frame, text="Hakkında", padding=10)
        about_group.pack(fill=tk.X, padx=5, pady=5)
        
        about_text = """GGBOT v2 - Mobile2 Global Bot
        
Öğretmen ödevi için geliştirilmiştir.

Özellikler:
• Otomatik potion kullanımı
• Savaş sistemi ve ESP
• Hareket hack'leri
• Item toplama sistemi
• Oyuncu algılama
• Otomatik rota sistemi
• Balık botu
• Spam bot

Geliştirici: Öğrenci
Tarih: 2025
Versiyon: 2.0"""
        
        about_label = ttk.Label(about_group, text=about_text, justify=tk.LEFT)
        about_label.pack(pady=5)
        
        # Sistem bilgileri
        system_info_btn = ttk.Button(about_group, text="Sistem Bilgileri", 
                                    command=self.show_system_info)
        system_info_btn.pack(pady=5)
        
    def start_spam_bot(self):
        """Spam bot'u başlat"""
        text = self.spam_text.get().strip()
        if not text:
            messagebox.showwarning("Uyarı", "Spam metni boş olamaz!")
            return
            
        try:
            self.settings.set("spam_bot.enabled", True)
            self.settings.set("spam_bot.text", text)
            self.settings.set("spam_bot.seconds", self.spam_seconds.get())
            
            self.spam_status_label.config(text="Durum: Çalışıyor", foreground="green")
            self.start_spam_btn.config(state=tk.DISABLED)
            self.stop_spam_btn.config(state=tk.NORMAL)
            
            # Spam işlemini başlat
            self.spam_thread = threading.Thread(target=self.spam_worker, daemon=True)
            self.spam_thread.start()
            
            print(f"Spam bot başlatıldı: '{text}' - {self.spam_seconds.get()} saniye aralıkla")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Spam bot başlatılırken hata:\n{e}")
            
    def stop_spam_bot(self):
        """Spam bot'u durdur"""
        try:
            self.settings.set("spam_bot.enabled", False)
            
            self.spam_status_label.config(text="Durum: Durduruldu", foreground="black")
            self.start_spam_btn.config(state=tk.NORMAL)
            self.stop_spam_btn.config(state=tk.DISABLED)
            
            print("Spam bot durduruldu")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Spam bot durdurulurken hata:\n{e}")
            
    def spam_worker(self):
        """Spam bot worker thread'i"""
        import time
        import random
        
        while self.settings.get("spam_bot.enabled", False):
            try:
                text = self.settings.get("spam_bot.text", "")
                interval = self.settings.get("spam_bot.seconds", 5)
                
                if text:
                    # Mesajı gönder (simülasyon)
                    print(f"Spam mesajı gönderildi: {text}")
                    
                    # Rastgele gecikme
                    if self.spam_random_delay.get():
                        delay_variation = random.uniform(0.5, 1.5)
                        time.sleep(interval * delay_variation)
                    else:
                        time.sleep(interval)
                else:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Spam worker hatası: {e}")
                time.sleep(1)
                
    def export_settings(self):
        """Ayarları dışa aktar"""
        filename = filedialog.asksaveasfilename(
            title="Ayarları Dışa Aktar",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import json
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.settings.settings, f, indent=4, ensure_ascii=False)
                    
                messagebox.showinfo("Başarılı", "Ayarlar başarıyla dışa aktarıldı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Ayarlar dışa aktarılırken hata:\n{e}")
                
    def import_settings(self):
        """Ayarları içe aktar"""
        filename = filedialog.askopenfilename(
            title="Ayarları İçe Aktar",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                import json
                with open(filename, 'r', encoding='utf-8') as f:
                    imported_settings = json.load(f)
                    
                result = messagebox.askyesno("Onay", "Mevcut ayarların üzerine yazmak istiyor musunuz?")
                if result:
                    self.settings.settings.update(imported_settings)
                    self.load_settings()  # UI'yi güncelle
                    messagebox.showinfo("Başarılı", "Ayarlar başarıyla içe aktarıldı!")
                    
            except Exception as e:
                messagebox.showerror("Hata", f"Ayarlar içe aktarılırken hata:\n{e}")
                
    def reset_to_defaults(self):
        """Varsayılan ayarlara dön"""
        result = messagebox.askyesno("Onay", "Tüm ayarları varsayılan değerlere döndürmek istiyor musunuz?")
        
        if result:
            try:
                self.settings.settings = self.settings.default_settings.copy()
                self.load_settings()
                messagebox.showinfo("Başarılı", "Ayarlar varsayılan değerlere döndürüldü!")
            except Exception as e:
                messagebox.showerror("Hata", f"Varsayılan ayarlara dönerken hata:\n{e}")
                
    def show_system_info(self):
        """Sistem bilgilerini göster"""
        try:
            import platform
            import psutil
            import sys
            
            info = f"""Sistem Bilgileri:

İşletim Sistemi: {platform.system()} {platform.release()}
Python Versiyonu: {sys.version.split()[0]}
CPU Çekirdek Sayısı: {psutil.cpu_count()}
Toplam RAM: {psutil.virtual_memory().total // (1024**3)} GB
Kullanılabilir RAM: {psutil.virtual_memory().available // (1024**3)} GB
CPU Kullanımı: {psutil.cpu_percent()}%

Bot Bilgileri:
Versiyon: 2.0
Çalışma Süresi: {self.get_uptime()}
"""
            
            messagebox.showinfo("Sistem Bilgileri", info)
            
        except Exception as e:
            messagebox.showerror("Hata", f"Sistem bilgileri alınırken hata:\n{e}")
            
    def get_uptime(self):
        """Bot çalışma süresini al"""
        # Bu fonksiyon gerçek implementasyonda bot başlangıç zamanını takip edecek
        return "Henüz hesaplanmadı"
        
    def load_settings(self):
        """Ayarları yükle"""
        # Spam bot
        self.spam_text.set(self.settings.get("spam_bot.text", ""))
        self.spam_seconds.set(self.settings.get("spam_bot.seconds", 5))
        self.spam_random_delay.set(self.settings.get("spam_bot.random_delay", False))
        self.spam_auto_stop.set(self.settings.get("spam_bot.auto_stop", False))
        
        # Genel ayarlar
        self.language.set(self.settings.get("general.language", "tr"))
        self.theme.set(self.settings.get("general.theme", "default"))
        self.auto_start_bot.set(self.settings.get("general.auto_start_bot", False))
        self.minimize_to_tray.set(self.settings.get("general.minimize_to_tray", False))
        self.save_logs.set(self.settings.get("general.save_logs", True))
        
        # Güvenlik ayarları
        self.anti_detection.set(self.settings.get("security.anti_detection", True))
        self.randomize_timings.set(self.settings.get("security.randomize_timings", True))
        self.human_like_movement.set(self.settings.get("security.human_like_movement", True))
        self.security_level.set(self.settings.get("security.level", "medium"))
        
        # Performans ayarları
        self.cpu_limit.set(self.settings.get("performance.cpu_limit", 50))
        self.update_frequency.set(self.settings.get("performance.update_frequency", 100))
        self.auto_cleanup.set(self.settings.get("performance.auto_cleanup", True))
        
        # Backup ayarları
        self.auto_backup.set(self.settings.get("backup.auto_backup", True))
        self.backup_interval.set(self.settings.get("backup.interval", 24))
        
    def save_settings(self):
        """Ayarları kaydet"""
        # Spam bot
        self.settings.set("spam_bot.text", self.spam_text.get())
        self.settings.set("spam_bot.seconds", self.spam_seconds.get())
        self.settings.set("spam_bot.random_delay", self.spam_random_delay.get())
        self.settings.set("spam_bot.auto_stop", self.spam_auto_stop.get())
        
        # Genel ayarlar
        self.settings.set("general.language", self.language.get())
        self.settings.set("general.theme", self.theme.get())
        self.settings.set("general.auto_start_bot", self.auto_start_bot.get())
        self.settings.set("general.minimize_to_tray", self.minimize_to_tray.get())
        self.settings.set("general.save_logs", self.save_logs.get())
        
        # Güvenlik ayarları
        self.settings.set("security.anti_detection", self.anti_detection.get())
        self.settings.set("security.randomize_timings", self.randomize_timings.get())
        self.settings.set("security.human_like_movement", self.human_like_movement.get())
        self.settings.set("security.level", self.security_level.get())
        
        # Performans ayarları
        self.settings.set("performance.cpu_limit", self.cpu_limit.get())
        self.settings.set("performance.update_frequency", self.update_frequency.get())
        self.settings.set("performance.auto_cleanup", self.auto_cleanup.get())
        
        # Backup ayarları
        self.settings.set("backup.auto_backup", self.auto_backup.get())
        self.settings.set("backup.interval", self.backup_interval.get())