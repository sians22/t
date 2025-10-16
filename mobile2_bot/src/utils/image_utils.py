#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Görüntü işleme ve tanıma yardımcı fonksiyonları
"""

import cv2
import numpy as np
import pyautogui
from PIL import Image, ImageGrab
from typing import List, Tuple, Optional, Dict
import os

class ImageUtils:
    """Görüntü işleme yardımcı sınıfı"""
    
    def __init__(self):
        self.template_cache = {}
        self.templates_dir = "assets/templates"
        
        # Varsayılan eşik değerleri
        self.match_threshold = 0.8
        self.confidence_threshold = 0.7
        
        # Template dizinini oluştur
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> Optional[np.ndarray]:
        """Ekran görüntüsü al"""
        try:
            if region:
                # Belirtilen bölgeyi yakala
                screenshot = ImageGrab.grab(bbox=region)
            else:
                # Tüm ekranı yakala
                screenshot = ImageGrab.grab()
                
            # PIL Image'ı OpenCV formatına çevir
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
            
        except Exception as e:
            print(f"Ekran yakalama hatası: {e}")
            return None
            
    def load_template(self, template_name: str) -> Optional[np.ndarray]:
        """Template görüntüsü yükle"""
        try:
            # Cache'den kontrol et
            if template_name in self.template_cache:
                return self.template_cache[template_name]
                
            # Dosyadan yükle
            template_path = os.path.join(self.templates_dir, f"{template_name}.png")
            if os.path.exists(template_path):
                template = cv2.imread(template_path)
                self.template_cache[template_name] = template
                return template
            else:
                print(f"Template bulunamadı: {template_path}")
                return None
                
        except Exception as e:
            print(f"Template yükleme hatası: {e}")
            return None
            
    def save_template(self, image: np.ndarray, template_name: str) -> bool:
        """Template görüntüsü kaydet"""
        try:
            template_path = os.path.join(self.templates_dir, f"{template_name}.png")
            success = cv2.imwrite(template_path, image)
            
            if success:
                # Cache'e ekle
                self.template_cache[template_name] = image
                print(f"Template kaydedildi: {template_path}")
                
            return success
            
        except Exception as e:
            print(f"Template kaydetme hatası: {e}")
            return False
            
    def find_template(self, screenshot: np.ndarray, template_name: str, 
                     threshold: Optional[float] = None) -> List[Dict]:
        """Template'i ekranda ara"""
        try:
            template = self.load_template(template_name)
            if template is None:
                return []
                
            if threshold is None:
                threshold = self.match_threshold
                
            # Template matching yap
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            
            # Eşik değerinin üzerindeki eşleşmeleri bul
            locations = np.where(result >= threshold)
            
            matches = []
            template_h, template_w = template.shape[:2]
            
            for pt in zip(*locations[::-1]):  # Switch x and y
                confidence = result[pt[1], pt[0]]
                
                match = {
                    'x': pt[0],
                    'y': pt[1],
                    'width': template_w,
                    'height': template_h,
                    'center_x': pt[0] + template_w // 2,
                    'center_y': pt[1] + template_h // 2,
                    'confidence': confidence
                }
                matches.append(match)
                
            # Confidence'a göre sırala
            matches.sort(key=lambda x: x['confidence'], reverse=True)
            
            return matches
            
        except Exception as e:
            print(f"Template arama hatası: {e}")
            return []
            
    def find_best_match(self, screenshot: np.ndarray, template_name: str, 
                       threshold: Optional[float] = None) -> Optional[Dict]:
        """En iyi eşleşmeyi bul"""
        matches = self.find_template(screenshot, template_name, threshold)
        return matches[0] if matches else None
        
    def find_color_regions(self, screenshot: np.ndarray, target_color: Tuple[int, int, int], 
                          tolerance: int = 10) -> List[Dict]:
        """Belirtilen renkteki bölgeleri bul"""
        try:
            # BGR formatına çevir (OpenCV BGR kullanır)
            target_bgr = (target_color[2], target_color[1], target_color[0])
            
            # Renk aralığı oluştur
            lower_bound = np.array([max(0, c - tolerance) for c in target_bgr])
            upper_bound = np.array([min(255, c + tolerance) for c in target_bgr])
            
            # Renk maskesi oluştur
            mask = cv2.inRange(screenshot, lower_bound, upper_bound)
            
            # Konturları bul
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            regions = []
            for contour in contours:
                # Bounding rectangle al
                x, y, w, h = cv2.boundingRect(contour)
                
                # Çok küçük bölgeleri filtrele
                if w > 5 and h > 5:
                    region = {
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h,
                        'center_x': x + w // 2,
                        'center_y': y + h // 2,
                        'area': cv2.contourArea(contour)
                    }
                    regions.append(region)
                    
            # Alan büyüklüğüne göre sırala
            regions.sort(key=lambda x: x['area'], reverse=True)
            
            return regions
            
        except Exception as e:
            print(f"Renk bölgesi arama hatası: {e}")
            return []
            
    def detect_text_regions(self, screenshot: np.ndarray) -> List[Dict]:
        """Metin bölgelerini algıla"""
        try:
            # Gri tonlamaya çevir
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            
            # Threshold uygula
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Konturları bul
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_regions = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # Metin benzeri boyutları filtrele
                aspect_ratio = w / h if h > 0 else 0
                if 0.1 < aspect_ratio < 10 and w > 10 and h > 5:
                    region = {
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h,
                        'center_x': x + w // 2,
                        'center_y': y + h // 2
                    }
                    text_regions.append(region)
                    
            return text_regions
            
        except Exception as e:
            print(f"Metin algılama hatası: {e}")
            return []
            
    def create_template_from_region(self, screenshot: np.ndarray, 
                                   x: int, y: int, width: int, height: int, 
                                   template_name: str) -> bool:
        """Belirtilen bölgeden template oluştur"""
        try:
            # Bölgeyi kes
            template = screenshot[y:y+height, x:x+width]
            
            # Template'i kaydet
            return self.save_template(template, template_name)
            
        except Exception as e:
            print(f"Template oluşturma hatası: {e}")
            return False
            
    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """Görüntü kalitesini artır"""
        try:
            # Gürültü azaltma
            denoised = cv2.fastNlMeansDenoisingColored(image)
            
            # Keskinlik artırma
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(denoised, -1, kernel)
            
            return sharpened
            
        except Exception as e:
            print(f"Görüntü geliştirme hatası: {e}")
            return image
            
    def compare_images(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """İki görüntüyü karşılaştır"""
        try:
            # Boyutları eşitle
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
                
            # Structural Similarity Index kullan
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY) if len(img1.shape) == 3 else img1
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) if len(img2.shape) == 3 else img2
            
            # Basit correlation coefficient hesapla
            correlation = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)[0, 0]
            
            return correlation
            
        except Exception as e:
            print(f"Görüntü karşılaştırma hatası: {e}")
            return 0.0
            
    def detect_ui_elements(self, screenshot: np.ndarray) -> Dict:
        """UI elementlerini algıla"""
        try:
            elements = {
                'buttons': [],
                'text_areas': [],
                'health_bars': [],
                'mana_bars': []
            }
            
            # Butonları algıla (köşeli şekiller)
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Yaklaşık şekil bul
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                x, y, w, h = cv2.boundingRect(contour)
                
                # Buton benzeri şekiller (4 köşeli, uygun boyut)
                if len(approx) == 4 and 20 < w < 200 and 10 < h < 100:
                    elements['buttons'].append({
                        'x': x, 'y': y, 'width': w, 'height': h,
                        'center_x': x + w//2, 'center_y': y + h//2
                    })
                    
            # Sağlık/mana barlarını algıla (kırmızı/mavi çizgiler)
            # Kırmızı bölgeler (HP bar)
            red_regions = self.find_color_regions(screenshot, (255, 0, 0), tolerance=30)
            for region in red_regions:
                if region['width'] > region['height'] * 2:  # Yatay bar
                    elements['health_bars'].append(region)
                    
            # Mavi bölgeler (MP bar)
            blue_regions = self.find_color_regions(screenshot, (0, 0, 255), tolerance=30)
            for region in blue_regions:
                if region['width'] > region['height'] * 2:  # Yatay bar
                    elements['mana_bars'].append(region)
                    
            return elements
            
        except Exception as e:
            print(f"UI element algılama hatası: {e}")
            return {'buttons': [], 'text_areas': [], 'health_bars': [], 'mana_bars': []}
            
    def get_dominant_color(self, image: np.ndarray) -> Tuple[int, int, int]:
        """Görüntünün dominant rengini bul"""
        try:
            # Görüntüyü küçült (performans için)
            small_image = cv2.resize(image, (50, 50))
            
            # Renkleri düzleştir
            pixels = small_image.reshape(-1, 3)
            
            # K-means clustering ile dominant rengi bul
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=1, random_state=42)
            kmeans.fit(pixels)
            
            dominant_color = kmeans.cluster_centers_[0].astype(int)
            
            # BGR'den RGB'ye çevir
            return (dominant_color[2], dominant_color[1], dominant_color[0])
            
        except Exception as e:
            print(f"Dominant renk bulma hatası: {e}")
            # Varsayılan olarak siyah döndür
            return (0, 0, 0)