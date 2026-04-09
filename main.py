import os
import sys
import time
import urllib.request
import urllib.error
import webbrowser

# ==========================================
# ⚙️ CONFIGURATION (TEAM-CZUCA URLs)
# ==========================================
# GitHub Raw URLs (To fetch exact text content)
REMOTE_BANNER_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/banner.txt"
REMOTE_LIST_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/wordlist/main/list.txt"

LOCAL_LIST = "list.txt"
BANNER_FILE = "banner.txt"

# ==========================================
# 🎨 COLOR SYSTEM (ANSI)
# ==========================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ==========================================
# 🧠 TOOLKIT CORE CLASS
# ==========================================
class TermuxToolkit:
    def __init__(self):
        self.data_list = []
        self.banner_text = ""

    def clear_screen(self):
        """Screen পরিষ্কার করার function"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_banner(self):
        """ASCII Banner দেখানোর function"""
        self.clear_screen()
        if self.banner_text:
            print(f"{Colors.CYAN}{Colors.BOLD}{self.banner_text}{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}{Colors.BOLD}=== TEAM-CZUCA ADVANCED TOOLKIT ==={Colors.RESET}")
        print("\n")

    def fetch_resources(self):
        """Remote URL থেকে Banner এবং List লোড করা ও Offline-এর জন্য Save করা"""
        print(f"{Colors.YELLOW}[*] Fetching resources from TEAM-CZUCA GitHub...{Colors.RESET}")
        
        # 1. Fetch Banner
        try:
            req_banner = urllib.request.Request(REMOTE_BANNER_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_banner, timeout=5) as response:
                self.banner_text = response.read().decode('utf-8')
                # Save as fallback
                with open(BANNER_FILE, 'w', encoding='utf-8') as f:
                    f.write(self.banner_text)
        except Exception:
            # Fallback to local banner if remote fails
            if os.path.exists(BANNER_FILE):
                with open(BANNER_FILE, 'r', encoding='utf-8') as f:
                    self.banner_text = f.read()

        # 2. Fetch List
        try:
            req_list = urllib.request.Request(REMOTE_LIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_list, timeout=5) as response:
                content = response.read().decode('utf-8')
                self._parse_data(content)
                # Save as fallback
                with open(LOCAL_LIST, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"{Colors.GREEN}[+] Resources loaded successfully from Online!{Colors.RESET}")
                time.sleep(1)
        except (urllib.error.URLError, Exception) as e:
            print(f"{Colors.RED}[!] Network fail: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Switching to local fallback ({LOCAL_LIST})...{Colors.RESET}")
            self._load_local_data()

    def _load_local_data(self):
        """Local file থেকে ডাটা লোড করার function"""
        if os.path.exists(LOCAL_LIST):
            try:
                with open(LOCAL_LIST, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._parse_data(content)
                    print(f"{Colors.GREEN}[+] Data loaded successfully from Local File!{Colors.RESET}")
                    time.sleep(1)
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to read local file: {e}{Colors.RESET}")
                sys.exit(1)
        else:
            print(f"{Colors.RED}[!] Fatal Error: No network connection and local '{LOCAL_LIST}' not found.{Colors.RESET}")
            sys.exit(1)

    def _parse_data(self, raw_text):
        """Raw text কে Name এবং URL এ ভাগ করা"""
        self.data_list =[]
        lines = raw_text.strip().splitlines()
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            
            if '|' in line:
                name, url = line.split('|', 1)
                self.data_list.append({"name": name.strip(), "url": url.strip()})
        
        if not self.data_list:
            print(f"{Colors.RED}[!] Error: No valid data found in the list.{Colors.RESET}")
            sys.exit(1)

    def open_link(self, url):
        """URL Browser এ Open করার function"""
        if url.startswith("http://") or url.startswith("https://"):
            print(f"{Colors.GREEN}[+] Opening URL: {url}{Colors.RESET}")
            try:
                webbrowser.open(url)
                print(f"{Colors.BLUE}[*] Check your browser!{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to open browser: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Invalid URL format: {url}{Colors.RESET}")
        
        time.sleep(2)

    def show_menu(self):
        """Dynamic Menu System"""
        while True:
            self.show_banner()
            print(f"{Colors.YELLOW}>> SELECT AN OPTION <<{Colors.RESET}\n")
            
            # Display dynamically loaded items
            for index, item in enumerate(self.data_list, start=1):
                print(f"  {Colors.GREEN}[{index}]{Colors.RESET} {item['name']}")
            
            print(f"\n  {Colors.RED}[0]{Colors.RESET} Exit Toolkit")
            print(f"{Colors.CYAN}-{Colors.RESET}" * 40)
            
            # User Input Handling
            try:
                choice = input(f"\n{Colors.BOLD}Termux > {Colors.RESET}").strip()
                
                if choice == '0':
                    print(f"\n{Colors.GREEN}[*] Exiting toolkit. Goodbye!{Colors.RESET}")
                    sys.exit(0)
                
                if choice.isdigit():
                    choice_idx = int(choice)
                    if 1 <= choice_idx <= len(self.data_list):
                        selected_item = self.data_list[choice_idx - 1]
                        self.open_link(selected_item['url'])
                    else:
                        print(f"{Colors.RED}[!] Invalid Selection. Please choose a valid number.{Colors.RESET}")
                        time.sleep(1)
                else:
                    print(f"{Colors.RED}[!] Invalid Input. Please enter numbers only.{Colors.RESET}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.RED}[!] Program interrupted by user. Exiting...{Colors.RESET}")
                sys.exit(0)

# ==========================================
# 🚀 MAIN EXECUTION
# ==========================================
def main():
    app = TermuxToolkit()
    app.clear_screen()
    app.fetch_resources()
    app.show_menu()

if __name__ == "__main__":
    main()
