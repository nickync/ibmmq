import pyautogui
import time
import random
import threading
import keyboard

class AdvancedAutoClicker:
    def __init__(self):
        self.is_running = False
        self.click_thread = None
        self.mouse_interval = 0.5  # seconds between mouse clicks
        self.key_interval = 0.3    # seconds between key presses
        self.mouse_button = 'left'
        self.keys = ['w', 'a', 's', 'd']
        self.key_probability = 0.3  # 30% chance to press a key with each click
        
    def random_key_press(self):
        """Press a random WASD key"""
        key = random.choice(self.keys)
        pyautogui.press(key)
        return key
        
    def click_and_key_loop(self):
        """Main loop with mouse clicks and random WASD keys"""
        print("Auto-clicker started! Press F6 to stop.")
        print(f"Mouse interval: {self.mouse_interval}s, Key interval: {self.key_interval}s")
        print(f"Key probability: {self.key_probability*100}%")
        
        click_count = 0
        key_count = 0
        
        while self.is_running:
            # Mouse click
            pyautogui.click(button=self.mouse_button)
            click_count += 1
            
            # Random key press based on probability
            if random.random() < self.key_probability:
                key = self.random_key_press()
                key_count += 1
                print(f"Click {click_count} + Key '{key}' pressed")
            else:
                print(f"Click {click_count}")
            
            # Random delay between mouse clicks (with slight variation)
            actual_interval = self.mouse_interval * (0.8 + 0.4 * random.random())
            time.sleep(actual_interval)
            
            # Occasionally press a key between clicks
            if random.random() < 0.2:  # 20% chance for extra key press
                key = self.random_key_press()
                key_count += 1
                print(f"Extra key '{key}' pressed")
                time.sleep(self.key_interval * random.uniform(0.5, 1.5))
    
    def start(self):
        """Start the auto-clicker"""
        if not self.is_running:
            self.is_running = True
            self.click_thread = threading.Thread(target=self.click_and_key_loop)
            self.click_thread.daemon = True
            self.click_thread.start()
            print("Auto-clicker started")
    
    def stop(self):
        """Stop the auto-clicker"""
        self.is_running = False
        if self.click_thread:
            self.click_thread.join(timeout=0.5)
        print("Auto-clicker stopped")
    
    def toggle(self):
        """Toggle the auto-clicker on/off"""
        if self.is_running:
            self.stop()
        else:
            self.start()

def main():
    clicker = AdvancedAutoClicker()
    
    # Set up hotkeys
    keyboard.add_hotkey('F6', clicker.toggle)  # Start/Stop
    keyboard.add_hotkey('esc', lambda: exit())  # Exit program
    
    print("=" * 50)
    print("ADVANCED AUTO-CLICKER WITH WASD KEYS")
    print("=" * 50)
    print("Hotkeys:")
    print("  F6 - Start/Stop clicking")
    print("  ESC - Exit program")
    print("\nConfiguration:")
    print(f"  Mouse click interval: {clicker.mouse_interval}s")
    print(f"  Key press interval: {clicker.key_interval}s")
    print(f"  Key probability: {clicker.key_probability*100}%")
    print("  Keys: W, A, S, D")
    print("\nPosition your mouse where you want to click")
    print("Press F6 to start...")
    
    # Keep the program running
    keyboard.wait('esc')

if __name__ == "__main__":
    main()