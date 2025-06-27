#!/usr/bin/env python3
"""
Test View Logs terminal opening and auto-closing in real time
"""

import subprocess
import time
import threading

def monitor_terminals():
    """Monitor terminal windows in real time"""
    print("🔍 Starting terminal monitoring...")
    
    for i in range(20):  # Monitor for 10 seconds
        try:
            result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                                  capture_output=True, text=True)
            
            current_time = time.time()
            windows = []
            
            if result.returncode == 0:
                window_ids = result.stdout.strip().split('\n')
                for window_id in window_ids:
                    if window_id.strip():
                        name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                   capture_output=True, text=True)
                        if name_result.returncode == 0:
                            window_name = name_result.stdout.strip()
                            windows.append((window_id, window_name))
            
            # Look for log/tail/evidence windows
            log_windows = []
            for window_id, name in windows:
                if any(keyword in name.lower() for keyword in ['tail', 'log', 'evidence']):
                    log_windows.append((window_id, name))
            
            if log_windows:
                print(f"[{i*0.5:.1f}s] 🪟 Found {len(log_windows)} log windows:")
                for window_id, name in log_windows:
                    print(f"       {name} (ID: {window_id})")
            else:
                print(f"[{i*0.5:.1f}s] ✅ No log windows")
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"[{i*0.5:.1f}s] ❌ Error: {e}")
            time.sleep(0.5)

def test_view_logs_with_monitoring():
    """Test View Logs while monitoring terminals"""
    print("🚀 Testing View Logs with real-time terminal monitoring")
    
    # Start monitoring in background
    monitor_thread = threading.Thread(target=monitor_terminals)
    monitor_thread.daemon = True
    monitor_thread.start()
    
    # Wait a moment for monitoring to start
    time.sleep(1)
    
    print("\n📋 Triggering View Logs...")
    
    try:
        result = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/view-logs'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ View Logs API successful")
            print(f"Response length: {len(result.stdout)} characters")
            
            # Check if response mentions auto-close
            if "auto-close" in result.stdout:
                print("✅ Response mentions auto-close")
            else:
                print("❌ No auto-close mentioned in response")
        else:
            print(f"❌ View Logs API failed: {result.stderr}")
        
        # Let monitoring continue for a bit
        time.sleep(8)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_view_logs_with_monitoring()
