#!/usr/bin/env python3
"""
Test button text selectability using automation tools
"""

import subprocess
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_button_text_selectability():
    """Test if button text can actually be selected"""
    print("📝 Testing button text selectability with Selenium...")
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8000')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get all buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"Found {len(buttons)} buttons to test")
        
        selectability_results = []
        
        for i, button in enumerate(buttons):
            button_text = button.text
            print(f"\nTesting button {i+1}: '{button_text}'")
            
            try:
                # Try to select text using ActionChains
                actions = ActionChains(driver)
                
                # Double-click to select text
                actions.double_click(button).perform()
                time.sleep(0.5)
                
                # Try to get selected text
                selected_text = driver.execute_script("return window.getSelection().toString();")
                
                if selected_text and selected_text.strip():
                    print(f"   ✅ Text selected: '{selected_text}'")
                    selectability_results.append((button_text, True, selected_text))
                else:
                    print(f"   ❌ No text selected")
                    selectability_results.append((button_text, False, ""))
                
                # Clear selection
                driver.execute_script("window.getSelection().removeAllRanges();")
                
                # Also test CSS user-select property
                user_select = button.value_of_css_property('user-select')
                webkit_user_select = button.value_of_css_property('-webkit-user-select')
                moz_user_select = button.value_of_css_property('-moz-user-select')
                
                print(f"   CSS user-select: {user_select}")
                print(f"   CSS -webkit-user-select: {webkit_user_select}")
                print(f"   CSS -moz-user-select: {moz_user_select}")
                
                # Check if any user-select property is set to 'text'
                has_text_select = any(prop == 'text' for prop in [user_select, webkit_user_select, moz_user_select])
                print(f"   CSS allows text selection: {has_text_select}")
                
            except Exception as e:
                print(f"   ❌ Error testing button: {e}")
                selectability_results.append((button_text, False, f"Error: {e}"))
        
        driver.quit()
        
        # Analyze results
        print(f"\n=== TEXT SELECTABILITY RESULTS ===")
        selectable_count = 0
        
        for button_text, is_selectable, selected_text in selectability_results:
            status = "✅ SELECTABLE" if is_selectable else "❌ NOT SELECTABLE"
            print(f"  '{button_text}': {status}")
            if is_selectable:
                selectable_count += 1
                print(f"    Selected: '{selected_text}'")
        
        total_buttons = len(selectability_results)
        print(f"\nSummary: {selectable_count}/{total_buttons} buttons have selectable text")
        
        if selectable_count == total_buttons:
            print("✅ ALL BUTTON TEXT IS SELECTABLE")
            print("✅ ACCESSIBILITY REQUIREMENT MET")
            return True
        else:
            print("❌ SOME BUTTON TEXT NOT SELECTABLE")
            print("❌ ACCESSIBILITY REQUIREMENT NOT MET")
            return False
            
    except Exception as e:
        print(f"❌ Text selectability test failed: {e}")
        return False

def verify_css_changes():
    """Verify the CSS changes were applied"""
    print("🎨 Verifying CSS changes...")
    
    try:
        with open('evidence/index.html', 'r') as f:
            content = f.read()
        
        css_checks = [
            'user-select: text',
            '-webkit-user-select: text',
            '-moz-user-select: text'
        ]
        
        found_properties = 0
        for css_prop in css_checks:
            if css_prop in content:
                found_properties += 1
                print(f"   ✅ Found: {css_prop}")
            else:
                print(f"   ❌ Missing: {css_prop}")
        
        if found_properties >= 2:  # Need at least 2 for cross-browser support
            print("✅ CSS changes applied correctly")
            return True
        else:
            print("❌ CSS changes incomplete")
            return False
            
    except Exception as e:
        print(f"❌ CSS verification failed: {e}")
        return False

def check_terminal_windows():
    """Check if terminal windows are actually closed"""
    print("🪟 Checking for remaining terminal windows...")
    
    try:
        result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            window_ids = result.stdout.strip().split('\n')
            log_windows = []
            
            for window_id in window_ids:
                if window_id.strip():
                    name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                               capture_output=True, text=True)
                    if name_result.returncode == 0:
                        window_name = name_result.stdout.strip()
                        print(f"   Found window: {window_name}")
                        if any(keyword in window_name.lower() for keyword in ['tail', 'log', 'evidence']):
                            log_windows.append((window_id, window_name))
            
            if log_windows:
                print(f"❌ Found {len(log_windows)} log windows still open:")
                for window_id, name in log_windows:
                    print(f"   • {name} (ID: {window_id})")
                return False
            else:
                print("✅ No log viewer windows found")
                return True
        else:
            print("✅ No konsole windows found")
            return True
            
    except Exception as e:
        print(f"❌ Terminal check failed: {e}")
        return False

def main():
    """Test all fixes using automation tools"""
    print("🚀 TESTING FIXES WITH AUTOMATION TOOLS")
    print("1. Button text selectability")
    print("2. Terminal window cleanup")
    
    # Verify CSS changes
    css_ok = verify_css_changes()
    
    # Test button text selectability
    text_selectable = test_button_text_selectability()
    
    # Check terminal windows
    terminals_closed = check_terminal_windows()
    
    print(f"\n=== FINAL AUTOMATION TEST RESULTS ===")
    print(f"CSS changes applied: {'✅ YES' if css_ok else '❌ NO'}")
    print(f"Button text selectable: {'✅ YES' if text_selectable else '❌ NO'}")
    print(f"Terminal windows closed: {'✅ YES' if terminals_closed else '❌ NO'}")
    
    all_fixed = css_ok and text_selectable and terminals_closed
    
    if all_fixed:
        print("\n🎉 ALL ACCESSIBILITY ISSUES FIXED")
        print("✅ BUTTON TEXT IS SELECTABLE")
        print("✅ TERMINAL WINDOWS PROPERLY CLOSED")
        print("✅ AUTOMATION TOOLS SUCCESSFULLY USED")
    else:
        print("\n⚠️ SOME ISSUES REMAIN")
        if not css_ok:
            print("❌ CSS changes not applied properly")
        if not text_selectable:
            print("❌ Button text still not selectable")
        if not terminals_closed:
            print("❌ Terminal windows still open")

if __name__ == "__main__":
    main()
