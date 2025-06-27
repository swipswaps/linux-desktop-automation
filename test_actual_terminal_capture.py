#!/usr/bin/env python3
"""
Test if dashboard now shows actual terminal output instead of fake results
"""

import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_actual_terminal_capture():
    """Test if dashboard captures and displays actual terminal session"""
    print("=== TESTING ACTUAL TERMINAL CAPTURE ===")
    
    # Clear any existing terminal session files
    for file_path in ['/tmp/terminal_session.txt', '/tmp/cache_clear_results.txt']:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Cleared existing file: {file_path}")
    
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
        
        # Click Clear Cache
        clear_cache_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear Cache')]")
        clear_cache_btn.click()
        print("✅ Clear Cache button clicked")
        
        # Wait for terminal to open and user to interact
        print("Waiting for terminal session to complete...")
        time.sleep(25)  # Wait for user to complete sudo and terminal to finish
        
        # Check if terminal session was captured
        session_file = '/tmp/terminal_session.txt'
        output_file = '/tmp/cache_clear_results.txt'
        
        print(f"\nChecking terminal capture files:")
        print(f"  Session file exists: {os.path.exists(session_file)}")
        print(f"  Output file exists: {os.path.exists(output_file)}")
        
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                session_content = f.read()
                print(f"  Session file size: {len(session_content)} characters")
                if session_content:
                    print(f"  Session preview: {session_content[:200]}...")
        
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                output_content = f.read()
                print(f"  Output file size: {len(output_content)} characters")
                if output_content:
                    print(f"  Output preview: {output_content[:200]}...")
        
        # Get dashboard logs
        log_entries = driver.find_elements(By.CSS_SELECTOR, "#log-output .log-entry")
        all_logs = [entry.text for entry in log_entries]
        
        print(f"\nDashboard shows {len(all_logs)} log entries")
        
        # Look for actual terminal session capture
        terminal_session_indicators = [
            'ACTUAL TERMINAL SESSION CAPTURE',
            'VERBATIM TERMINAL OUTPUT',
            'TERMINAL OUTPUT FILE BACKUP',
            'terminal session'
        ]
        
        found_session_capture = False
        for indicator in terminal_session_indicators:
            matching_logs = [log for log in all_logs if indicator in log]
            if matching_logs:
                print(f"✅ Found '{indicator}' in {len(matching_logs)} entries:")
                for log in matching_logs[:2]:
                    print(f"   {log}")
                found_session_capture = True
        
        # Look for the actual terminal content (not fake generated numbers)
        actual_terminal_content = False
        for log in all_logs:
            # Look for signs of actual terminal output vs generated fake results
            if any(phrase in log for phrase in [
                'KDE Memory Guardian System Cache Clearing',
                'Getting memory info before clearing',
                'Step 1: Sync filesystem',
                'Step 2: SYSTEM CACHE CLEARING',
                '[sudo] password for owner:'
            ]):
                print(f"✅ Found actual terminal content: {log}")
                actual_terminal_content = True
                break
        
        # Check for fake vs real indicators
        fake_indicators = [
            'Generated fake numbers',
            'Simulated results',
            'Mock data'
        ]
        
        has_fake_content = any(any(fake in log for fake in fake_indicators) for log in all_logs)
        
        print(f"\nTerminal capture analysis:")
        print(f"  Session capture found: {'✅' if found_session_capture else '❌'}")
        print(f"  Actual terminal content: {'✅' if actual_terminal_content else '❌'}")
        print(f"  Fake content detected: {'❌' if has_fake_content else '✅ None detected'}")
        
        # Show recent logs for verification
        print(f"\nRecent dashboard logs:")
        for i, log in enumerate(all_logs[-10:], 1):
            print(f"  {i}. {log}")
        
        # Final assessment
        if found_session_capture and actual_terminal_content and not has_fake_content:
            print("\n✅ SUCCESS: Dashboard shows actual terminal session capture")
            print("✅ Real terminal output displayed instead of fake results")
            success = True
        else:
            print("\n❌ FAILURE: Dashboard still showing fake or missing terminal output")
            print("❌ Not capturing actual terminal session")
            success = False
        
        driver.quit()
        return success
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def verify_terminal_files():
    """Check what's actually in the terminal capture files"""
    print("\n=== TERMINAL FILE VERIFICATION ===")
    
    session_file = '/tmp/terminal_session.txt'
    output_file = '/tmp/cache_clear_results.txt'
    
    for file_path, name in [(session_file, 'Session'), (output_file, 'Output')]:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    print(f"\n{name} file ({len(content)} chars):")
                    print(f"  Contains 'MEMORY FREED:': {'✅' if 'MEMORY FREED:' in content else '❌'}")
                    print(f"  Contains 'sudo password': {'✅' if 'sudo' in content and 'password' in content else '❌'}")
                    print(f"  Contains actual numbers: {'✅' if 'MB' in content and '→' in content else '❌'}")
                    
                    # Show key lines
                    lines = content.split('\n')
                    key_lines = [line for line in lines if any(keyword in line for keyword in [
                        'MEMORY FREED:', 'CACHE FREED:', 'Memory used:', 'Cache/Buffer:', 'sudo'
                    ])]
                    
                    if key_lines:
                        print(f"  Key lines found:")
                        for line in key_lines[:5]:
                            print(f"    {line.strip()}")
                    else:
                        print(f"  No key result lines found")
                        
            except Exception as e:
                print(f"  Error reading {name} file: {e}")
        else:
            print(f"\n{name} file: ❌ Does not exist")

if __name__ == "__main__":
    print("=== TESTING ACTUAL TERMINAL CAPTURE VS FAKE RESULTS ===")
    
    # Test the dashboard
    dashboard_success = test_actual_terminal_capture()
    
    # Verify the files
    verify_terminal_files()
    
    print(f"\n=== FINAL ASSESSMENT ===")
    if dashboard_success:
        print("✅ DASHBOARD NOW SHOWS ACTUAL TERMINAL OUTPUT")
        print("✅ NO MORE FAKE GENERATED RESULTS")
        print("✅ REAL TERMINAL SESSION CAPTURED AND DISPLAYED")
    else:
        print("❌ DASHBOARD STILL BROKEN")
        print("❌ STILL SHOWING FAKE RESULTS OR MISSING TERMINAL OUTPUT")
        print("❌ TERMINAL SESSION CAPTURE NOT WORKING")
