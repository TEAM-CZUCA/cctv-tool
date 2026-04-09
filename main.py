import os
import sys
import time
import urllib.request
import urllib.error
import webbrowser

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
# আপনার GitHub Raw URL এখানে দিন
REMOTE_URL = "https://raw.githubusercontent.com/YourUsername/YourRepo/main/list.txt"
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

    def clear_screen(self):
        """Screen পরিষ্কার করার function"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_banner(self):
        """banner.txt থেকে ASCII Banner দেখানোর function"""
        self.clear_screen()
        try:
            if os.path.exists(BANNER_FILE):
                with open(BANNER_FILE, 'r', encoding='utf-8') as f:
                    banner = f.read()
                    print(f"{Colors.CYAN}{Colors.BOLD}{banner}{Colors.RESET}")
            else:
                print(f"{Colors.CYAN}{Colors.BOLD}=== ADVANCED TERMUX TOOLKIT ==={Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Banner Load Error: {e}{Colors.RESET}")
        print("\n")

    def fetch_data(self):
        """Remote URL থেকে ডাটা লোড করা, ফেইল করলে Local File ব্যবহার করা"""
        print(f"{Colors.YELLOW}[*] Fetching data from remote server...{Colors.RESET}")
        
        try:
            # Request remote data (timeout 5 seconds)
            req = urllib.request.Request(REMOTE_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('utf-8')
                self._parse_data(content)
                print(f"{Colors.GREEN}[+] Data loaded successfully from Online!{Colors.RESET}")
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
        self.data_list = []
        lines = raw_text.strip().splitlines()
        for line in lines:
            # Ignore empty lines and comments
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
    app.fetch_data()
    app.show_menu()

if __name__ == "__main__":
    main()
