# 🧪 Linux Desktop Automation

🚀 **Comprehensive Selenium and Playwright testing framework** for Linux desktop environments - Professional automation tools for web interfaces, system testing, and desktop application verification.

## ✨ Features

### **🔧 Multi-Framework Support**
- **Selenium WebDriver** for robust web automation
- **Playwright** for modern browser testing
- **Cross-browser compatibility** (Chrome, Firefox, Edge)
- **Headless and GUI modes** for different testing scenarios

### **🖥️ Desktop Integration Testing**
- **KDE Plasma** interface automation
- **System cache management** testing
- **Terminal window automation** and verification
- **Accessibility compliance** testing (text selectability, button interactions)

### **📊 Evidence Collection**
- **Screenshot capture** with timestamps
- **JSON test reports** with detailed results
- **Performance metrics** and timing analysis
- **Before/after comparison** documentation

### **🛠️ System Testing Tools**
- **Cache clearing verification** with visual evidence
- **Button functionality testing** across web interfaces
- **Terminal capture and automation** with real system integration
- **Memory management testing** for desktop applications

## 📁 Repository Structure

```
linux-desktop-automation/
├── selenium_tests/
│   ├── test_cache_clearing.py         # Cache management testing
│   ├── test_all_buttons_fixed.py      # UI component verification
│   ├── test_automation_tools.py       # Tool validation framework
│   └── test_text_selectability.py     # Accessibility testing
├── playwright_tests/
│   ├── test_cache_playwright.py       # Playwright cache testing
│   └── comprehensive_browser_tests.py # Cross-browser validation
├── terminal_automation/
│   ├── test_actual_terminal_capture.py    # Real terminal integration
│   ├── test_fixed_terminal_capture.py     # Terminal window management
│   └── test_3_second_terminal_close.py    # Automated cleanup testing
├── frameworks/
│   ├── actual_automation_fix.py           # Core automation framework
│   ├── comprehensive_automation_fix.py    # Advanced testing tools
│   └── final_automation_verification.py   # Verification framework
├── evidence/                              # Screenshots and test results
│   ├── *.png                             # Visual evidence files
│   ├── *.json                            # Test result reports
│   └── REAL_USER_INTERACTION_LOG.md      # User interaction documentation
└── docs/                                  # Documentation and guides
    ├── DESKTOP_AUTOMATION_EXAMPLES.md    # Usage examples
    ├── LINUX_DESKTOP_AUTOMATION_GUIDE.md # Comprehensive guide
    └── TESTING_RESULTS.md                # Test result summaries
```

## 🚀 Quick Start

### **Prerequisites**
```bash
# Install Python dependencies
pip install selenium playwright pytest

# Install browser drivers
playwright install
# For Selenium, chromedriver should be in PATH

# Install system dependencies (Ubuntu/Debian)
sudo apt install xvfb xdotool wmctrl

# Install system dependencies (Fedora)
sudo dnf install xorg-x11-server-Xvfb xdotool wmctrl
```

### **Basic Usage**
```bash
# Clone the repository
git clone https://github.com/swipswaps/linux-desktop-automation.git
cd linux-desktop-automation

# Run Selenium tests
python3 test_cache_clearing.py
python3 test_all_buttons_fixed.py

# Run Playwright tests
python3 test_cache_playwright.py
python3 comprehensive_browser_tests.py

# Run terminal automation tests
python3 test_actual_terminal_capture.py
```

## 📈 Usage Examples

### **Cache Management Testing**
```bash
# Test cache clearing with visual verification
python3 test_cache_clearing.py

# Playwright-based cache testing
python3 test_cache_playwright.py
```

### **UI Component Testing**
```bash
# Test all button functionality
python3 test_all_buttons_fixed.py

# Accessibility testing
python3 test_text_selectability.py
```

### **Terminal Automation**
```bash
# Real terminal capture testing
python3 test_actual_terminal_capture.py

# Automated terminal cleanup
python3 test_3_second_terminal_close.py
```

### **Comprehensive Testing**
```bash
# Run full automation verification
python3 final_automation_verification.py

# Cross-browser testing
python3 comprehensive_browser_tests.py
```

## 🎯 Key Benefits

- **🔍 Real System Testing**: No simulations - actual desktop environment testing
- **📸 Visual Evidence**: Screenshot capture for every test step
- **🚀 Cross-Platform**: Works on major Linux distributions
- **⚡ Fast Execution**: Optimized for quick feedback cycles
- **🛡️ Accessibility Focus**: Built-in accessibility compliance testing
- **📊 Detailed Reporting**: JSON reports with timing and success metrics

## 🧪 Test Categories

### **Web Interface Testing**
- Dashboard functionality verification
- Button click automation and validation
- Form submission and data handling
- API endpoint testing through web interfaces

### **Desktop Environment Testing**
- KDE Plasma widget management
- System cache operations
- Terminal window automation
- Desktop application integration

### **Performance Testing**
- Page load timing analysis
- Memory usage monitoring
- Cache effectiveness measurement
- System responsiveness validation

## 🔧 Advanced Configuration

### **Selenium Configuration**
```python
# Custom Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
```

### **Playwright Configuration**
```python
# Browser launch options
browser = await playwright.chromium.launch(
    headless=True,
    args=['--no-sandbox', '--disable-dev-shm-usage']
)
```

### **Evidence Collection**
```python
# Screenshot with timestamp
screenshot_name = f"test_evidence_{int(time.time())}.png"
driver.save_screenshot(screenshot_name)

# JSON report generation
results = {
    "timestamp": datetime.now().isoformat(),
    "test_status": "PASS",
    "evidence_files": [screenshot_name]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/automation-improvement`)
3. Commit your changes (`git commit -m 'Add automation improvement'`)
4. Push to the branch (`git push origin feature/automation-improvement`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [kde-memory-guardian](https://github.com/swipswaps/kde-memory-guardian) - KDE memory management
- [memory-pressure-tools](https://github.com/swipswaps/memory-pressure-tools) - System memory management
- [performance-monitoring-suite](https://github.com/swipswaps/performance-monitoring-suite) - Performance analysis

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Built with ❤️ for Linux desktop automation and testing**
