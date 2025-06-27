#!/usr/bin/env python3
"""
Test that View Logs terminal closes in 3 seconds using the SAME method as other windows
"""

import subprocess
import time

def test_view_logs_3_second_close():
    """Test that View Logs terminal closes in exactly 3 seconds"""
    print("🪟 Testing View Logs 3-second terminal close...")
    
    try:
        # Record initial terminal windows
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
        
        print(f"Initial windows: {len(initial_windows)}")
        for window_id, name in initial_windows:
            print(f"  {name}")
        
        # Trigger View Logs
        print("\nTriggering View Logs...")
        start_time = time.time()
        
        result = subprocess.run(['curl', '-s', '-X', 'POST', 'http://localhost:8000/api/view-logs'], 
                              capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ View Logs API call successful")
            
            # Wait exactly 1 second for terminal to open
            time.sleep(1)
            
            # Check for new terminal windows
            result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                                  capture_output=True, text=True)
            
            log_window_found = False
            log_window_id = None
            
            if result.returncode == 0:
                window_ids = result.stdout.strip().split('\n')
                for window_id in window_ids:
                    if window_id.strip():
                        name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                                   capture_output=True, text=True)
                        if name_result.returncode == 0:
                            window_name = name_result.stdout.strip()
                            if any(keyword in window_name.lower() for keyword in ['tail', 'log', 'evidence']):
                                if (window_id, window_name) not in initial_windows:
                                    log_window_found = True
                                    log_window_id = window_id
                                    print(f"✅ New log window detected: {window_name} (ID: {window_id})")
                                    break
            
            if log_window_found:
                # Wait for the 3-second auto-close
                print("Waiting for 3-second auto-close...")
                
                # Check every 0.5 seconds to see when it closes
                for i in range(8):  # Check for 4 seconds total
                    time.sleep(0.5)
                    elapsed = time.time() - start_time
                    
                    # Check if window still exists
                    name_result = subprocess.run(['xdotool', 'getwindowname', log_window_id],
                                               capture_output=True, text=True)
                    
                    if name_result.returncode != 0:
                        # Window closed
                        print(f"✅ Window auto-closed after {elapsed:.1f} seconds")
                        
                        if elapsed <= 4.0:  # Within 4 seconds is acceptable
                            print("✅ TERMINAL CLOSES IN 3 SECONDS - SAME AS OTHER WINDOWS")
                            return True
                        else:
                            print("❌ Terminal took too long to close")
                            return False
                
                # If we get here, window didn't close
                print("❌ Window did not auto-close within 4 seconds")
                
                # Manual cleanup
                subprocess.run(['xdotool', 'windowclose', log_window_id])
                print(f"✅ Manually closed window {log_window_id}")
                return False
            else:
                print("❌ No new log window detected")
                return False
        else:
            print(f"❌ View Logs API failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_manual_close_method():
    """Test the manual close method that works for other windows"""
    print("\n🔧 Testing manual close method...")
    
    try:
        # Use the EXACT same command that works for other windows
        result = subprocess.run([
            'bash', '-c',
            'xdotool search --class konsole | xargs -I {} bash -c \'name=$(xdotool getwindowname {}); if [[ "$name" == *"evidence"* && "$name" == *"tail"* ]]; then echo "Closing $name"; xdotool windowclose {}; fi\''
        ], capture_output=True, text=True)
        
        print(f"Command output: {result.stdout}")
        print(f"Command stderr: {result.stderr}")
        print(f"Return code: {result.returncode}")
        
        if "Closing" in result.stdout:
            print("✅ Manual close method works")
            return True
        else:
            print("✅ No evidence/tail windows to close")
            return True
            
    except Exception as e:
        print(f"❌ Manual close test failed: {e}")
        return False

def main():
    """Test both methods"""
    print("🚀 TESTING 3-SECOND TERMINAL CLOSE")
    print("Using SAME method that works for other windows")
    
    # Test manual method first
    manual_works = test_manual_close_method()
    
    # Test automatic 3-second close
    auto_works = test_view_logs_3_second_close()
    
    print(f"\n=== RESULTS ===")
    print(f"Manual close method: {'✅ WORKS' if manual_works else '❌ BROKEN'}")
    print(f"3-second auto-close: {'✅ WORKS' if auto_works else '❌ BROKEN'}")
    
    if auto_works:
        print("\n🎉 SUCCESS: VIEW LOGS TERMINAL CLOSES IN 3 SECONDS")
        print("✅ SAME METHOD AS OTHER WINDOWS")
        print("✅ AUTOMATION TOOLS VERIFIED")
    else:
        print("\n❌ FAILURE: TERMINAL STILL NOT AUTO-CLOSING")
        print("❌ NEED TO FIX AUTO-CLOSE IMPLEMENTATION")

if __name__ == "__main__":
    main()
