#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Route ve Auto Route sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading

class RouteTab:
    """Route sekmesi"""
    
    def __init__(self, parent, settings, bot_engine):
        self.settings = settings
        self.bot_engine = bot_engine
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """UI'yi kur"""
        # Ana paned window
        paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sol panel - Route kaydı
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Sağ panel - Route yönetimi
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        # Sol panel içeriği
        self.setup_left_panel(left_frame)
        
        # Sağ panel içeriği
        self.setup_right_panel(right_frame)
        
    def setup_left_panel(self, parent):
        """Sol paneli kur (Route Recording)"""
        # Record Route grubu
        record_group = ttk.LabelFrame(parent, text="Record Route (Rota Kaydetme)", padding=10)
        record_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Recording durumu
        self.recording_status_label = ttk.Label(record_group, text="Durum: Kayıt yapılmıyor", 
                                               font=("Arial", 10, "bold"))
        self.recording_status_label.pack(pady=5)
        
        # Recording butonları
        record_buttons_frame = ttk.Frame(record_group)
        record_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.start_recording_btn = ttk.Button(record_buttons_frame, text="Start Recording", 
                                             command=self.start_recording)
        self.start_recording_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_recording_btn = ttk.Button(record_buttons_frame, text="Stop Recording", 
                                            command=self.stop_recording, state=tk.DISABLED)
        self.stop_recording_btn.pack(side=tk.LEFT, padx=2)
        
        self.pause_recording_btn = ttk.Button(record_buttons_frame, text="Pause", 
                                             command=self.pause_recording, state=tk.DISABLED)
        self.pause_recording_btn.pack(side=tk.LEFT, padx=2)
        
        # Recording ayarları
        recording_settings_frame = ttk.Frame(record_group)
        recording_settings_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(recording_settings_frame, text="Kayıt Aralığı:").pack(side=tk.LEFT)
        self.recording_interval = tk.IntVar(value=1000)
        interval_spin = ttk.Spinbox(recording_settings_frame, from_=100, to=5000, width=10, 
                                   textvariable=self.recording_interval)
        interval_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(recording_settings_frame, text="ms").pack(side=tk.LEFT)
        
        # Route Range grubu
        range_group = ttk.LabelFrame(parent, text="Route Range (Farm Alanı)", padding=10)
        range_group.pack(fill=tk.X, padx=5, pady=5)
        
        range_frame = ttk.Frame(range_group)
        range_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(range_frame, text="Farm Range:").pack(side=tk.LEFT)
        self.farm_range = tk.IntVar(value=100)
        range_spin = ttk.Spinbox(range_frame, from_=50, to=500, width=10, 
                                textvariable=self.farm_range)
        range_spin.pack(side=tk.LEFT, padx=5)
        
        # Route Preview
        preview_group = ttk.LabelFrame(parent, text="Route Preview (Rota Önizleme)", padding=10)
        preview_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Canvas for route visualization
        self.route_canvas = tk.Canvas(preview_group, bg="white", height=200)
        self.route_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Route info
        self.route_info_label = ttk.Label(preview_group, text="Rota bilgisi: Henüz rota yok")
        self.route_info_label.pack(pady=2)
        
        # Preview butonları
        preview_buttons_frame = ttk.Frame(preview_group)
        preview_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(preview_buttons_frame, text="Rotayı Çiz", 
                  command=self.draw_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(preview_buttons_frame, text="Temizle", 
                  command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
        
    def setup_right_panel(self, parent):
        """Sağ paneli kur (Route Management)"""
        # Route Management grubu
        management_group = ttk.LabelFrame(parent, text="Route Management (Rota Yönetimi)", padding=10)
        management_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Route name
        name_frame = ttk.Frame(management_group)
        name_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(name_frame, text="Route Name:").pack(side=tk.LEFT)
        self.route_name_var = tk.StringVar(value="my_route")
        name_entry = ttk.Entry(name_frame, textvariable=self.route_name_var, width=20)
        name_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Route management butonları
        mgmt_buttons_frame = ttk.Frame(management_group)
        mgmt_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(mgmt_buttons_frame, text="Save", 
                  command=self.save_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(mgmt_buttons_frame, text="Load", 
                  command=self.load_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(mgmt_buttons_frame, text="Delete", 
                  command=self.delete_route).pack(side=tk.LEFT, padx=2)
        ttk.Button(mgmt_buttons_frame, text="Clear Route", 
                  command=self.clear_route).pack(side=tk.LEFT, padx=2)
        
        # Kaydedilmiş rotalar listesi
        saved_routes_frame = ttk.Frame(management_group)
        saved_routes_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(saved_routes_frame, text="Kaydedilmiş Rotalar:").pack(anchor=tk.W)
        self.saved_routes_combo = ttk.Combobox(saved_routes_frame, state="readonly", width=25)
        self.saved_routes_combo.pack(fill=tk.X, pady=2)
        self.saved_routes_combo.bind('<<ComboboxSelected>>', self.on_route_selected)
        
        # Auto Route grubu
        auto_route_group = ttk.LabelFrame(parent, text="Auto Route (Otomatik Rota)", padding=10)
        auto_route_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Auto route durumu
        self.auto_route_status_label = ttk.Label(auto_route_group, text="Durum: Durduruldu", 
                                                font=("Arial", 10, "bold"))
        self.auto_route_status_label.pack(pady=5)
        
        # Auto route butonları
        auto_buttons_frame = ttk.Frame(auto_route_group)
        auto_buttons_frame.pack(fill=tk.X, pady=5)
        
        self.start_auto_route_btn = ttk.Button(auto_buttons_frame, text="Start Auto Route", 
                                              command=self.start_auto_route)
        self.start_auto_route_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_auto_route_btn = ttk.Button(auto_buttons_frame, text="Stop Auto Route", 
                                             command=self.stop_auto_route, state=tk.DISABLED)
        self.stop_auto_route_btn.pack(side=tk.LEFT, padx=2)
        
        # Auto route ayarları
        auto_settings_frame = ttk.Frame(auto_route_group)
        auto_settings_frame.pack(fill=tk.X, pady=5)
        
        self.loop_route = tk.BooleanVar(value=True)
        ttk.Checkbutton(auto_settings_frame, text="Rotayı Tekrarla", 
                       variable=self.loop_route).pack(anchor=tk.W)
        
        self.reverse_route = tk.BooleanVar()
        ttk.Checkbutton(auto_settings_frame, text="Ters Yönde Çalıştır", 
                       variable=self.reverse_route).pack(anchor=tk.W)
        
        speed_frame = ttk.Frame(auto_settings_frame)
        speed_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(speed_frame, text="Hareket Hızı:").pack(side=tk.LEFT)
        self.route_speed = tk.IntVar(value=100)
        speed_spin = ttk.Spinbox(speed_frame, from_=50, to=300, width=10, 
                                textvariable=self.route_speed)
        speed_spin.pack(side=tk.LEFT, padx=5)
        ttk.Label(speed_frame, text="%").pack(side=tk.LEFT)
        
        # Route Statistics
        stats_group = ttk.LabelFrame(parent, text="Rota İstatistikleri", padding=10)
        stats_group.pack(fill=tk.X, padx=5, pady=5)
        
        stats_frame = ttk.Frame(stats_group)
        stats_frame.pack(fill=tk.X)
        
        # Sol kolon
        left_stats = ttk.Frame(stats_frame)
        left_stats.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(left_stats, text="Toplam Nokta:").pack(anchor=tk.W)
        self.total_points_label = ttk.Label(left_stats, text="0", font=("Arial", 12, "bold"))
        self.total_points_label.pack(anchor=tk.W, padx=10)
        
        ttk.Label(left_stats, text="Rota Uzunluğu:").pack(anchor=tk.W, pady=(10, 0))
        self.route_length_label = ttk.Label(left_stats, text="0 pixel", font=("Arial", 12, "bold"))
        self.route_length_label.pack(anchor=tk.W, padx=10)
        
        # Sağ kolon
        right_stats = ttk.Frame(stats_frame)
        right_stats.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        ttk.Label(right_stats, text="Tamamlanan Tur:").pack(anchor=tk.W)
        self.completed_loops_label = ttk.Label(right_stats, text="0", font=("Arial", 12, "bold"))
        self.completed_loops_label.pack(anchor=tk.W, padx=10)
        
        ttk.Label(right_stats, text="Geçen Süre:").pack(anchor=tk.W, pady=(10, 0))
        self.elapsed_time_label = ttk.Label(right_stats, text="00:00:00", font=("Arial", 12, "bold"))
        self.elapsed_time_label.pack(anchor=tk.W, padx=10)
        
        # Route Log
        log_group = ttk.LabelFrame(parent, text="Rota Kayıtları", padding=10)
        log_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        log_frame = ttk.Frame(log_group)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.route_log = tk.Text(log_frame, height=8, wrap=tk.WORD)
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.route_log.yview)
        self.route_log.configure(yscrollcommand=log_scrollbar.set)
        
        self.route_log.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Log kontrol butonları
        log_control_frame = ttk.Frame(log_group)
        log_control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(log_control_frame, text="Kayıtları Temizle", 
                  command=self.clear_route_log).pack(side=tk.LEFT)
        
        # Refresh butonları
        self.refresh_routes_list()
        
    def start_recording(self):
        """Rota kaydını başlat"""
        try:
            if hasattr(self.bot_engine, 'start_route_recording'):
                self.bot_engine.start_route_recording()
                
            self.recording_status_label.config(text="Durum: Kayıt yapılıyor", foreground="red")
            self.start_recording_btn.config(state=tk.DISABLED)
            self.stop_recording_btn.config(state=tk.NORMAL)
            self.pause_recording_btn.config(state=tk.NORMAL)
            
            self.add_route_log("Rota kaydı başlatıldı")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rota kaydı başlatılırken hata:\n{e}")
            
    def stop_recording(self):
        """Rota kaydını durdur"""
        try:
            if hasattr(self.bot_engine, 'stop_route_recording'):
                self.bot_engine.stop_route_recording()
                
            self.recording_status_label.config(text="Durum: Kayıt durduruldu", foreground="black")
            self.start_recording_btn.config(state=tk.NORMAL)
            self.stop_recording_btn.config(state=tk.DISABLED)
            self.pause_recording_btn.config(state=tk.DISABLED)
            
            self.add_route_log("Rota kaydı durduruldu")
            self.update_route_stats()
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rota kaydı durdurulurken hata:\n{e}")
            
    def pause_recording(self):
        """Rota kaydını duraklat"""
        # Bu fonksiyon implementasyonu bot_engine'de olacak
        self.add_route_log("Rota kaydı duraklatıldı")
        
    def save_route(self):
        """Rotayı kaydet"""
        route_name = self.route_name_var.get().strip()
        if not route_name:
            messagebox.showwarning("Uyarı", "Rota adı boş olamaz!")
            return
            
        try:
            if hasattr(self.bot_engine, 'save_current_route'):
                self.bot_engine.save_current_route(route_name)
                
            self.refresh_routes_list()
            self.add_route_log(f"Rota kaydedildi: {route_name}")
            messagebox.showinfo("Başarılı", f"Rota kaydedildi: {route_name}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rota kaydedilirken hata:\n{e}")
            
    def load_route(self):
        """Rota yükle"""
        route_name = self.saved_routes_combo.get()
        if not route_name:
            messagebox.showwarning("Uyarı", "Yüklenecek rota seçin!")
            return
            
        try:
            if hasattr(self.bot_engine, 'load_route'):
                self.bot_engine.load_route(route_name)
                
            self.add_route_log(f"Rota yüklendi: {route_name}")
            self.update_route_stats()
            self.draw_route()
            messagebox.showinfo("Başarılı", f"Rota yüklendi: {route_name}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rota yüklenirken hata:\n{e}")
            
    def delete_route(self):
        """Rota sil"""
        route_name = self.saved_routes_combo.get()
        if not route_name:
            messagebox.showwarning("Uyarı", "Silinecek rota seçin!")
            return
            
        result = messagebox.askyesno("Onay", f"'{route_name}' rotasını silmek istiyor musunuz?")
        if result:
            try:
                self.settings.delete_route(route_name)
                self.refresh_routes_list()
                self.add_route_log(f"Rota silindi: {route_name}")
                messagebox.showinfo("Başarılı", f"Rota silindi: {route_name}")
                
            except Exception as e:
                messagebox.showerror("Hata", f"Rota silinirken hata:\n{e}")
                
    def clear_route(self):
        """Mevcut rotayı temizle"""
        result = messagebox.askyesno("Onay", "Mevcut rotayı temizlemek istiyor musunuz?")
        if result:
            if hasattr(self.bot_engine, 'current_route'):
                self.bot_engine.current_route = []
                
            self.clear_canvas()
            self.update_route_stats()
            self.add_route_log("Mevcut rota temizlendi")
            
    def start_auto_route(self):
        """Otomatik rotayı başlat"""
        try:
            if hasattr(self.bot_engine, 'current_route') and self.bot_engine.current_route:
                self.settings.set("routes.auto_route_enabled", True)
                
                self.auto_route_status_label.config(text="Durum: Çalışıyor", foreground="green")
                self.start_auto_route_btn.config(state=tk.DISABLED)
                self.stop_auto_route_btn.config(state=tk.NORMAL)
                
                self.add_route_log("Otomatik rota başlatıldı")
                
                # Timer başlat
                self.start_route_timer()
                
            else:
                messagebox.showwarning("Uyarı", "Önce bir rota yükleyin!")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Otomatik rota başlatılırken hata:\n{e}")
            
    def stop_auto_route(self):
        """Otomatik rotayı durdur"""
        try:
            self.settings.set("routes.auto_route_enabled", False)
            
            self.auto_route_status_label.config(text="Durum: Durduruldu", foreground="black")
            self.start_auto_route_btn.config(state=tk.NORMAL)
            self.stop_auto_route_btn.config(state=tk.DISABLED)
            
            self.add_route_log("Otomatik rota durduruldu")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Otomatik rota durdurulurken hata:\n{e}")
            
    def draw_route(self):
        """Rotayı canvas'a çiz"""
        self.clear_canvas()
        
        if hasattr(self.bot_engine, 'current_route') and self.bot_engine.current_route:
            route = self.bot_engine.current_route
            
            if len(route) < 2:
                return
                
            # Canvas boyutlarını al
            canvas_width = self.route_canvas.winfo_width()
            canvas_height = self.route_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                self.route_canvas.after(100, self.draw_route)  # Tekrar dene
                return
                
            # Route koordinatlarını normalize et
            min_x = min(point.get('x', 0) for point in route)
            max_x = max(point.get('x', 0) for point in route)
            min_y = min(point.get('y', 0) for point in route)
            max_y = max(point.get('y', 0) for point in route)
            
            if max_x == min_x or max_y == min_y:
                return
                
            # Ölçekleme faktörleri
            scale_x = (canvas_width - 40) / (max_x - min_x)
            scale_y = (canvas_height - 40) / (max_y - min_y)
            scale = min(scale_x, scale_y)
            
            # Çizgiyi çiz
            for i in range(len(route) - 1):
                x1 = (route[i].get('x', 0) - min_x) * scale + 20
                y1 = (route[i].get('y', 0) - min_y) * scale + 20
                x2 = (route[i + 1].get('x', 0) - min_x) * scale + 20
                y2 = (route[i + 1].get('y', 0) - min_y) * scale + 20
                
                self.route_canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
                
            # Başlangıç ve bitiş noktalarını işaretle
            if route:
                # Başlangıç (yeşil)
                start_x = (route[0].get('x', 0) - min_x) * scale + 20
                start_y = (route[0].get('y', 0) - min_y) * scale + 20
                self.route_canvas.create_oval(start_x-5, start_y-5, start_x+5, start_y+5, 
                                            fill="green", outline="darkgreen")
                
                # Bitiş (kırmızı)
                end_x = (route[-1].get('x', 0) - min_x) * scale + 20
                end_y = (route[-1].get('y', 0) - min_y) * scale + 20
                self.route_canvas.create_oval(end_x-5, end_y-5, end_x+5, end_y+5, 
                                            fill="red", outline="darkred")
                
    def clear_canvas(self):
        """Canvas'ı temizle"""
        self.route_canvas.delete("all")
        
    def on_route_selected(self, event=None):
        """Rota seçildiğinde"""
        route_name = self.saved_routes_combo.get()
        self.route_name_var.set(route_name)
        
    def refresh_routes_list(self):
        """Rotalar listesini yenile"""
        try:
            routes = self.settings.get_routes()
            self.saved_routes_combo['values'] = routes
        except Exception as e:
            print(f"Rotalar listesi yenilenirken hata: {e}")
            
    def update_route_stats(self):
        """Rota istatistiklerini güncelle"""
        if hasattr(self.bot_engine, 'current_route') and self.bot_engine.current_route:
            route = self.bot_engine.current_route
            point_count = len(route)
            
            # Rota uzunluğunu hesapla
            total_length = 0
            for i in range(len(route) - 1):
                x1, y1 = route[i].get('x', 0), route[i].get('y', 0)
                x2, y2 = route[i + 1].get('x', 0), route[i + 1].get('y', 0)
                length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                total_length += length
                
            self.total_points_label.config(text=str(point_count))
            self.route_length_label.config(text=f"{int(total_length)} pixel")
            self.route_info_label.config(text=f"Rota bilgisi: {point_count} nokta, {int(total_length)} pixel uzunluk")
        else:
            self.total_points_label.config(text="0")
            self.route_length_label.config(text="0 pixel")
            self.route_info_label.config(text="Rota bilgisi: Henüz rota yok")
            
    def start_route_timer(self):
        """Rota timer'ını başlat"""
        import time
        self.route_start_time = time.time()
        self.update_timer()
        
    def update_timer(self):
        """Timer'ı güncelle"""
        if self.settings.get("routes.auto_route_enabled", False):
            import time
            elapsed = int(time.time() - getattr(self, 'route_start_time', time.time()))
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            
            self.elapsed_time_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            
            # 1 saniye sonra tekrar güncelle
            self.frame.after(1000, self.update_timer)
            
    def add_route_log(self, message):
        """Rota log'una mesaj ekle"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.route_log.insert(tk.END, log_entry)
        self.route_log.see(tk.END)
        
        # Log boyutunu sınırla
        lines = self.route_log.get(1.0, tk.END).split('\n')
        if len(lines) > 500:
            self.route_log.delete(1.0, f"{len(lines) - 500}.0")
            
    def clear_route_log(self):
        """Rota kayıtlarını temizle"""
        self.route_log.delete(1.0, tk.END)
        
    def load_settings(self):
        """Ayarları yükle"""
        self.recording_interval.set(self.settings.get("routes.recording_interval", 1000))
        self.farm_range.set(self.settings.get("farm.range", 100))
        self.route_speed.set(self.settings.get("routes.speed", 100))
        self.loop_route.set(self.settings.get("routes.loop", True))
        self.reverse_route.set(self.settings.get("routes.reverse", False))
        
        # Mevcut rota varsa yükle
        current_route_name = self.settings.get("routes.current_route", "")
        if current_route_name:
            self.route_name_var.set(current_route_name)
            self.saved_routes_combo.set(current_route_name)
            
    def save_settings(self):
        """Ayarları kaydet"""
        self.settings.set("routes.recording_interval", self.recording_interval.get())
        self.settings.set("farm.range", self.farm_range.get())
        self.settings.set("routes.speed", self.route_speed.get())
        self.settings.set("routes.loop", self.loop_route.get())
        self.settings.set("routes.reverse", self.reverse_route.get())
        self.settings.set("routes.current_route", self.route_name_var.get())