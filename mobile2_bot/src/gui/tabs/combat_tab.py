#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Combat ve ESP sekmesi
"""

import tkinter as tk
from tkinter import ttk

class CombatTab:
    """Combat sekmesi"""
    
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
        
        # Target Selection grubu
        target_group = ttk.LabelFrame(scrollable_frame, text="Hedef Seçimi", padding=10)
        target_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.attack_mobs = tk.BooleanVar()
        mob_check = ttk.Checkbutton(target_group, text="Mob (Saldırı için canavarları seç)", 
                                   variable=self.attack_mobs)
        mob_check.pack(anchor=tk.W, pady=2)
        
        self.attack_stones = tk.BooleanVar()
        stone_check = ttk.Checkbutton(target_group, text="Stone (Saldırı için metinleri seç)", 
                                     variable=self.attack_stones)
        stone_check.pack(anchor=tk.W, pady=2)
        
        # Attack Groups
        groups_frame = ttk.Frame(target_group)
        groups_frame.pack(fill=tk.X, pady=5)
        
        self.attack_mob_groups = tk.BooleanVar()
        groups_check = ttk.Checkbutton(groups_frame, text="Attack mob groups (Birden fazla gruba saldır)", 
                                      variable=self.attack_mob_groups)
        groups_check.pack(anchor=tk.W)
        
        amount_frame = ttk.Frame(groups_frame)
        amount_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(amount_frame, text="Amount (Saldıracağı grup adeti):").pack(side=tk.LEFT)
        self.group_amount = tk.IntVar(value=1)
        amount_spin = ttk.Spinbox(amount_frame, from_=1, to=10, width=10, 
                                 textvariable=self.group_amount)
        amount_spin.pack(side=tk.LEFT, padx=5)
        
        # Combat Options grubu
        combat_group = ttk.LabelFrame(scrollable_frame, text="Savaş Seçenekleri", padding=10)
        combat_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.base_skills = tk.BooleanVar()
        base_skills_check = ttk.Checkbutton(combat_group, text="Base Skills (Hava Öfke gibi hasar vermeyen base itemleri otomatik yak)", 
                                           variable=self.base_skills)
        base_skills_check.pack(anchor=tk.W, pady=2)
        
        self.stop_on_no_red = tk.BooleanVar()
        stop_red_check = ttk.Checkbutton(combat_group, text="Stop bot when no red potions (Kırmızı pot bittiğinde bot durdur)", 
                                        variable=self.stop_on_no_red)
        stop_red_check.pack(anchor=tk.W, pady=2)
        
        # ESP grubu
        esp_group = ttk.LabelFrame(scrollable_frame, text="ESP (Extra Sensory Perception)", padding=10)
        esp_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.esp_players = tk.BooleanVar()
        esp_players_check = ttk.Checkbutton(esp_group, text="ESP Player (Oyuncuları göster)", 
                                           variable=self.esp_players)
        esp_players_check.pack(anchor=tk.W, pady=2)
        
        self.esp_stones = tk.BooleanVar()
        esp_stones_check = ttk.Checkbutton(esp_group, text="ESP Stone (Metinleri göster)", 
                                          variable=self.esp_stones)
        esp_stones_check.pack(anchor=tk.W, pady=2)
        
        # Combat Stats grubu
        stats_group = ttk.LabelFrame(scrollable_frame, text="Savaş İstatistikleri", padding=10)
        stats_group.pack(fill=tk.X, padx=5, pady=5)
        
        stats_frame = ttk.Frame(stats_group)
        stats_frame.pack(fill=tk.X)
        
        # Sol kolon
        left_stats = ttk.Frame(stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_stats, text="Toplam Saldırı:").pack(anchor=tk.W)
        self.total_attacks_label = ttk.Label(left_stats, text="0", font=("Arial", 12, "bold"))
        self.total_attacks_label.pack(anchor=tk.W, padx=10)
        
        ttk.Label(left_stats, text="Öldürülen Mob:").pack(anchor=tk.W, pady=(10, 0))
        self.killed_mobs_label = ttk.Label(left_stats, text="0", font=("Arial", 12, "bold"))
        self.killed_mobs_label.pack(anchor=tk.W, padx=10)
        
        # Sağ kolon
        right_stats = ttk.Frame(stats_frame)
        right_stats.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_stats, text="Kırılan Stone:").pack(anchor=tk.W)
        self.broken_stones_label = ttk.Label(right_stats, text="0", font=("Arial", 12, "bold"))
        self.broken_stones_label.pack(anchor=tk.W, padx=10)
        
        ttk.Label(right_stats, text="Kullanılan Potion:").pack(anchor=tk.W, pady=(10, 0))
        self.used_potions_label = ttk.Label(right_stats, text="0", font=("Arial", 12, "bold"))
        self.used_potions_label.pack(anchor=tk.W, padx=10)
        
        # Reset butonu
        reset_btn = ttk.Button(stats_group, text="İstatistikleri Sıfırla", 
                              command=self.reset_stats)
        reset_btn.pack(pady=10)
        
        # Combat Log
        log_group = ttk.LabelFrame(scrollable_frame, text="Savaş Kayıtları", padding=10)
        log_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Log text widget
        log_frame = ttk.Frame(log_group)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_frame, height=8, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Log kontrol butonları
        log_control_frame = ttk.Frame(log_group)
        log_control_frame.pack(fill=tk.X, pady=5)
        
        clear_log_btn = ttk.Button(log_control_frame, text="Kayıtları Temizle", 
                                  command=self.clear_log)
        clear_log_btn.pack(side=tk.LEFT)
        
        save_log_btn = ttk.Button(log_control_frame, text="Kayıtları Dosyaya Kaydet", 
                                 command=self.save_log)
        save_log_btn.pack(side=tk.LEFT, padx=5)
        
    def reset_stats(self):
        """İstatistikleri sıfırla"""
        self.total_attacks_label.config(text="0")
        self.killed_mobs_label.config(text="0")
        self.broken_stones_label.config(text="0")
        self.used_potions_label.config(text="0")
        tk.messagebox.showinfo("Sıfırlandı", "Tüm istatistikler sıfırlandı!")
        
    def clear_log(self):
        """Kayıtları temizle"""
        self.log_text.delete(1.0, tk.END)
        
    def save_log(self):
        """Kayıtları dosyaya kaydet"""
        from tkinter import filedialog
        import datetime
        
        filename = filedialog.asksaveasfilename(
            title="Savaş Kayıtlarını Kaydet",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"GGBOT v2 - Savaş Kayıtları\n")
                    f.write(f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(self.log_text.get(1.0, tk.END))
                    
                tk.messagebox.showinfo("Kaydedildi", "Savaş kayıtları dosyaya kaydedildi!")
            except Exception as e:
                tk.messagebox.showerror("Hata", f"Dosya kaydedilirken hata:\n{e}")
                
    def add_log_entry(self, message):
        """Log'a yeni giriş ekle"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)  # En sona scroll et
        
        # Log boyutunu sınırla (son 1000 satır)
        lines = self.log_text.get(1.0, tk.END).split('\n')
        if len(lines) > 1000:
            self.log_text.delete(1.0, f"{len(lines) - 1000}.0")
            
    def load_settings(self):
        """Ayarları yükle"""
        self.attack_mobs.set(self.settings.get("combat.attack_mobs", True))
        self.attack_stones.set(self.settings.get("combat.attack_stones", False))
        self.attack_mob_groups.set(self.settings.get("combat.attack_mob_groups", False))
        self.group_amount.set(self.settings.get("combat.group_amount", 1))
        self.base_skills.set(self.settings.get("combat.base_skills", False))
        self.stop_on_no_red.set(self.settings.get("combat.stop_on_no_red_potions", True))
        
        self.esp_players.set(self.settings.get("esp.players", False))
        self.esp_stones.set(self.settings.get("esp.stones", False))
        
    def save_settings(self):
        """Ayarları kaydet"""
        self.settings.set("combat.attack_mobs", self.attack_mobs.get())
        self.settings.set("combat.attack_stones", self.attack_stones.get())
        self.settings.set("combat.attack_mob_groups", self.attack_mob_groups.get())
        self.settings.set("combat.group_amount", self.group_amount.get())
        self.settings.set("combat.base_skills", self.base_skills.get())
        self.settings.set("combat.stop_on_no_red_potions", self.stop_on_no_red.get())
        
        self.settings.set("esp.players", self.esp_players.get())
        self.settings.set("esp.stones", self.esp_stones.get())