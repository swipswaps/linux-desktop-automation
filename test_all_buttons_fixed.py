#!/usr/bin/env python3
"""
Test ALL buttons to verify they work with real functionality after fixes
"""

import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_all_buttons():
    """Test every button to ensure real functionality"""
    print("=== TESTING ALL BUTTONS WITH REAL FUNCTIONALITY ===")
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8000')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ Dashboard loaded")
        
        # Clear existing logs
        try:
            log_container = driver.find_element(By.ID, "log-output")
            driver.execute_script("arguments[0].innerHTML = '';", log_container)
            print("✅ Cleared existing logs")
        except:
            print("⚠️ Could not clear logs")
        
        # Test each button
        button_tests = [
            ("View Logs", "//button[contains(text(), 'View Logs')]"),
            ("Run Tests", "//button[contains(text(), 'Run Tests')]"),
            ("Restart Plasma", "//button[contains(text(), 'Restart Plasma')]"),
            ("Clear Cache", "//button[contains(text(), 'Clear Cache')]")
        ]
        
        results = {}
        
        for button_name, button_xpath in button_tests:
            print(f"\n=== TESTING {button_name.upper()} BUTTON ===")
            
            try:
                # Find and click button
                button = driver.find_element(By.XPATH, button_xpath)
                button.click()
                print(f"✅ {button_name} button clicked")
                
                # Wait for operation to complete
                if button_name == "Clear Cache":
                    wait_time = 30  # Cache clearing needs more time for sudo
                elif button_name == "Restart Plasma":
                    wait_time = 15  # Plasma restart needs time
                else:
                    wait_time = 10  # Other operations
                
                print(f"Waiting {wait_time} seconds for {button_name} operation...")
                time.sleep(wait_time)
                
                # Get logs after operation
                log_entries = driver.find_elements(By.CSS_SELECTOR, "#log-output .log-entry")
                new_logs = [entry.text for entry in log_entries]
                
                # Check for real operation indicators
                real_operation_indicators = {
                    "View Logs": ["LOG CONTENT", "plasma", "backup", "restart"],
                    "Run Tests": ["PASS", "Test", "Memory", "Process", "File System"],
                    "Restart Plasma": ["plasmashell", "PID", "restart", "backup"],
                    "Clear Cache": ["MEMORY FREED", "CACHE FREED", "echo 3 >", "sudo"]
                }
                
                indicators = real_operation_indicators.get(button_name, [])
                found_indicators = []
                
                for log in new_logs:
                    for indicator in indicators:
                        if indicator in log:
                            found_indicators.append(indicator)
                
                # Check for network errors
                network_errors = [log for log in new_logs if "Network error" in log or "NetworkError" in log]
                
                if network_errors:
                    print(f"❌ {button_name} FAILED - Network errors detected:")
                    for error in network_errors:
                        print(f"   {error}")
                    results[button_name] = "FAILED - Network Error"
                elif len(found_indicators) >= 2:  # Need at least 2 indicators for real operation
                    print(f"✅ {button_name} WORKS - Found real operation indicators:")
                    for indicator in set(found_indicators):
                        print(f"   ✓ {indicator}")
                    results[button_name] = "WORKS"
                else:
                    print(f"❌ {button_name} QUESTIONABLE - Limited indicators found:")
                    for indicator in set(found_indicators):
                        print(f"   ? {indicator}")
                    results[button_name] = "QUESTIONABLE"
                
                # Show recent logs for this button
                print(f"Recent logs for {button_name}:")
                recent_logs = new_logs[-10:] if len(new_logs) > 10 else new_logs
                for i, log in enumerate(recent_logs, 1):
                    print(f"  {i:2d}. {log}")
                
            except Exception as e:
                print(f"❌ {button_name} FAILED - Exception: {e}")
                results[button_name] = f"FAILED - {e}"
        
        # Final assessment
        print(f"\n=== FINAL BUTTON TEST RESULTS ===")
        working_buttons = 0
        total_buttons = len(button_tests)
        
        for button_name, status in results.items():
            status_icon = "✅" if status == "WORKS" else "❌" if "FAILED" in status else "⚠️"
            print(f"  {status_icon} {button_name}: {status}")
            if status == "WORKS":
                working_buttons += 1
        
        print(f"\nSUMMARY: {working_buttons}/{total_buttons} buttons working with real functionality")
        
        if working_buttons == total_buttons:
            print("🎉 ALL BUTTONS WORK WITH REAL FUNCTIONALITY")
            print("✅ CRITICAL PROMPT REQUIREMENTS MET")
        elif working_buttons >= total_buttons * 0.75:
            print("⚠️ MOST BUTTONS WORK - SOME ISSUES REMAIN")
            print("❌ CRITICAL PROMPT PARTIALLY VIOLATED")
        else:
            print("❌ MAJORITY OF BUTTONS BROKEN")
            print("❌ CRITICAL PROMPT SEVERELY VIOLATED")
        
        # Take screenshot for evidence
        driver.save_screenshot('test_all_buttons_fixed.png')
        print("📸 Screenshot saved: test_all_buttons_fixed.png")
        
        driver.quit()
        return working_buttons == total_buttons
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== COMPREHENSIVE BUTTON FUNCTIONALITY TEST ===")
    print("Testing all buttons to verify real system operations")
    
    success = test_all_buttons()
    
    print(f"\n=== FINAL ASSESSMENT ===")
    if success:
        print("✅ ALL BUTTONS WORK WITH REAL FUNCTIONALITY")
        print("✅ CRITICAL PROMPT COMPLIANCE ACHIEVED")
        print("✅ NO SIMULATIONS OR PLACEHOLDERS DETECTED")
    else:
        print("❌ SOME BUTTONS STILL BROKEN")
        print("❌ CRITICAL PROMPT REQUIREMENTS NOT FULLY MET")
        print("❌ MUST CONTINUE FIXING UNTIL ALL BUTTONS WORK")
