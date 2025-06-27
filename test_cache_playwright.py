#!/usr/bin/env python3
"""
Test cache clearing with Playwright automation including terminal interaction
"""

from playwright.sync_api import sync_playwright
import subprocess
import time
import os

def test_cache_clearing_with_interaction():
    print("=== PLAYWRIGHT CACHE CLEARING TEST WITH TERMINAL INTERACTION ===")
    
    # Check initial state
    print("\n1. Checking initial system state...")
    cache_before = subprocess.run(['du', '-sh', os.path.expanduser('~/.cache')], 
                                capture_output=True, text=True)
    print(f"Cache size before: {cache_before.stdout.strip()}")
    
    with sync_playwright() as p:
        try:
            # Launch browser
            print("\n2. Starting browser...")
            browser = p.chromium.launch(headless=False)  # Visible browser
            page = browser.new_page()
            
            # Navigate to dashboard
            page.goto('http://localhost:8000')
            page.wait_for_load_state('networkidle')
            print("✅ Dashboard loaded")
            
            # Take screenshot before
            page.screenshot(path='playwright_before.png')
            print("📸 Screenshot saved: playwright_before.png")
            
            # Click Clear Cache button
            print("\n3. Clicking Clear Cache button...")
            clear_cache_btn = page.locator("button:has-text('Clear Cache')")
            clear_cache_btn.click()
            print("✅ Clear Cache button clicked")
            
            # Wait for terminal to open
            time.sleep(3)
            
            # Check for new Konsole processes
            konsole_check = subprocess.run(['pgrep', '-f', 'kde_cache_clear'], 
                                         capture_output=True, text=True)
            if konsole_check.stdout.strip():
                print(f"✅ Cache clearing terminal detected: {konsole_check.stdout.strip()}")
                
                # Use xdotool to interact with the terminal
                print("\n4. Attempting to interact with terminal using xdotool...")
                
                # Find the terminal window
                window_search = subprocess.run(['xdotool', 'search', '--name', 'kde_cache_clear'], 
                                             capture_output=True, text=True)
                if window_search.stdout.strip():
                    window_id = window_search.stdout.strip().split('\n')[0]
                    print(f"✅ Found terminal window: {window_id}")
                    
                    # Focus the window
                    subprocess.run(['xdotool', 'windowactivate', window_id])
                    time.sleep(1)
                    
                    # Type a fake password (this will fail but we can see the interaction)
                    print("Sending password to terminal...")
                    subprocess.run(['xdotool', 'type', 'testpassword'])
                    time.sleep(1)
                    subprocess.run(['xdotool', 'key', 'Return'])
                    
                    # Wait for command to complete
                    time.sleep(5)
                    
                    # Press Enter to close terminal
                    subprocess.run(['xdotool', 'key', 'Return'])
                    time.sleep(2)
                    
                else:
                    print("❌ Could not find terminal window with xdotool")
            else:
                print("❌ No cache clearing terminal detected")
            
            # Wait for operation to complete
            print("\n5. Waiting for operation to complete...")
            time.sleep(5)
            
            # Check cache size after
            cache_after = subprocess.run(['du', '-sh', os.path.expanduser('~/.cache')], 
                                       capture_output=True, text=True)
            print(f"Cache size after: {cache_after.stdout.strip()}")
            
            # Compare results
            if cache_before.stdout != cache_after.stdout:
                print("✅ CACHE SIZE CHANGED - CLEARING HAD REAL EFFECT")
                print(f"   Before: {cache_before.stdout.strip()}")
                print(f"   After:  {cache_after.stdout.strip()}")
            else:
                print("❌ CACHE SIZE UNCHANGED - CLEARING HAD NO EFFECT")
            
            # Check browser log output
            print("\n6. Checking browser log output...")
            log_entries = page.locator("#log-output .log-entry").all()
            recent_logs = [entry.text_content() for entry in log_entries[-10:]]
            
            print("Recent log entries:")
            for i, log in enumerate(recent_logs, 1):
                if log and log.strip():
                    print(f"  {i}. {log}")
            
            # Take screenshot after
            page.screenshot(path='playwright_after.png')
            print("📸 Screenshot saved: playwright_after.png")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            try:
                browser.close()
                print("\n✅ Browser closed")
            except:
                pass

def test_direct_cache_clearing():
    """Test cache clearing directly without web interface"""
    print("\n=== DIRECT CACHE CLEARING TEST ===")
    
    # Check initial cache size
    cache_before = subprocess.run(['du', '-sb', os.path.expanduser('~/.cache')], 
                                capture_output=True, text=True)
    cache_before_bytes = int(cache_before.stdout.split()[0]) if cache_before.returncode == 0 else 0
    print(f"Cache size before: {cache_before_bytes} bytes")
    
    # Clear specific cache files that we can clear without sudo
    cache_items_cleared = 0
    total_bytes_freed = 0
    
    cache_targets = [
        os.path.expanduser('~/.cache/thumbnails'),
        os.path.expanduser('~/.cache/fontconfig'),
        os.path.expanduser('~/.cache/icon-cache.kcache'),
    ]
    
    for target in cache_targets:
        if os.path.exists(target):
            try:
                if os.path.isfile(target):
                    size = os.path.getsize(target)
                    os.remove(target)
                    print(f"✅ Removed file: {os.path.basename(target)} ({size} bytes)")
                    cache_items_cleared += 1
                    total_bytes_freed += size
                elif os.path.isdir(target):
                    import shutil
                    size_result = subprocess.run(['du', '-sb', target], capture_output=True, text=True)
                    size = int(size_result.stdout.split()[0]) if size_result.returncode == 0 else 0
                    shutil.rmtree(target)
                    print(f"✅ Removed directory: {os.path.basename(target)} ({size} bytes)")
                    cache_items_cleared += 1
                    total_bytes_freed += size
            except Exception as e:
                print(f"❌ Failed to remove {target}: {e}")
    
    # Clear ksycoca files
    ksycoca_pattern = os.path.expanduser('~/.cache/ksycoca*')
    import glob
    for ksycoca_file in glob.glob(ksycoca_pattern):
        try:
            size = os.path.getsize(ksycoca_file)
            os.remove(ksycoca_file)
            print(f"✅ Removed ksycoca: {os.path.basename(ksycoca_file)} ({size} bytes)")
            cache_items_cleared += 1
            total_bytes_freed += size
        except Exception as e:
            print(f"❌ Failed to remove {ksycoca_file}: {e}")
    
    # Check cache size after
    cache_after = subprocess.run(['du', '-sb', os.path.expanduser('~/.cache')], 
                                capture_output=True, text=True)
    cache_after_bytes = int(cache_after.stdout.split()[0]) if cache_after.returncode == 0 else 0
    
    actual_freed = cache_before_bytes - cache_after_bytes
    
    print(f"\nResults:")
    print(f"  Items cleared: {cache_items_cleared}")
    print(f"  Expected bytes freed: {total_bytes_freed}")
    print(f"  Actual bytes freed: {actual_freed}")
    print(f"  Cache before: {cache_before_bytes} bytes")
    print(f"  Cache after: {cache_after_bytes} bytes")
    
    if actual_freed > 0:
        print("✅ CACHE CLEARING SUCCESSFUL - REAL EFFECT MEASURED")
    else:
        print("❌ CACHE CLEARING HAD NO MEASURABLE EFFECT")

if __name__ == "__main__":
    test_cache_clearing_with_interaction()
    test_direct_cache_clearing()
