"""
Game Interaction Module for Mobile2 Global Bot
Handles actual game mechanics and memory manipulation
"""

import time
import random
import logging
from typing import List, Tuple, Optional, Dict
import win32gui
import win32api
import win32con
import win32process
import psutil
import ctypes
from ctypes import wintypes
import struct

logger = logging.getLogger(__name__)

class GameInteraction:
    def __init__(self):
        self.process_handle = None
        self.process_id = None
        self.window_handle = None
        self.base_address = None
        self.is_connected = False
        
        # Game memory offsets (these would need to be updated based on game version)
        self.offsets = {
            'player_hp': 0x12345678,
            'player_max_hp': 0x12345679,
            'player_mp': 0x1234567A,
            'player_max_mp': 0x1234567B,
            'player_x': 0x1234567C,
            'player_y': 0x1234567D,
            'player_z': 0x1234567E,
            'inventory_slot_1': 0x1234567F,
            'mob_list': 0x12345680,
            'item_list': 0x12345681,
            'player_list': 0x12345682,
        }
        
        # Key mappings for game controls
        self.keys = {
            'red_potion': 'F1',
            'blue_potion': 'F2',
            'attack': 'SPACE',
            'move_up': 'W',
            'move_down': 'S',
            'move_left': 'A',
            'move_right': 'D',
            'pickup': 'E',
            'chat': 'ENTER',
        }
    
    def connect_to_game(self, window_title: str = "Mobile2 Global") -> bool:
        """Connect to the game process"""
        try:
            # Find game window
            self.window_handle = win32gui.FindWindow(None, window_title)
            if not self.window_handle:
                logger.error(f"Game window '{window_title}' not found")
                return False
            
            # Get process ID
            _, self.process_id = win32process.GetWindowThreadProcessId(self.window_handle)
            
            # Open process handle
            self.process_handle = win32api.OpenProcess(
                win32con.PROCESS_ALL_ACCESS, False, self.process_id
            )
            
            if not self.process_handle:
                logger.error("Failed to open process handle")
                return False
            
            # Get base address
            self.base_address = self.get_module_base_address()
            
            self.is_connected = True
            logger.info("Successfully connected to game")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to game: {e}")
            return False
    
    def get_module_base_address(self) -> int:
        """Get the base address of the main game module"""
        try:
            process = psutil.Process(self.process_id)
            for module in process.memory_maps():
                if 'Mobile2' in module.path or 'Game' in module.path:
                    return int(module.addr.split('-')[0], 16)
            return 0x400000  # Default base address
        except Exception as e:
            logger.error(f"Failed to get base address: {e}")
            return 0x400000
    
    def read_memory(self, address: int, size: int) -> bytes:
        """Read memory from game process"""
        try:
            buffer = ctypes.create_string_buffer(size)
            bytes_read = ctypes.c_size_t()
            
            ctypes.windll.kernel32.ReadProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                buffer,
                size,
                ctypes.byref(bytes_read)
            )
            
            return buffer.raw
        except Exception as e:
            logger.error(f"Failed to read memory at {hex(address)}: {e}")
            return b'\x00' * size
    
    def write_memory(self, address: int, data: bytes) -> bool:
        """Write memory to game process"""
        try:
            bytes_written = ctypes.c_size_t()
            
            result = ctypes.windll.kernel32.WriteProcessMemory(
                self.process_handle,
                ctypes.c_void_p(address),
                data,
                len(data),
                ctypes.byref(bytes_written)
            )
            
            return result != 0
        except Exception as e:
            logger.error(f"Failed to write memory at {hex(address)}: {e}")
            return False
    
    def read_int(self, address: int) -> int:
        """Read 4-byte integer from memory"""
        data = self.read_memory(address, 4)
        return struct.unpack('<I', data)[0]
    
    def read_float(self, address: int) -> float:
        """Read 4-byte float from memory"""
        data = self.read_memory(address, 4)
        return struct.unpack('<f', data)[0]
    
    def write_int(self, address: int, value: int) -> bool:
        """Write 4-byte integer to memory"""
        data = struct.pack('<I', value)
        return self.write_memory(address, data)
    
    def write_float(self, address: int, value: float) -> bool:
        """Write 4-byte float to memory"""
        data = struct.pack('<f', value)
        return self.write_memory(address, data)
    
    def get_player_hp_percentage(self) -> float:
        """Get player HP percentage"""
        try:
            hp = self.read_int(self.base_address + self.offsets['player_hp'])
            max_hp = self.read_int(self.base_address + self.offsets['player_max_hp'])
            if max_hp > 0:
                return (hp / max_hp) * 100
            return 0
        except Exception as e:
            logger.error(f"Failed to get HP percentage: {e}")
            return 0
    
    def get_player_mp_percentage(self) -> float:
        """Get player MP percentage"""
        try:
            mp = self.read_int(self.base_address + self.offsets['player_mp'])
            max_mp = self.read_int(self.base_address + self.offsets['player_max_mp'])
            if max_mp > 0:
                return (mp / max_mp) * 100
            return 0
        except Exception as e:
            logger.error(f"Failed to get MP percentage: {e}")
            return 0
    
    def get_player_position(self) -> Tuple[float, float, float]:
        """Get player position (x, y, z)"""
        try:
            x = self.read_float(self.base_address + self.offsets['player_x'])
            y = self.read_float(self.base_address + self.offsets['player_y'])
            z = self.read_float(self.base_address + self.offsets['player_z'])
            return (x, y, z)
        except Exception as e:
            logger.error(f"Failed to get player position: {e}")
            return (0, 0, 0)
    
    def use_red_potion(self) -> bool:
        """Use red potion"""
        return self.send_key(self.keys['red_potion'])
    
    def use_blue_potion(self) -> bool:
        """Use blue potion"""
        return self.send_key(self.keys['blue_potion'])
    
    def attack(self) -> bool:
        """Perform attack"""
        return self.send_key(self.keys['attack'])
    
    def move_to_position(self, x: float, y: float, z: float) -> bool:
        """Move player to specified position"""
        try:
            # This would involve pathfinding and movement logic
            # For now, just send movement keys
            current_x, current_y, current_z = self.get_player_position()
            
            if x > current_x:
                self.send_key(self.keys['move_right'])
            elif x < current_x:
                self.send_key(self.keys['move_left'])
            
            if y > current_y:
                self.send_key(self.keys['move_up'])
            elif y < current_y:
                self.send_key(self.keys['move_down'])
            
            return True
        except Exception as e:
            logger.error(f"Failed to move to position: {e}")
            return False
    
    def pickup_item(self) -> bool:
        """Pickup nearby item"""
        return self.send_key(self.keys['pickup'])
    
    def send_chat_message(self, message: str) -> bool:
        """Send chat message"""
        try:
            # Open chat
            self.send_key(self.keys['chat'])
            time.sleep(0.1)
            
            # Type message
            for char in message:
                self.send_key(char)
                time.sleep(0.01)
            
            # Send message
            self.send_key(self.keys['chat'])
            return True
        except Exception as e:
            logger.error(f"Failed to send chat message: {e}")
            return False
    
    def send_key(self, key: str) -> bool:
        """Send key press to game window"""
        try:
            if not self.window_handle:
                return False
            
            # Convert key string to virtual key code
            vk_code = self.get_virtual_key_code(key)
            if vk_code is None:
                return False
            
            # Send key down
            win32api.PostMessage(self.window_handle, win32con.WM_KEYDOWN, vk_code, 0)
            time.sleep(0.05)
            
            # Send key up
            win32api.PostMessage(self.window_handle, win32con.WM_KEYUP, vk_code, 0)
            
            return True
        except Exception as e:
            logger.error(f"Failed to send key {key}: {e}")
            return False
    
    def get_virtual_key_code(self, key: str) -> Optional[int]:
        """Get virtual key code for key string"""
        key_map = {
            'F1': win32con.VK_F1,
            'F2': win32con.VK_F2,
            'F3': win32con.VK_F3,
            'F4': win32con.VK_F4,
            'F5': win32con.VK_F5,
            'F6': win32con.VK_F6,
            'F7': win32con.VK_F7,
            'F8': win32con.VK_F8,
            'F9': win32con.VK_F9,
            'F10': win32con.VK_F10,
            'F11': win32con.VK_F11,
            'F12': win32con.VK_F12,
            'SPACE': win32con.VK_SPACE,
            'ENTER': win32con.VK_RETURN,
            'W': ord('W'),
            'A': ord('A'),
            'S': ord('S'),
            'D': ord('D'),
            'E': ord('E'),
            'Q': ord('Q'),
            'R': ord('R'),
            'T': ord('T'),
            'Y': ord('Y'),
            'U': ord('U'),
            'I': ord('I'),
            'O': ord('O'),
            'P': ord('P'),
        }
        
        return key_map.get(key.upper())
    
    def get_mobs_in_range(self, range_distance: float) -> List[Dict]:
        """Get list of mobs within specified range"""
        try:
            # This would read from the mob list in memory
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Failed to get mobs in range: {e}")
            return []
    
    def get_items_in_range(self, range_distance: float) -> List[Dict]:
        """Get list of items within specified range"""
        try:
            # This would read from the item list in memory
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Failed to get items in range: {e}")
            return []
    
    def get_players_in_range(self, range_distance: float) -> List[Dict]:
        """Get list of players within specified range"""
        try:
            # This would read from the player list in memory
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Failed to get players in range: {e}")
            return []
    
    def enable_wallhack(self) -> bool:
        """Enable wallhack functionality"""
        try:
            # This would modify game memory to enable wallhack
            # For now, just return True
            return True
        except Exception as e:
            logger.error(f"Failed to enable wallhack: {e}")
            return False
    
    def set_movement_speed(self, speed: float) -> bool:
        """Set player movement speed"""
        try:
            # This would modify movement speed in memory
            # For now, just return True
            return True
        except Exception as e:
            logger.error(f"Failed to set movement speed: {e}")
            return False
    
    def set_attack_speed(self, speed: float) -> bool:
        """Set attack speed"""
        try:
            # This would modify attack speed in memory
            # For now, just return True
            return True
        except Exception as e:
            logger.error(f"Failed to set attack speed: {e}")
            return False
    
    def upgrade_item_slot1(self) -> bool:
        """Upgrade item in slot 1"""
        try:
            # This would perform the upgrade action
            # For now, just return True
            return True
        except Exception as e:
            logger.error(f"Failed to upgrade item in slot 1: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from game process"""
        try:
            if self.process_handle:
                win32api.CloseHandle(self.process_handle)
                self.process_handle = None
            
            self.is_connected = False
            logger.info("Disconnected from game")
        except Exception as e:
            logger.error(f"Failed to disconnect: {e}")