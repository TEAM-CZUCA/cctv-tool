import os
import sys
import time
import urllib.request
import urllib.error
import subprocess

# ==========================================
# ⚙️ CONFIGURATION (TEAM-CZUCA URLs)
# ==========================================
REMOTE_BANNER_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/banner.txt"
REMOTE_LIST_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/wordlist/main/list.txt"

LOCAL_LIST = "list.txt"
BANNER_FILE = "banner.txt"
MENU_WIDTH = 50  # Box Width for Premium UI

# ==========================================
# 🎨 PREMIUM COLOR SYSTEM (ANSI)
# ==========================================
class Colors:
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    BLUE = '\033[38;5;33m'
    CYAN = '\033[38;5;51m'
    MAGENTA = '\033[38;5;201m'
    WHITE = '\033[38;5;231m'
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
        os.system('clear' if os.name == 'posix' else 'cls')

    def animated_loading(self, text, duration=2):
        """Premium Spinner Animation"""
        chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
        end_time = time.time() + duration
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{Colors.CYAN}[{chars[idx]}]{Colors.RESET} {Colors.YELLOW}{text}{Colors.RESET}")
            sys.stdout.flush()
            idx = (idx + 1) % len(chars)
            time.sleep(0.1)
        sys.stdout.write(f"\r{Colors.GREEN}[✔]{Colors.RESET} {Colors.WHITE}{text} - Success!{' '*10}{Colors.RESET}\n")

    def show_banner(self):
        self.clear_screen()
        if self.banner_text:
            print(f"{Colors.MAGENTA}{Colors.BOLD}{self.banner_text}{Colors.RESET}")
        else:
            print(f"{Colors.CYAN}{Colors.BOLD}=== TEAM-CZUCA ADVANCED TOOLKIT ==={Colors.RESET}")
        print()

    def fetch_resources(self, is_update=False):
        """Fetch files from GitHub with Premium Loading"""
        if is_update:
            print(f"\n{Colors.CYAN}[*] Initiating Live Update...{Colors.RESET}")
        
        self.animated_loading("Connecting to TEAM-CZUCA Servers...", 1.5)

        # Fetch Banner
        try:
            req_banner = urllib.request.Request(REMOTE_BANNER_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_banner, timeout=5) as response:
                self.banner_text = response.read().decode('utf-8')
                with open(BANNER_FILE, 'w', encoding='utf-8') as f:
                    f.write(self.banner_text)
        except Exception:
            if os.path.exists(BANNER_FILE):
                with open(BANNER_FILE, 'r', encoding='utf-8') as f:
                    self.banner_text = f.read()

        # Fetch List
        try:
            req_list = urllib.request.Request(REMOTE_LIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_list, timeout=5) as response:
                content = response.read().decode('utf-8')
                self._parse_data(content)
                with open(LOCAL_LIST, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.animated_loading("Downloading Latest Payloads...", 1.5)
        except (urllib.error.URLError, Exception) as e:
            print(f"{Colors.RED}[!] Network fail: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Switching to Offline Mode...{Colors.RESET}")
            time.sleep(1)
            self._load_local_data()

        if is_update:
            print(f"{Colors.GREEN}[+] Update Completed Successfully!{Colors.RESET}")
            time.sleep(1.5)

    def _load_local_data(self):
        if os.path.exists(LOCAL_LIST):
            try:
                with open(LOCAL_LIST, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._parse_data(content)
                    print(f"{Colors.GREEN}[+] Loaded from Offline Cache.{Colors.RESET}")
                    time.sleep(1)
            except Exception as e:
                print(f"{Colors.RED}[!] Failed to read cache: {e}{Colors.RESET}")
                sys.exit(1)
        else:
            print(f"{Colors.RED}[!] Fatal Error: No internet and no offline cache found.{Colors.RESET}")
            sys.exit(1)

    def _parse_data(self, raw_text):
        self.data_list =[]
        lines = raw_text.strip().splitlines()
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            if '|' in line:
                name, url = line.split('|', 1)
                self.data_list.append({"name": name.strip(), "url": url.strip()})
        
        if not self.data_list:
            print(f"{Colors.RED}[!] Error: No data found.{Colors.RESET}")
            sys.exit(1)

    def open_link(self, url):
        if url.startswith("http://") or url.startswith("https://"):
            print(f"\n{Colors.CYAN}[*] Launching target URL...{Colors.RESET}")
            time.sleep(0.5)
            try:
                subprocess.run(['termux-open-url', url], check=True)
                print(f"{Colors.GREEN}[+] Target Opened in System Browser!{Colors.RESET}")
            except Exception:
                try:
                    import webbrowser
                    webbrowser.open(url)
                    print(f"{Colors.GREEN}[+] Target Opened!{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[!] Failed to open browser: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Invalid URL target: {url}{Colors.RESET}")
        time.sleep(2)

    def draw_box_line(self, left, right, middle_char="─"):
        """Helper to draw premium box borders"""
        print(f"{Colors.BLUE}{left}{middle_char * MENU_WIDTH}{right}{Colors.RESET}")

    def show_menu(self):
        """Premium UI Menu System"""
        while True:
            self.show_banner()
            
            # Draw Top Box
            self.draw_box_line("╭", "╮")
            title = f"{Colors.YELLOW}{Colors.BOLD}❖ SELECT A TARGET ❖{Colors.RESET}"
            print(f"{Colors.BLUE}│{Colors.RESET} {title.center(MENU_WIDTH + 14)} {Colors.BLUE}│{Colors.RESET}")
            self.draw_box_line("├", "┤")
            
            # Print List Items
            for index, item in enumerate(self.data_list, start=1):
                idx_str = f"{index:02d}"  # 01, 02 format
                name_str = item['name'][:MENU_WIDTH-12] # Trim if too long
                
                # Format: │  [01] 🟢 Tool Name     │
                line = f"  {Colors.CYAN}[{idx_str}]{Colors.RESET} {Colors.WHITE}■{Colors.RESET} {Colors.GREEN}{name_str}{Colors.RESET}"
                padding = MENU_WIDTH - len(idx_str) - len(name_str) - 8
                print(f"{Colors.BLUE}│{Colors.RESET}{line}{' ' * padding}{Colors.BLUE}│{Colors.RESET}")
            
            # Draw System Options Segment
            self.draw_box_line("├", "┤")
            sys_title = f"{Colors.RED}⚙ SYSTEM OPTIONS ⚙{Colors.RESET}"
            print(f"{Colors.BLUE}│{Colors.RESET} {sys_title.center(MENU_WIDTH + 8)} {Colors.BLUE}│{Colors.RESET}")
            self.draw_box_line("├", "┤")
            
            # Update & Exit Options
            update_line = f"  {Colors.YELLOW}[88]{Colors.RESET} {Colors.WHITE}🔄 Update Toolkit{Colors.RESET}"
            exit_line   = f"  {Colors.RED}[00]{Colors.RESET} {Colors.WHITE}❌ Exit System{Colors.RESET}"
            
            print(f"{Colors.BLUE}│{Colors.RESET}{update_line}{' ' * (MENU_WIDTH - 21)}{Colors.BLUE}│{Colors.RESET}")
            print(f"{Colors.BLUE}│{Colors.RESET}{exit_line}{' ' * (MENU_WIDTH - 19)}{Colors.BLUE}│{Colors.RESET}")
            self.draw_box_line("╰", "╯")
            
            # Input Prompt
            try:
                choice = input(f"\n  {Colors.BOLD}{Colors.MAGENTA}CZUCA {Colors.CYAN}❯ {Colors.GREEN}").strip()
                print(Colors.RESET, end="") # Reset color after input
                
                if choice == '00' or choice == '0':
                    print(f"\n{Colors.RED}[*] Terminating Session. Goodbye!{Colors.RESET}")
                    sys.exit(0)
                
                elif choice == '88':
                    # Call Update Function
                    self.fetch_resources(is_update=True)
                
                elif choice.isdigit():
                    choice_idx = int(choice)
                    if 1 <= choice_idx <= len(self.data_list):
                        selected_item = self.data_list[choice_idx - 1]
                        self.open_link(selected_item['url'])
                    else:
                        print(f"{Colors.RED}[!] Invalid Target ID.{Colors.RESET}")
                        time.sleep(1)
                else:
                    print(f"{Colors.RED}[!] Invalid Input.{Colors.RESET}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n\n{Colors.RED}[!] Force Exit Triggered...{Colors.RESET}")
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
