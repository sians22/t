#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Items ve Pickup sekmesi
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class ItemsTab:
    """Items sekmesi"""
    
    def __init__(self, parent, settings):
        self.settings = settings
        self.frame = ttk.Frame(parent)
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """UI'yi kur"""
        # Ana paned window (sol ve sağ panel)
        paned = ttk.PanedWindow(self.frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Sol panel - Item arama ve ekleme
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)
        
        # Sağ panel - Item listesi ve ayarlar
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        # Sol panel içeriği
        self.setup_left_panel(left_frame)
        
        # Sağ panel içeriği
        self.setup_right_panel(right_frame)
        
    def setup_left_panel(self, parent):
        """Sol paneli kur"""
        # Item arama grubu
        search_group = ttk.LabelFrame(parent, text="Item Arama", padding=10)
        search_group.pack(fill=tk.X, padx=5, pady=5)
        
        search_frame = ttk.Frame(search_group)
        search_frame.pack(fill=tk.X)
        
        ttk.Label(search_frame, text="Search Item:").pack(anchor=tk.W)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(fill=tk.X, pady=2)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Arama sonuçları listesi
        search_results_frame = ttk.Frame(search_group)
        search_results_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(search_results_frame, text="Arama Sonuçları:").pack(anchor=tk.W)
        
        # Listbox ve scrollbar
        listbox_frame = ttk.Frame(search_results_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        self.search_listbox = tk.Listbox(listbox_frame, height=10)
        search_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=self.search_listbox.yview)
        self.search_listbox.configure(yscrollcommand=search_scrollbar.set)
        
        self.search_listbox.pack(side="left", fill="both", expand=True)
        search_scrollbar.pack(side="right", fill="y")
        
        # Çift tıklama ile ekleme
        self.search_listbox.bind('<Double-1>', self.add_selected_item)
        
        # Add Item butonu
        add_btn = ttk.Button(search_group, text="Add Item (Seçili itemi ekle)", 
                            command=self.add_selected_item)
        add_btn.pack(pady=5)
        
        # Manuel item ekleme
        manual_group = ttk.LabelFrame(parent, text="Manuel Item Ekleme", padding=10)
        manual_group.pack(fill=tk.X, padx=5, pady=5)
        
        manual_frame = ttk.Frame(manual_group)
        manual_frame.pack(fill=tk.X)
        
        ttk.Label(manual_frame, text="Item Adı:").pack(anchor=tk.W)
        self.manual_item_var = tk.StringVar()
        manual_entry = ttk.Entry(manual_frame, textvariable=self.manual_item_var, width=30)
        manual_entry.pack(fill=tk.X, pady=2)
        
        add_manual_btn = ttk.Button(manual_group, text="Manuel Ekle", 
                                   command=self.add_manual_item)
        add_manual_btn.pack(pady=5)
        
        # Popüler itemler
        popular_group = ttk.LabelFrame(parent, text="Popüler İtemler", padding=10)
        popular_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Popüler item butonları
        popular_items = [
            "Gold", "Silver", "Copper", "Iron Ore", "Steel",
            "Health Potion", "Mana Potion", "Sword", "Shield", "Armor",
            "Ring", "Necklace", "Earring", "Gem", "Crystal"
        ]
        
        popular_frame = ttk.Frame(popular_group)
        popular_frame.pack(fill=tk.BOTH, expand=True)
        
        for i, item in enumerate(popular_items):
            row = i // 3
            col = i % 3
            btn = ttk.Button(popular_frame, text=item, width=15,
                           command=lambda x=item: self.add_popular_item(x))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="ew")
            
        # Grid column configure
        for i in range(3):
            popular_frame.columnconfigure(i, weight=1)
            
    def setup_right_panel(self, parent):
        """Sağ paneli kur"""
        # Pickup ayarları
        pickup_group = ttk.LabelFrame(parent, text="Pickup Ayarları", padding=10)
        pickup_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.pickup_filter_enabled = tk.BooleanVar()
        pickup_check = ttk.Checkbutton(pickup_group, text="Pickup Filter (Sadece listeye eklediğiniz itemleri toplar)", 
                                      variable=self.pickup_filter_enabled)
        pickup_check.pack(anchor=tk.W, pady=2)
        
        self.drop_no_bonus = tk.BooleanVar()
        drop_check = ttk.Checkbutton(pickup_group, text="Drop item if it has no bonus (Bütün itemleri toplar, efsunsuz ise yere atar)", 
                                    variable=self.drop_no_bonus)
        drop_check.pack(anchor=tk.W, pady=2)
        
        # Item listesi
        list_group = ttk.LabelFrame(parent, text="Item Listesi", padding=10)
        list_group.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Listbox ve scrollbar
        list_frame = ttk.Frame(list_group)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.items_listbox = tk.Listbox(list_frame, height=15)
        items_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.items_listbox.yview)
        self.items_listbox.configure(yscrollcommand=items_scrollbar.set)
        
        self.items_listbox.pack(side="left", fill="both", expand=True)
        items_scrollbar.pack(side="right", fill="y")
        
        # Liste kontrol butonları
        list_control_frame = ttk.Frame(list_group)
        list_control_frame.pack(fill=tk.X, pady=5)
        
        delete_btn = ttk.Button(list_control_frame, text="Delete Item (Seçili itemi sil)", 
                               command=self.delete_selected_item)
        delete_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = ttk.Button(list_control_frame, text="Clear Items (Tüm listeyi temizle)", 
                              command=self.clear_items)
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Dosya işlemleri
        file_group = ttk.LabelFrame(parent, text="Dosya İşlemleri", padding=10)
        file_group.pack(fill=tk.X, padx=5, pady=5)
        
        # Dosya adı
        filename_frame = ttk.Frame(file_group)
        filename_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(filename_frame, text="File Name:").pack(side=tk.LEFT)
        self.filename_var = tk.StringVar(value="my_items")
        filename_entry = ttk.Entry(filename_frame, textvariable=self.filename_var, width=20)
        filename_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Dosya butonları
        file_buttons_frame = ttk.Frame(file_group)
        file_buttons_frame.pack(fill=tk.X, pady=5)
        
        save_btn = ttk.Button(file_buttons_frame, text="Save File (Listeyi kaydet)", 
                             command=self.save_item_list)
        save_btn.pack(side=tk.LEFT, padx=2)
        
        load_btn = ttk.Button(file_buttons_frame, text="Load File (Liste yükle)", 
                             command=self.load_item_list)
        load_btn.pack(side=tk.LEFT, padx=2)
        
        delete_file_btn = ttk.Button(file_buttons_frame, text="Delete File (Dosya sil)", 
                                    command=self.delete_item_file)
        delete_file_btn.pack(side=tk.LEFT, padx=2)
        
        # Kaydedilmiş dosyalar listesi
        saved_files_frame = ttk.Frame(file_group)
        saved_files_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(saved_files_frame, text="Kaydedilmiş Listeler:").pack(anchor=tk.W)
        self.saved_files_combo = ttk.Combobox(saved_files_frame, state="readonly", width=25)
        self.saved_files_combo.pack(fill=tk.X, pady=2)
        self.saved_files_combo.bind('<<ComboboxSelected>>', self.on_file_selected)
        
        # Dosya listesini güncelle
        self.refresh_saved_files()
        
        # İstatistikler
        stats_group = ttk.LabelFrame(parent, text="İstatistikler", padding=10)
        stats_group.pack(fill=tk.X, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_group, text="Listede 0 item var")
        self.stats_label.pack()
        
    def on_search_change(self, event=None):
        """Arama değiştiğinde çağrılır"""
        search_term = self.search_var.get().lower()
        
        # Tüm mevcut itemleri ara
        all_items = [
            "Gold", "Silver", "Copper", "Iron Ore", "Steel", "Mithril",
            "Health Potion", "Mana Potion", "Stamina Potion", "Antidote",
            "Sword", "Axe", "Bow", "Staff", "Dagger", "Mace",
            "Shield", "Helmet", "Armor", "Boots", "Gloves",
            "Ring", "Necklace", "Earring", "Bracelet", "Amulet",
            "Ruby", "Sapphire", "Emerald", "Diamond", "Topaz",
            "Scroll of Teleport", "Scroll of Healing", "Scroll of Lightning",
            "Fish", "Bread", "Meat", "Apple", "Orange",
            "Key", "Lockpick", "Rope", "Torch", "Lantern"
        ]
        
        # Arama sonuçlarını filtrele
        if search_term:
            filtered_items = [item for item in all_items if search_term in item.lower()]
        else:
            filtered_items = all_items[:20]  # İlk 20 item
            
        # Listbox'ı güncelle
        self.search_listbox.delete(0, tk.END)
        for item in filtered_items:
            self.search_listbox.insert(tk.END, item)
            
    def add_selected_item(self, event=None):
        """Seçili itemi listeye ekle"""
        selection = self.search_listbox.curselection()
        if selection:
            item = self.search_listbox.get(selection[0])
            self.add_item_to_list(item)
            
    def add_manual_item(self):
        """Manuel item ekle"""
        item = self.manual_item_var.get().strip()
        if item:
            self.add_item_to_list(item)
            self.manual_item_var.set("")
        else:
            messagebox.showwarning("Uyarı", "Item adı boş olamaz!")
            
    def add_popular_item(self, item):
        """Popüler item ekle"""
        self.add_item_to_list(item)
        
    def add_item_to_list(self, item):
        """Item'i listeye ekle"""
        # Çift eklemeyi önle
        current_items = list(self.items_listbox.get(0, tk.END))
        if item not in current_items:
            self.items_listbox.insert(tk.END, item)
            self.update_stats()
            print(f"Item eklendi: {item}")
        else:
            messagebox.showinfo("Bilgi", f"'{item}' zaten listede!")
            
    def delete_selected_item(self):
        """Seçili itemi sil"""
        selection = self.items_listbox.curselection()
        if selection:
            item = self.items_listbox.get(selection[0])
            self.items_listbox.delete(selection[0])
            self.update_stats()
            print(f"Item silindi: {item}")
        else:
            messagebox.showwarning("Uyarı", "Silinecek item seçin!")
            
    def clear_items(self):
        """Tüm itemleri temizle"""
        result = messagebox.askyesno("Onay", "Tüm itemleri listeden silmek istiyor musunuz?")
        if result:
            self.items_listbox.delete(0, tk.END)
            self.update_stats()
            print("Tüm itemler temizlendi")
            
    def save_item_list(self):
        """Item listesini kaydet"""
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showwarning("Uyarı", "Dosya adı boş olamaz!")
            return
            
        items = list(self.items_listbox.get(0, tk.END))
        if not items:
            messagebox.showwarning("Uyarı", "Kaydedilecek item yok!")
            return
            
        try:
            self.settings.save_item_list(filename, items)
            self.refresh_saved_files()
            messagebox.showinfo("Başarılı", f"Item listesi kaydedildi: {filename}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken hata:\n{e}")
            
    def load_item_list(self):
        """Item listesi yükle"""
        filename = self.saved_files_combo.get()
        if not filename:
            messagebox.showwarning("Uyarı", "Yüklenecek dosya seçin!")
            return
            
        try:
            items = self.settings.load_item_list(filename)
            if items:
                self.items_listbox.delete(0, tk.END)
                for item in items:
                    self.items_listbox.insert(tk.END, item)
                self.update_stats()
                messagebox.showinfo("Başarılı", f"Item listesi yüklendi: {filename}")
            else:
                messagebox.showwarning("Uyarı", "Dosya boş veya bulunamadı!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya yüklenirken hata:\n{e}")
            
    def delete_item_file(self):
        """Item dosyasını sil"""
        filename = self.saved_files_combo.get()
        if not filename:
            messagebox.showwarning("Uyarı", "Silinecek dosya seçin!")
            return
            
        result = messagebox.askyesno("Onay", f"'{filename}' dosyasını silmek istiyor musunuz?")
        if result:
            try:
                import os
                file_path = os.path.join(self.settings.items_dir, f"{filename}.json")
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.refresh_saved_files()
                    messagebox.showinfo("Başarılı", f"Dosya silindi: {filename}")
                else:
                    messagebox.showwarning("Uyarı", "Dosya bulunamadı!")
            except Exception as e:
                messagebox.showerror("Hata", f"Dosya silinirken hata:\n{e}")
                
    def on_file_selected(self, event=None):
        """Dosya seçildiğinde"""
        filename = self.saved_files_combo.get()
        self.filename_var.set(filename)
        
    def refresh_saved_files(self):
        """Kaydedilmiş dosyalar listesini yenile"""
        try:
            files = self.settings.get_item_lists()
            self.saved_files_combo['values'] = files
        except Exception as e:
            print(f"Dosya listesi yenilenirken hata: {e}")
            
    def update_stats(self):
        """İstatistikleri güncelle"""
        item_count = self.items_listbox.size()
        self.stats_label.config(text=f"Listede {item_count} item var")
        
    def load_settings(self):
        """Ayarları yükle"""
        self.pickup_filter_enabled.set(self.settings.get("items.pickup_filter", False))
        self.drop_no_bonus.set(self.settings.get("items.drop_no_bonus", False))
        
        # Item listesini yükle
        items = self.settings.get("items.item_list", [])
        self.items_listbox.delete(0, tk.END)
        for item in items:
            self.items_listbox.insert(tk.END, item)
        self.update_stats()
        
        # Arama listesini başlat
        self.on_search_change()
        
    def save_settings(self):
        """Ayarları kaydet"""
        self.settings.set("items.pickup_filter", self.pickup_filter_enabled.get())
        self.settings.set("items.drop_no_bonus", self.drop_no_bonus.get())
        
        # Item listesini kaydet
        items = list(self.items_listbox.get(0, tk.END))
        self.settings.set("items.item_list", items)