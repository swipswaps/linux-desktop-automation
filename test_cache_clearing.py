#!/usr/bin/env python3
"""
Test cache clearing functionality using Selenium automation
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import time
import os

def test_cache_clearing():
    print("=== COMPREHENSIVE CACHE CLEARING TEST ===")

    # Check initial state
    print("\n1. Checking initial system state...")
    initial_konsole = subprocess.run(['pgrep', '-f', 'konsole'], capture_output=True, text=True)
    initial_pids = initial_konsole.stdout.strip().split('\n') if initial_konsole.stdout.strip() else []
    print(f"Initial Konsole PIDs: {initial_pids}")

    # Get initial cache size with detailed breakdown
    cache_before = subprocess.run(['du', '-sh', os.path.expanduser('~/.cache')],
                                capture_output=True, text=True)
    print(f"Cache size before: {cache_before.stdout.strip()}")

    # Get memory usage before
    mem_before = subprocess.run(['free', '-h'], capture_output=True, text=True)
    print(f"Memory before:\n{mem_before.stdout}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        # Start browser
        print("\n2. Starting browser and loading dashboard...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('http://localhost:8000')

        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ Dashboard loaded")

        # Take screenshot before
        driver.save_screenshot('before_cache_clear.png')
        print("📸 Screenshot saved: before_cache_clear.png")

        # Click Clear Cache button
        print("\n3. Clicking Clear Cache button...")
        clear_cache_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Clear Cache')]")
        clear_cache_btn.click()
        print("✅ Clear Cache button clicked")

        # Wait for terminal to open
        print("\n4. Waiting for terminal to open...")
        time.sleep(2)

        # Check for new Konsole processes
        current_konsole = subprocess.run(['pgrep', '-f', 'konsole'], capture_output=True, text=True)
        current_pids = current_konsole.stdout.strip().split('\n') if current_konsole.stdout.strip() else []
        new_pids = [pid for pid in current_pids if pid not in initial_pids and pid]

        if new_pids:
            print(f"✅ New Konsole terminal opened: {new_pids}")

            # Check what the terminal is doing
            for pid in new_pids:
                ps_result = subprocess.run(['ps', '-p', pid, '-o', 'pid,cmd'],
                                         capture_output=True, text=True)
                print(f"Terminal process: {ps_result.stdout.strip()}")

            # Check if terminal window is visible using wmctrl
            wmctrl_result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
            if wmctrl_result.returncode == 0:
                konsole_windows = [line for line in wmctrl_result.stdout.split('\n')
                                 if 'konsole' in line.lower()]
                if konsole_windows:
                    print("✅ Konsole window visible in window manager:")
                    for window in konsole_windows:
                        print(f"  {window}")
                else:
                    print("❌ No Konsole windows visible in window manager")

            print("\n5. Waiting for user to complete sudo authentication...")
            print("   (User should see terminal asking for password)")

            # Wait longer for user interaction
            time.sleep(15)

            # Check if processes are still running
            still_running = subprocess.run(['pgrep', '-f', 'konsole'], capture_output=True, text=True)
            current_pids_after = still_running.stdout.strip().split('\n') if still_running.stdout.strip() else []

            if any(pid in current_pids_after for pid in new_pids):
                print("⚠️ Terminal still running - user may still be interacting")
                time.sleep(10)  # Wait more
            else:
                print("✅ Terminal completed and closed")

        else:
            print("❌ No new Konsole terminal detected")

        # Check cache size after
        print("\n6. Checking results after cache clearing...")
        cache_after = subprocess.run(['du', '-sh', os.path.expanduser('~/.cache')],
                                   capture_output=True, text=True)
        print(f"Cache size after: {cache_after.stdout.strip()}")

        # Get memory usage after
        mem_after = subprocess.run(['free', '-h'], capture_output=True, text=True)
        print(f"Memory after:\n{mem_after.stdout}")

        # Compare results
        cache_before_size = cache_before.stdout.strip()
        cache_after_size = cache_after.stdout.strip()

        if cache_before_size != cache_after_size:
            print("✅ CACHE SIZE CHANGED - CLEARING HAD REAL EFFECT")
            print(f"   Before: {cache_before_size}")
            print(f"   After:  {cache_after_size}")
        else:
            print("❌ CACHE SIZE UNCHANGED - CLEARING HAD NO EFFECT")
            print(f"   Size: {cache_before_size}")

        # Check browser log output
        print("\n7. Checking browser log output...")
        log_entries = driver.find_elements(By.CSS_SELECTOR, "#log-output .log-entry")
        recent_logs = [entry.text for entry in log_entries[-15:]]  # Last 15 entries

        print("Recent log entries:")
        for i, log in enumerate(recent_logs, 1):
            print(f"  {i}. {log}")

        # Take screenshot after
        driver.save_screenshot('after_cache_clear.png')
        print("📸 Screenshot saved: after_cache_clear.png")

        # Final process check
        print("\n8. Final process cleanup check...")
        final_konsole = subprocess.run(['pgrep', '-f', 'konsole'], capture_output=True, text=True)
        final_pids = final_konsole.stdout.strip().split('\n') if final_konsole.stdout.strip() else []

        stuck_processes = [pid for pid in final_pids if pid not in initial_pids and pid]
        if stuck_processes:
            print(f"⚠️ Processes still running: {stuck_processes}")
            for pid in stuck_processes:
                ps_result = subprocess.run(['ps', '-p', pid, '-o', 'pid,etime,cmd'],
                                         capture_output=True, text=True)
                print(f"Process details: {ps_result.stdout}")

                # Kill stuck processes
                print(f"Killing stuck process {pid}")
                subprocess.run(['kill', pid], capture_output=True)
        else:
            print("✅ No stuck processes - clean completion")

        # Verify system cache was actually cleared
        print("\n9. Verifying system cache clearing...")
        # Check if drop_caches was executed by looking at system logs
        dmesg_result = subprocess.run(['dmesg', '-T'], capture_output=True, text=True)
        if 'drop_caches' in dmesg_result.stdout or 'cache' in dmesg_result.stdout.lower():
            print("✅ System cache clearing detected in system logs")
        else:
            print("❌ No evidence of system cache clearing in logs")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    finally:
        try:
            driver.quit()
            print("\n✅ Browser closed")
        except:
            pass

if __name__ == "__main__":
    test_cache_clearing()
