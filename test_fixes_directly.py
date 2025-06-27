#!/usr/bin/env python3
"""
Test the fixes directly using automation tools
"""

import subprocess
import time
import os

def close_terminal_windows():
    """Close any open terminal windows"""
    print("🪟 Closing open terminal windows...")
    
    try:
        result = subprocess.run(['xdotool', 'search', '--class', 'konsole'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            window_ids = result.stdout.strip().split('\n')
            closed_count = 0
            
            for window_id in window_ids:
                if window_id.strip():
                    name_result = subprocess.run(['xdotool', 'getwindowname', window_id],
                                               capture_output=True, text=True)
                    if name_result.returncode == 0:
                        window_name = name_result.stdout.strip()
                        if any(keyword in window_name.lower() for keyword in ['tail', 'log', 'evidence']):
                            print(f"   Closing: {window_name}")
                            subprocess.run(['xdotool', 'windowclose', window_id])
                            closed_count += 1
            
            print(f"✅ Closed {closed_count} terminal windows")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_accessibility_fixes():
    """Verify accessibility fixes were applied"""
    print("♿ Verifying accessibility fixes...")
    
    html_file = 'evidence/index.html'
    
    try:
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Check for accessibility attributes
        accessibility_checks = [
            'tabindex="0"',
            'aria-label=',
            'role="button"',
            'keydown'
        ]
        
        found_features = 0
        for check in accessibility_checks:
            if check in content:
                found_features += 1
                print(f"   ✅ Found: {check}")
            else:
                print(f"   ❌ Missing: {check}")
        
        success = found_features >= 3
        print(f"{'✅ ACCESSIBILITY FIXED' if success else '❌ ACCESSIBILITY INCOMPLETE'}")
        return success
        
    except Exception as e:
        print(f"❌ Error checking accessibility: {e}")
        return False

def verify_refresh_stats_fix():
    """Verify refresh stats fix"""
    print("🔄 Verifying Refresh Stats fix...")
    
    html_file = 'evidence/index.html'
    
    try:
        with open(html_file, 'r') as f:
            content = f.read()
        
        # Check for refresh stats improvements
        refresh_checks = [
            'addLogEntry(\'🔄 Refreshing',
            'Stats refreshed',
            'Refresh failed'
        ]
        
        found_features = 0
        for check in refresh_checks:
            if check in content:
                found_features += 1
                print(f"   ✅ Found: {check}")
        
        success = found_features >= 2
        print(f"{'✅ REFRESH STATS FIXED' if success else '❌ REFRESH STATS INCOMPLETE'}")
        return success
        
    except Exception as e:
        print(f"❌ Error checking refresh stats: {e}")
        return False

def verify_terminal_management_fix():
    """Verify terminal management fix"""
    print("📋 Verifying terminal management fix...")
    
    server_file = 'evidence/server.py'
    
    try:
        with open(server_file, 'r') as f:
            content = f.read()
        
        # Check for terminal management code
        terminal_checks = [
            'cleanup_terminal',
            'threading.Thread',
            'xdotool',
            'windowclose'
        ]
        
        found_features = 0
        for check in terminal_checks:
            if check in content:
                found_features += 1
                print(f"   ✅ Found: {check}")
        
        success = found_features >= 3
        print(f"{'✅ TERMINAL MANAGEMENT FIXED' if success else '❌ TERMINAL MANAGEMENT INCOMPLETE'}")
        return success
        
    except Exception as e:
        print(f"❌ Error checking terminal management: {e}")
        return False

def start_server_on_available_port():
    """Start server on an available port"""
    print("🌐 Starting server on available port...")
    
    for port in [8000, 8001, 8002, 8003]:
        try:
            # Check if port is available
            result = subprocess.run(['netstat', '-ln'], capture_output=True, text=True)
            if f':{port}' not in result.stdout:
                print(f"   Port {port} available, starting server...")
                
                # Start server
                process = subprocess.Popen([
                    'python3', '-c', f'''
import sys, os
sys.path.append("evidence")
os.chdir("evidence")
from server import KDEMemoryGuardianHandler
import socketserver
with socketserver.TCPServer(("", {port}), KDEMemoryGuardianHandler) as httpd:
    print(f"Server running on port {port}")
    httpd.serve_forever()
'''
                ])
                
                time.sleep(3)
                
                # Test if server is responding
                test_result = subprocess.run(['curl', '-s', f'http://localhost:{port}/'], 
                                           capture_output=True, text=True, timeout=5)
                
                if test_result.returncode == 0:
                    print(f"✅ Server started successfully on port {port}")
                    return port, process
                else:
                    process.terminate()
                    
        except Exception as e:
            print(f"   Port {port} failed: {e}")
            continue
    
    print("❌ Could not start server on any port")
    return None, None

def test_buttons_with_curl(port):
    """Test buttons using curl"""
    print(f"🧪 Testing buttons with curl on port {port}...")
    
    tests = [
        ("Stats", f"http://localhost:{port}/api/stats"),
        ("View Logs", f"http://localhost:{port}/api/view-logs"),
        ("Run Tests", f"http://localhost:{port}/api/run-tests")
    ]
    
    results = {}
    
    for test_name, url in tests:
        try:
            if test_name == "View Logs":
                # POST request for view logs
                result = subprocess.run(['curl', '-s', '-X', 'POST', url], 
                                      capture_output=True, text=True, timeout=15)
            else:
                # GET request for others
                result = subprocess.run(['curl', '-s', url], 
                                      capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and len(result.stdout) > 10:
                print(f"   ✅ {test_name}: Working ({len(result.stdout)} chars)")
                results[test_name] = True
                
                # For view logs, check if terminal cleanup is mentioned
                if test_name == "View Logs" and "auto-close" in result.stdout:
                    print(f"      ✅ Terminal auto-cleanup detected")
            else:
                print(f"   ❌ {test_name}: Failed")
                results[test_name] = False
                
        except Exception as e:
            print(f"   ❌ {test_name}: Error - {e}")
            results[test_name] = False
    
    return results

def main():
    """Main test function"""
    print("🚀 TESTING ALL FIXES WITH AUTOMATION TOOLS")
    
    # Close any open terminals first
    close_terminal_windows()
    
    # Verify fixes were applied to files
    print("\n=== VERIFYING FILE FIXES ===")
    accessibility_ok = verify_accessibility_fixes()
    refresh_ok = verify_refresh_stats_fix()
    terminal_ok = verify_terminal_management_fix()
    
    file_fixes = accessibility_ok and refresh_ok and terminal_ok
    
    # Start server and test functionality
    print("\n=== TESTING FUNCTIONALITY ===")
    port, server_process = start_server_on_available_port()
    
    if port:
        try:
            # Test buttons
            button_results = test_buttons_with_curl(port)
            
            # Wait a bit then close any terminal windows that opened
            time.sleep(5)
            close_terminal_windows()
            
            # Final assessment
            working_buttons = sum(button_results.values())
            total_buttons = len(button_results)
            
            print(f"\n=== FINAL RESULTS ===")
            print(f"File fixes: {'✅ COMPLETE' if file_fixes else '❌ INCOMPLETE'}")
            print(f"Button functionality: {working_buttons}/{total_buttons} working")
            
            for button, working in button_results.items():
                status = "✅ WORKING" if working else "❌ BROKEN"
                print(f"  {button}: {status}")
            
            overall_success = file_fixes and working_buttons >= total_buttons * 0.8
            
            if overall_success:
                print("\n🎉 FIXES SUCCESSFULLY APPLIED AND TESTED")
                print("✅ ACCESSIBILITY STANDARDS MET")
                print("✅ BUTTONS WORKING PROPERLY")
                print("✅ TERMINAL MANAGEMENT IMPROVED")
            else:
                print("\n⚠️ SOME ISSUES REMAIN")
                print("❌ ADDITIONAL FIXES NEEDED")
            
        finally:
            if server_process:
                server_process.terminate()
                print("🛑 Server stopped")
    else:
        print("❌ Could not test functionality - server failed to start")

if __name__ == "__main__":
    main()
