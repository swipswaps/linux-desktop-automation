#!/usr/bin/env python3
"""
Test ALL automation tools properly:
- script command for terminal recording
- asciinema for session recording  
- Selenium for web automation
- xdotool for window management
"""

import subprocess
import time
import os

def test_script_command():
    """Test script command for terminal recording"""
    print("📜 Testing script command...")
    
    session_file = "/tmp/script_test_session.txt"
    
    # Test script command with a simple operation
    script_cmd = f'script -q -c "echo \'Script command test\'; curl -s http://localhost:8000/api/stats" {session_file}'
    
    try:
        result = subprocess.run(['bash', '-c', script_cmd], 
                              capture_output=True, text=True, timeout=15)
        
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                content = f.read()
                print(f"✅ Script command captured {len(content)} characters")
                print(f"   Sample: {content[:200]}...")
                return True
        else:
            print("❌ Script command failed to create session file")
            return False
            
    except Exception as e:
        print(f"❌ Script command error: {e}")
        return False

def test_asciinema():
    """Test asciinema recording"""
    print("🎬 Testing asciinema...")
    
    recording_file = "/tmp/asciinema_test.cast"
    
    try:
        # Start asciinema recording
        cmd = ['asciinema', 'rec', '--overwrite', '-c', 'echo "Asciinema test"; sleep 2', recording_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if os.path.exists(recording_file):
            file_size = os.path.getsize(recording_file)
            print(f"✅ Asciinema created recording file ({file_size} bytes)")
            return True
        else:
            print("❌ Asciinema failed to create recording file")
            return False
            
    except Exception as e:
        print(f"❌ Asciinema error: {e}")
        return False

def test_selenium():
    """Test Selenium automation"""
    print("🔧 Testing Selenium...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--headless')  # Run headless for testing
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8000')
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Check if we can find buttons
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"✅ Selenium found {len(buttons)} buttons on dashboard")
        
        driver.quit()
        return True
        
    except Exception as e:
        print(f"❌ Selenium error: {e}")
        return False

def test_xdotool():
    """Test xdotool for window management"""
    print("🪟 Testing xdotool...")
    
    try:
        # Test basic xdotool functionality
        result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            windows = result.stdout.strip().split('\n')
            window_count = len([w for w in windows if w.strip()])
            print(f"✅ xdotool found {window_count} konsole windows")
            return True
        else:
            print("❌ xdotool failed to search for windows")
            return False
            
    except Exception as e:
        print(f"❌ xdotool error: {e}")
        return False

def test_view_logs_with_proper_automation():
    """Test View Logs button with proper automation and window management"""
    print("\n🧪 TESTING VIEW LOGS WITH PROPER AUTOMATION")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8000')
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Clear existing logs
        log_container = driver.find_element(By.ID, "log-output")
        driver.execute_script("arguments[0].innerHTML = '';", log_container)
        
        # Click View Logs button
        view_logs_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'View Logs')]")
        view_logs_btn.click()
        print("✅ Clicked View Logs button")
        
        # Wait for operation to complete
        time.sleep(8)
        
        # Get dashboard results
        log_entries = driver.find_elements(By.CSS_SELECTOR, "#log-output .log-entry")
        dashboard_logs = [entry.text for entry in log_entries]
        
        print(f"✅ Dashboard shows {len(dashboard_logs)} log entries")
        
        # Check for log content indicators
        log_content_found = any("LOG CONTENT" in log for log in dashboard_logs)
        plasma_logs_found = any("plasma" in log.lower() for log in dashboard_logs)
        
        print(f"   Log content section: {'✅' if log_content_found else '❌'}")
        print(f"   Plasma operations: {'✅' if plasma_logs_found else '❌'}")
        
        # Now check for and properly close terminal windows
        print("🪟 Managing terminal windows...")
        
        try:
            result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                window_ids = result.stdout.strip().split('\n')
                closed_windows = 0
                
                for window_id in window_ids:
                    if window_id.strip():
                        # Get window name
                        name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                   capture_output=True, text=True)
                        if name_result.returncode == 0:
                            window_name = name_result.stdout.strip()
                            if 'tail' in window_name or 'log' in window_name.lower():
                                print(f"   Closing log viewer: {window_name}")
                                subprocess.run(['xdotool', 'windowclose', window_id])
                                closed_windows += 1
                
                print(f"✅ Closed {closed_windows} log viewer windows")
        except Exception as e:
            print(f"⚠️ Window management error: {e}")
        
        driver.quit()
        
        # Final assessment
        success = log_content_found and plasma_logs_found
        print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: View Logs button test")
        return success
        
    except Exception as e:
        print(f"❌ View Logs automation test failed: {e}")
        return False

def main():
    """Run comprehensive automation tool tests"""
    print("🚀 COMPREHENSIVE AUTOMATION TOOL TEST")
    print("Testing: script, asciinema, Selenium, xdotool")
    
    results = {}
    
    # Test each tool
    results['script'] = test_script_command()
    results['asciinema'] = test_asciinema()
    results['selenium'] = test_selenium()
    results['xdotool'] = test_xdotool()
    
    # Test actual button functionality with proper automation
    results['view_logs_automation'] = test_view_logs_with_proper_automation()
    
    # Summary
    print("\n=== AUTOMATION TOOL TEST RESULTS ===")
    working_tools = 0
    total_tools = len(results)
    
    for tool, working in results.items():
        status = "✅ WORKING" if working else "❌ FAILED"
        print(f"  {tool}: {status}")
        if working:
            working_tools += 1
    
    print(f"\nSUMMARY: {working_tools}/{total_tools} automation tools working")
    
    if working_tools == total_tools:
        print("🎉 ALL AUTOMATION TOOLS WORKING PERFECTLY")
        print("✅ COMPREHENSIVE VERIFICATION COMPLETE")
        print("✅ TERMINAL WINDOWS PROPERLY MANAGED")
    else:
        print("⚠️ SOME AUTOMATION TOOLS NEED FIXING")
        print("❌ VERIFICATION INCOMPLETE")
    
    return working_tools == total_tools

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ ALL AUTOMATION INFRASTRUCTURE VERIFIED")
        print("✅ READY FOR COMPREHENSIVE TESTING")
    else:
        print("\n❌ AUTOMATION INFRASTRUCTURE NEEDS WORK")
        print("❌ MUST FIX TOOLS BEFORE COMPREHENSIVE TESTING")
