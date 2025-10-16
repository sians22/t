#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Player Detection sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox

class PlayerTab:
    """Player Detection sekmesi"""
    
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
        
        # Whitelist grubu
        whitelist_group = ttk.LabelFrame(scrollable_frame, text="Whitelist Yönetimi", padding=10)
        whitelist_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Player arama ve ekleme
        search_frame = ttk.Frame(whitelist_group)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Player Name:").pack(side=tk.LEFT)
        self.player_search_var = tk.StringVar()
        self.player_search_entry = ttk.Entry(search_frame, textvariable=self.player_search_var, width=20)
        self.player_search_entry.pack(side=tk.LEFT, padx=5)
        
        add_whitelist_btn = ttk.Button(search_frame, text="Add to whitelist", 
                                      command=self.add_to_whitelist)
        add_whitelist_btn.pack(side=tk.LEFT, padx=5)
        
        # Manuel oyuncu ekleme
        manual_frame = ttk.Frame(whitelist_group)
        manual_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(manual_frame, text="Add Player Manually:").pack(side=tk.LEFT)
        self.manual_player_var = tk.StringVar()
        manual_entry = ttk.Entry(manual_frame, textvariable=self.manual_player_var, width=20)
        manual_entry.pack(side=tk.LEFT, padx=5)
        
        add_manual_btn = ttk.Button(manual_frame, text="Manuel Ekle", 
                                   command=self.add_manual_player)
        add_manual_btn.pack(side=tk.LEFT, padx=5)
        
        # Whitelist listesi
        list_frame = ttk.Frame(whitelist_group)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(list_frame, text="Whitelist:").pack(anchor=tk.W)
        
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.whitelist_listbox = tk.Listbox(listbox_frame, height=8)
        whitelist_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.whitelist_listbox.yview)
        self.whitelist_listbox.configure(yscrollcommand=whitelist_scrollbar.set)
        
        self.whitelist_listbox.pack(side="left", fill="both", expand=True)
        whitelist_scrollbar.pack(side="right", fill="y")
        
        # Whitelist kontrol butonları
        whitelist_control_frame = ttk.Frame(whitelist_group)
        whitelist_control_frame.pack(fill=tk.X, pady=5)
        
        delete_whitelist_btn = ttk.Button(whitelist_control_frame, text="Delete from whitelist", 
                                         command=self.delete_from_whitelist)
        delete_whitelist_btn.pack(side=tk.LEFT, padx=2)
        
        clear_whitelist_btn = ttk.Button(whitelist_control_frame, text="Clear Whitelist", 
                                        command=self.clear_whitelist)
        clear_whitelist_btn.pack(side=tk.LEFT, padx=2)
        
        # Range ayarları
        range_group = ttk.LabelFrame(scrollable_frame, text="Alan Ayarları", padding=10)
        range_group.pack(fill=tk.X, padx=5, pady=5)
        
        range_frame = ttk.Frame(range_group)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(range_frame, text="Player Range (Alan belirleme):").pack(side=tk.LEFT)
        self.player_range = tk.IntVar(value=100)
        range_spin = ttk.Spinbox(range_frame, from_=50, to=500, width=10, 
                                textvariable=self.player_range)
        range_spin.pack(side=tk.LEFT, padx=5)
        
        self.range_enabled = tk.BooleanVar()
        range_check = ttk.Checkbutton(range_group, text="Activate Range (Belirlediğiniz alanı aktif et)", 
                                     variable=self.range_enabled)
        range_check.pack(anchor=tk.W, pady=2)
        
        # Player Detection Reactions
        player_reactions_group = ttk.LabelFrame(scrollable_frame, text="If Player (Oyuncu Algılandığında)", padding=10)
        player_reactions_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.player_stop_wait_range = tk.BooleanVar()
        ttk.Checkbutton(player_reactions_group, text="Stop Wait+Range (waithack+range deaktif olur)", 
                       variable=self.player_stop_wait_range).pack(anchor=tk.W, pady=1)
        
        self.player_stop_speedhacks = tk.BooleanVar()
        ttk.Checkbutton(player_reactions_group, text="Stop Speedhacks (hareket hızı deaktif olur)", 
                       variable=self.player_stop_speedhacks).pack(anchor=tk.W, pady=1)
        
        self.player_stop_bot = tk.BooleanVar()
        ttk.Checkbutton(player_reactions_group, text="Stop Bot (bot durur)", 
                       variable=self.player_stop_bot).pack(anchor=tk.W, pady=1)
        
        self.player_quit_game = tk.BooleanVar()
        ttk.Checkbutton(player_reactions_group, text="Quit (oyun kapanır)", 
                       variable=self.player_quit_game).pack(anchor=tk.W, pady=1)
        
        self.player_sound_alarm = tk.BooleanVar()
        ttk.Checkbutton(player_reactions_group, text="Sound Alarm (alarm öter)", 
                       variable=self.player_sound_alarm).pack(anchor=tk.W, pady=1)
        
        # GM Detection Reactions
        gm_reactions_group = ttk.LabelFrame(scrollable_frame, text="If GM (GM Algılandığında)", padding=10)
        gm_reactions_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.gm_stop_wait_range = tk.BooleanVar()
        ttk.Checkbutton(gm_reactions_group, text="Stop Wait+Range (waithack+range deaktif olur)", 
                       variable=self.gm_stop_wait_range).pack(anchor=tk.W, pady=1)
        
        self.gm_stop_speedhacks = tk.BooleanVar()
        ttk.Checkbutton(gm_reactions_group, text="Stop Speedhacks (hareket hızı deaktif olur)", 
                       variable=self.gm_stop_speedhacks).pack(anchor=tk.W, pady=1)
        
        self.gm_stop_bot = tk.BooleanVar()
        ttk.Checkbutton(gm_reactions_group, text="Stop Bot (bot durur)", 
                       variable=self.gm_stop_bot).pack(anchor=tk.W, pady=1)
        
        self.gm_quit_game = tk.BooleanVar()
        ttk.Checkbutton(gm_reactions_group, text="Quit (oyun kapanır)", 
                       variable=self.gm_quit_game).pack(anchor=tk.W, pady=1)
        
        self.gm_sound_alarm = tk.BooleanVar()
        ttk.Checkbutton(gm_reactions_group, text="Sound Alarm (alarm öter)", 
                       variable=self.gm_sound_alarm).pack(anchor=tk.W, pady=1)
        
        # Detection Log
        log_group = ttk.LabelFrame(scrollable_frame, text="Algılama Kayıtları", padding=10)
        log_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        log_frame = ttk.Frame(log_group)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.detection_log = tk.Text(log_frame, height=8, wrap=tk.WORD)
        log_scrollbar_det = ttk.Scrollbar(log_frame, orient="vertical", command=self.detection_log.yview)
        self.detection_log.configure(yscrollcommand=log_scrollbar_det.set)
        
        self.detection_log.pack(side="left", fill="both", expand=True)
        log_scrollbar_det.pack(side="right", fill="y")
        
        # Log kontrol butonları
        log_control_frame = ttk.Frame(log_group)
        log_control_frame.pack(fill=tk.X, pady=5)
        
        clear_log_btn = ttk.Button(log_control_frame, text="Kayıtları Temizle", 
                                  command=self.clear_detection_log)
        clear_log_btn.pack(side=tk.LEFT)
        
        # Test butonu
        test_btn = ttk.Button(log_control_frame, text="Algılama Testi", 
                             command=self.test_detection)
        test_btn.pack(side=tk.LEFT, padx=5)
        
        # İstatistikler
        stats_group = ttk.LabelFrame(scrollable_frame, text="Algılama İstatistikleri", padding=10)
        stats_group.pack(fill=tk.X, padx=5, pady=5)
        
        stats_frame = ttk.Frame(stats_group)
        stats_frame.pack(fill=tk.X)
        
        # Sol kolon
        left_stats = ttk.Frame(stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_stats, text="Algılanan Oyuncu:").pack(anchor=tk.W)
        self.detected_players_label = ttk.Label(left_stats, text="0", font=("Arial", 12, "bold"))
        self.detected_players_label.pack(anchor=tk.W, padx=10)
        
        # Sağ kolon
        right_stats = ttk.Frame(stats_frame)
        right_stats.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_stats, text="Algılanan GM:").pack(anchor=tk.W)
        self.detected_gms_label = ttk.Label(right_stats, text="0", font=("Arial", 12, "bold"))
        self.detected_gms_label.pack(anchor=tk.W, padx=10)
        
        # Reset stats butonu
        reset_stats_btn = ttk.Button(stats_group, text="İstatistikleri Sıfırla", 
                                    command=self.reset_detection_stats)
        reset_stats_btn.pack(pady=5)
        
    def add_to_whitelist(self):
        """Oyuncuyu whitelist'e ekle"""
        player_name = self.player_search_var.get().strip()
        if player_name:
            self.add_player_to_whitelist(player_name)
            self.player_search_var.set("")
        else:
            messagebox.showwarning("Uyarı", "Oyuncu adı boş olamaz!")
            
    def add_manual_player(self):
        """Manuel oyuncu ekle"""
        player_name = self.manual_player_var.get().strip()
        if player_name:
            self.add_player_to_whitelist(player_name)
            self.manual_player_var.set("")
        else:
            messagebox.showwarning("Uyarı", "Oyuncu adı boş olamaz!")
            
    def add_player_to_whitelist(self, player_name):
        """Oyuncuyu whitelist'e ekle"""
        current_players = list(self.whitelist_listbox.get(0, tk.END))
        if player_name not in current_players:
            self.whitelist_listbox.insert(tk.END, player_name)
            self.add_detection_log(f"Whitelist'e eklendi: {player_name}")
            print(f"Whitelist'e eklendi: {player_name}")
        else:
            messagebox.showinfo("Bilgi", f"'{player_name}' zaten whitelist'te!")
            
    def delete_from_whitelist(self):
        """Seçili oyuncuyu whitelist'ten sil"""
        selection = self.whitelist_listbox.curselection()
        if selection:
            player_name = self.whitelist_listbox.get(selection[0])
            self.whitelist_listbox.delete(selection[0])
            self.add_detection_log(f"Whitelist'ten silindi: {player_name}")
            print(f"Whitelist'ten silindi: {player_name}")
        else:
            messagebox.showwarning("Uyarı", "Silinecek oyuncu seçin!")
            
    def clear_whitelist(self):
        """Whitelist'i temizle"""
        result = messagebox.askyesno("Onay", "Tüm whitelist'i temizlemek istiyor musunuz?")
        if result:
            self.whitelist_listbox.delete(0, tk.END)
            self.add_detection_log("Whitelist temizlendi")
            print("Whitelist temizlendi")
            
    def clear_detection_log(self):
        """Algılama kayıtlarını temizle"""
        self.detection_log.delete(1.0, tk.END)
        
    def test_detection(self):
        """Algılama testi yap"""
        import random
        
        # Rastgele test oyuncusu
        test_players = ["TestPlayer1", "GM_Admin", "Hacker123", "NormalUser", "Moderator"]
        detected_player = random.choice(test_players)
        
        is_gm = "GM" in detected_player or "Moderator" in detected_player
        
        if is_gm:
            self.add_detection_log(f"🚨 GM ALGıLANDı: {detected_player}")
            self.simulate_gm_reaction()
        else:
            self.add_detection_log(f"👤 Oyuncu algılandı: {detected_player}")
            self.simulate_player_reaction()
            
    def simulate_player_reaction(self):
        """Oyuncu algılama tepkisini simüle et"""
        reactions = []
        
        if self.player_stop_wait_range.get():
            reactions.append("Wait+Range durduruldu")
        if self.player_stop_speedhacks.get():
            reactions.append("Speed hacks durduruldu")
        if self.player_stop_bot.get():
            reactions.append("Bot durduruldu")
        if self.player_quit_game.get():
            reactions.append("Oyun kapatılacak")
        if self.player_sound_alarm.get():
            reactions.append("Alarm çalıyor")
            
        if reactions:
            self.add_detection_log(f"Tepkiler: {', '.join(reactions)}")
        else:
            self.add_detection_log("Hiçbir tepki ayarlanmamış")
            
    def simulate_gm_reaction(self):
        """GM algılama tepkisini simüle et"""
        reactions = []
        
        if self.gm_stop_wait_range.get():
            reactions.append("Wait+Range durduruldu")
        if self.gm_stop_speedhacks.get():
            reactions.append("Speed hacks durduruldu")
        if self.gm_stop_bot.get():
            reactions.append("Bot durduruldu")
        if self.gm_quit_game.get():
            reactions.append("Oyun kapatılacak")
        if self.gm_sound_alarm.get():
            reactions.append("Alarm çalıyor")
            
        if reactions:
            self.add_detection_log(f"GM Tepkileri: {', '.join(reactions)}")
        else:
            self.add_detection_log("Hiçbir GM tepkisi ayarlanmamış")
            
    def add_detection_log(self, message):
        """Algılama log'una mesaj ekle"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.detection_log.insert(tk.END, log_entry)
        self.detection_log.see(tk.END)
        
        # Log boyutunu sınırla
        lines = self.detection_log.get(1.0, tk.END).split('\n')
        if len(lines) > 500:
            self.detection_log.delete(1.0, f"{len(lines) - 500}.0")
            
    def reset_detection_stats(self):
        """Algılama istatistiklerini sıfırla"""
        self.detected_players_label.config(text="0")
        self.detected_gms_label.config(text="0")
        messagebox.showinfo("Sıfırlandı", "Algılama istatistikleri sıfırlandı!")
        
    def load_settings(self):
        """Ayarları yükle"""
        # Whitelist
        whitelist = self.settings.get("player_detection.whitelist", [])
        self.whitelist_listbox.delete(0, tk.END)
        for player in whitelist:
            self.whitelist_listbox.insert(tk.END, player)
            
        # Range ayarları
        self.player_range.set(self.settings.get("player_detection.range", 100))
        self.range_enabled.set(self.settings.get("player_detection.range_enabled", False))
        
        # Player reactions
        player_settings = self.settings.get("player_detection.on_player", {})
        self.player_stop_wait_range.set(player_settings.get("stop_wait_range", False))
        self.player_stop_speedhacks.set(player_settings.get("stop_speedhacks", False))
        self.player_stop_bot.set(player_settings.get("stop_bot", False))
        self.player_quit_game.set(player_settings.get("quit_game", False))
        self.player_sound_alarm.set(player_settings.get("sound_alarm", False))
        
        # GM reactions
        gm_settings = self.settings.get("player_detection.on_gm", {})
        self.gm_stop_wait_range.set(gm_settings.get("stop_wait_range", True))
        self.gm_stop_speedhacks.set(gm_settings.get("stop_speedhacks", True))
        self.gm_stop_bot.set(gm_settings.get("stop_bot", True))
        self.gm_quit_game.set(gm_settings.get("quit_game", False))
        self.gm_sound_alarm.set(gm_settings.get("sound_alarm", True))
        
    def save_settings(self):
        """Ayarları kaydet"""
        # Whitelist
        whitelist = list(self.whitelist_listbox.get(0, tk.END))
        self.settings.set("player_detection.whitelist", whitelist)
        
        # Range ayarları
        self.settings.set("player_detection.range", self.player_range.get())
        self.settings.set("player_detection.range_enabled", self.range_enabled.get())
        
        # Player reactions
        self.settings.set("player_detection.on_player.stop_wait_range", self.player_stop_wait_range.get())
        self.settings.set("player_detection.on_player.stop_speedhacks", self.player_stop_speedhacks.get())
        self.settings.set("player_detection.on_player.stop_bot", self.player_stop_bot.get())
        self.settings.set("player_detection.on_player.quit_game", self.player_quit_game.get())
        self.settings.set("player_detection.on_player.sound_alarm", self.player_sound_alarm.get())
        
        # GM reactions
        self.settings.set("player_detection.on_gm.stop_wait_range", self.gm_stop_wait_range.get())
        self.settings.set("player_detection.on_gm.stop_speedhacks", self.gm_stop_speedhacks.get())
        self.settings.set("player_detection.on_gm.stop_bot", self.gm_stop_bot.get())
        self.settings.set("player_detection.on_gm.quit_game", self.gm_quit_game.get())
        self.settings.set("player_detection.on_gm.sound_alarm", self.gm_sound_alarm.get())