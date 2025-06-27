#!/usr/bin/env python3
"""
Test the final fixes for both issues using automation tools
"""

import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_button_text_full_selectability():
    """Test if button text can be fully selected (not just search-highlighted)"""
    print("📝 Testing FULL button text selectability...")
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8000')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Testing {len(buttons)} buttons for full text selection...")
        
        full_selection_results = []
        
        for i, button in enumerate(buttons):
            button_text = button.text
            print(f"\nTesting button {i+1}: '{button_text}'")
            
            try:
                # Test triple-click for full text selection
                actions = ActionChains(driver)
                
                # Triple-click to select all text
                actions.click(button).click(button).click(button).perform()
                time.sleep(0.5)
                
                # Get selected text
                selected_text = driver.execute_script("return window.getSelection().toString();")
                
                # Check if full text was selected (not just partial)
                full_text_selected = selected_text.strip() == button_text.strip()
                
                print(f"   Button text: '{button_text}'")
                print(f"   Selected: '{selected_text}'")
                print(f"   Full selection: {'✅' if full_text_selected else '❌'}")
                
                # Check CSS properties
                user_select = button.value_of_css_property('user-select')
                cursor = button.value_of_css_property('cursor')
                
                print(f"   CSS user-select: {user_select}")
                print(f"   CSS cursor: {cursor}")
                
                full_selection_results.append((button_text, full_text_selected, selected_text))
                
                # Clear selection
                driver.execute_script("window.getSelection().removeAllRanges();")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                full_selection_results.append((button_text, False, f"Error: {e}"))
        
        driver.quit()
        
        # Analyze results
        fully_selectable = sum(1 for _, selectable, _ in full_selection_results if selectable)
        total_buttons = len(full_selection_results)
        
        print(f"\n=== FULL TEXT SELECTION RESULTS ===")
        for button_text, selectable, selected in full_selection_results:
            status = "✅ FULLY SELECTABLE" if selectable else "❌ NOT FULLY SELECTABLE"
            print(f"  '{button_text}': {status}")
        
        print(f"\nSummary: {fully_selectable}/{total_buttons} buttons fully selectable")
        
        return fully_selectable == total_buttons
        
    except Exception as e:
        print(f"❌ Full selectability test failed: {e}")
        return False

def test_view_logs_terminal_behavior():
    """Test the View Logs terminal behavior and auto-cleanup"""
    print("🪟 Testing View Logs terminal behavior...")
    
    try:
        # First, check current terminal windows
        result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                              capture_output=True, text=True)
        
        initial_windows = []
        if result.returncode == 0:
            window_ids = result.stdout.strip().split('\n')
            for window_id in window_ids:
                if window_id.strip():
                    name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                               capture_output=True, text=True)
                    if name_result.returncode == 0:
                        window_name = name_result.stdout.strip()
                        initial_windows.append((window_id, window_name))
        
        print(f"Initial terminal windows: {len(initial_windows)}")
        for window_id, name in initial_windows:
            print(f"  {name}")
        
        # Trigger View Logs
        print("\nTriggering View Logs...")
        result = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/view-logs'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ View Logs API call successful")
            
            # Wait for terminal to open
            time.sleep(3)
            
            # Check for new terminal windows
            result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                                  capture_output=True, text=True)
            
            new_windows = []
            if result.returncode == 0:
                window_ids = result.stdout.strip().split('\n')
                for window_id in window_ids:
                    if window_id.strip():
                        name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                   capture_output=True, text=True)
                        if name_result.returncode == 0:
                            window_name = name_result.stdout.strip()
                            new_windows.append((window_id, window_name))
            
            print(f"\nTerminal windows after View Logs: {len(new_windows)}")
            
            log_windows = []
            for window_id, name in new_windows:
                print(f"  {name}")
                if any(keyword in name.lower() for keyword in ['tail', 'log', 'evidence']):
                    log_windows.append((window_id, name))
            
            if log_windows:
                print(f"\n✅ Log viewer opened: {len(log_windows)} windows")
                for window_id, name in log_windows:
                    print(f"  Log window: {name}")
                
                # Wait for auto-cleanup (15 seconds + buffer)
                print("\nWaiting for auto-cleanup (20 seconds)...")
                time.sleep(20)
                
                # Check if windows were auto-closed
                result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                                      capture_output=True, text=True)
                
                remaining_log_windows = []
                if result.returncode == 0:
                    window_ids = result.stdout.strip().split('\n')
                    for window_id in window_ids:
                        if window_id.strip():
                            name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                       capture_output=True, text=True)
                            if name_result.returncode == 0:
                                window_name = name_result.stdout.strip()
                                if any(keyword in window_name.lower() for keyword in ['tail', 'log', 'evidence']):
                                    remaining_log_windows.append((window_id, window_name))
                
                if remaining_log_windows:
                    print(f"❌ Auto-cleanup failed: {len(remaining_log_windows)} log windows still open")
                    for window_id, name in remaining_log_windows:
                        print(f"  Still open: {name}")
                        # Manual cleanup
                        subprocess.run(['xdotool', 'windowclose', window_id])
                        print(f"  ✅ Manually closed: {name}")
                    return False
                else:
                    print("✅ Auto-cleanup successful: No log windows remain")
                    return True
            else:
                print("❌ No log viewer windows detected")
                return False
        else:
            print(f"❌ View Logs API failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Terminal behavior test failed: {e}")
        return False

def main():
    """Test both final fixes"""
    print("🚀 TESTING FINAL FIXES WITH AUTOMATION TOOLS")
    print("1. Full button text selectability")
    print("2. View Logs terminal auto-cleanup")
    
    # Test button text selectability
    text_fully_selectable = test_button_text_full_selectability()
    
    # Test View Logs behavior
    terminal_cleanup_working = test_view_logs_terminal_behavior()
    
    print(f"\n=== FINAL FIX TEST RESULTS ===")
    print(f"Button text fully selectable: {'✅ YES' if text_fully_selectable else '❌ NO'}")
    print(f"View Logs auto-cleanup: {'✅ YES' if terminal_cleanup_working else '❌ NO'}")
    
    both_fixed = text_fully_selectable and terminal_cleanup_working
    
    if both_fixed:
        print("\n🎉 BOTH ISSUES COMPLETELY FIXED")
        print("✅ BUTTON TEXT FULLY SELECTABLE")
        print("✅ VIEW LOGS TERMINAL AUTO-CLOSES")
        print("✅ AUTOMATION TOOLS VERIFIED FIXES")
    else:
        print("\n⚠️ SOME ISSUES REMAIN")
        if not text_fully_selectable:
            print("❌ Button text still not fully selectable")
        if not terminal_cleanup_working:
            print("❌ View Logs terminal still not auto-closing")

if __name__ == "__main__":
    main()
