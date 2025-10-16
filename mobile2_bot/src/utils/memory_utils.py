#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory okuma/yazma yardımcı fonksiyonları
"""

import ctypes
from ctypes import wintypes
import struct
from typing import Optional, Any

# Windows API fonksiyonları
kernel32 = ctypes.windll.kernel32
user32 = ctypes.windll.user32

# Process erişim hakları
PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008

class MemoryUtils:
    """Memory okuma/yazma yardımcı sınıfı"""
    
    def __init__(self):
        self.process_handle = None
        self.process_id = None
        
    def attach_to_process(self, process_id: int) -> bool:
        """Process'e attach ol"""
        try:
            self.process_handle = kernel32.OpenProcess(
                PROCESS_ALL_ACCESS,
                False,
                process_id
            )
            
            if self.process_handle:
                self.process_id = process_id
                print(f"Process'e bağlanıldı: PID {process_id}")
                return True
            else:
                print(f"Process'e bağlanılamadı: PID {process_id}")
                return False
                
        except Exception as e:
            print(f"Process attach hatası: {e}")
            return False
            
    def detach_from_process(self):
        """Process'ten ayrıl"""
        if self.process_handle:
            kernel32.CloseHandle(self.process_handle)
            self.process_handle = None
            self.process_id = None
            print("Process'ten ayrıldı")
            
    def read_memory(self, address: int, size: int) -> Optional[bytes]:
        """Memory'den veri oku"""
        try:
            if not self.process_handle:
                return None
                
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            
            success = kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                buffer,
                size,
                ctypes.byref(bytes_read)
            )
            
            if success and bytes_read.value == size:
                return buffer.raw
            else:
                return None
                
        except Exception as e:
            print(f"Memory okuma hatası: {e}")
            return None
            
    def write_memory(self, address: int, data: bytes) -> bool:
        """Memory'ye veri yaz"""
        try:
            if not self.process_handle:
                return False
                
            bytes_written = ctypes.c_size_t()
            
            success = kernel32.WriteProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                data,
                len(data),
                ctypes.byref(bytes_written)
            )
            
            return success and bytes_written.value == len(data)
            
        except Exception as e:
            print(f"Memory yazma hatası: {e}")
            return False
            
    def read_int(self, address: int) -> Optional[int]:
        """4 byte integer oku"""
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('<I', data)[0]
        return None
        
    def read_float(self, address: int) -> Optional[float]:
        """4 byte float oku"""
        data = self.read_memory(address, 4)
        if data:
            return struct.unpack('<f', data)[0]
        return None
        
    def read_double(self, address: int) -> Optional[float]:
        """8 byte double oku"""
        data = self.read_memory(address, 8)
        if data:
            return struct.unpack('<d', data)[0]
        return None
        
    def read_string(self, address: int, max_length: int = 256) -> Optional[str]:
        """String oku"""
        data = self.read_memory(address, max_length)
        if data:
            # Null terminator'a kadar oku
            null_pos = data.find(b'\x00')
            if null_pos != -1:
                data = data[:null_pos]
            try:
                return data.decode('utf-8')
            except:
                return data.decode('latin-1', errors='ignore')
        return None
        
    def write_int(self, address: int, value: int) -> bool:
        """4 byte integer yaz"""
        data = struct.pack('<I', value)
        return self.write_memory(address, data)
        
    def write_float(self, address: int, value: float) -> bool:
        """4 byte float yaz"""
        data = struct.pack('<f', value)
        return self.write_memory(address, data)
        
    def write_double(self, address: int, value: float) -> bool:
        """8 byte double yaz"""
        data = struct.pack('<d', value)
        return self.write_memory(address, data)
        
    def write_string(self, address: int, value: str) -> bool:
        """String yaz"""
        try:
            data = value.encode('utf-8') + b'\x00'
            return self.write_memory(address, data)
        except:
            return False
            
    def find_pattern(self, pattern: bytes, start_address: int = 0x400000, end_address: int = 0x7FFFFFFF) -> Optional[int]:
        """Memory'de pattern ara"""
        try:
            if not self.process_handle:
                return None
                
            current_address = start_address
            chunk_size = 4096  # 4KB chunks
            
            while current_address < end_address:
                data = self.read_memory(current_address, chunk_size)
                if data:
                    pos = data.find(pattern)
                    if pos != -1:
                        return current_address + pos
                        
                current_address += chunk_size - len(pattern) + 1
                
            return None
            
        except Exception as e:
            print(f"Pattern arama hatası: {e}")
            return None
            
    def read_pointer_chain(self, base_address: int, offsets: list) -> Optional[int]:
        """Pointer chain'i takip et"""
        try:
            current_address = base_address
            
            for offset in offsets[:-1]:
                current_address += offset
                pointer_value = self.read_int(current_address)
                if pointer_value is None:
                    return None
                current_address = pointer_value
                
            # Son offset'i ekle
            if offsets:
                current_address += offsets[-1]
                
            return current_address
            
        except Exception as e:
            print(f"Pointer chain okuma hatası: {e}")
            return None
            
    def get_module_base_address(self, module_name: str) -> Optional[int]:
        """Module'ün base adresini al"""
        try:
            # Bu fonksiyon gerçek implementasyon için psutil veya 
            # Windows API kullanarak module listesini almalı
            # Şimdilik basit bir implementasyon
            
            if module_name.lower() == "mobile2.exe":
                # Tipik bir oyun base adresi
                return 0x400000
            elif module_name.lower() == "kernel32.dll":
                return 0x7C800000
            elif module_name.lower() == "user32.dll":
                return 0x7E410000
                
            return None
            
        except Exception as e:
            print(f"Module base address alma hatası: {e}")
            return None
            
    def is_valid_address(self, address: int) -> bool:
        """Adres geçerli mi kontrol et"""
        try:
            if not self.process_handle:
                return False
                
            # 1 byte okumaya çalış
            data = self.read_memory(address, 1)
            return data is not None
            
        except:
            return False
            
    def allocate_memory(self, size: int) -> Optional[int]:
        """Memory'de alan ayır"""
        try:
            if not self.process_handle:
                return None
                
            address = kernel32.VirtualAllocEx(
                self.process_handle,
                None,
                size,
                0x1000 | 0x2000,  # MEM_COMMIT | MEM_RESERVE
                0x40  # PAGE_EXECUTE_READWRITE
            )
            
            return address if address else None
            
        except Exception as e:
            print(f"Memory allocation hatası: {e}")
            return None
            
    def free_memory(self, address: int) -> bool:
        """Ayrılan memory'yi serbest bırak"""
        try:
            if not self.process_handle:
                return False
                
            success = kernel32.VirtualFreeEx(
                self.process_handle,
                address,
                0,
                0x8000  # MEM_RELEASE
            )
            
            return bool(success)
            
        except Exception as e:
            print(f"Memory free hatası: {e}")
            return False
            
    def nop_instruction(self, address: int, size: int) -> bool:
        """Instruction'ları NOP ile doldur"""
        try:
            nop_bytes = b'\x90' * size  # 0x90 = NOP instruction
            return self.write_memory(address, nop_bytes)
            
        except Exception as e:
            print(f"NOP instruction hatası: {e}")
            return False
            
    def create_code_cave(self, size: int) -> Optional[int]:
        """Code cave oluştur"""
        try:
            # Memory ayır
            cave_address = self.allocate_memory(size)
            if not cave_address:
                return None
                
            # NOP'larla doldur
            if self.nop_instruction(cave_address, size):
                return cave_address
            else:
                self.free_memory(cave_address)
                return None
                
        except Exception as e:
            print(f"Code cave oluşturma hatası: {e}")
            return None