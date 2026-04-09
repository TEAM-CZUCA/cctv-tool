#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import urllib.request
import urllib.error
import subprocess

# ==========================================
# ⚙️ CONFIGURATION & PATHS
# ==========================================
REMOTE_BANNER_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/banner.txt"
REMOTE_LIST_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/wordlist/main/list.txt"
FB_PAGE_URL = "https://www.facebook.com/CyberZulfiqarUnderCoverAgency"

HOME_DIR = os.environ.get('HOME', os.path.expanduser('~'))
APP_DIR = os.path.join(HOME_DIR, '.czuca_toolkit')

if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

LOCAL_LIST = os.path.join(APP_DIR, "list.txt")
BANNER_FILE = os.path.join(APP_DIR, "banner.txt")

# ==========================================
# 🎨 NEON COLOR SYSTEM (ANSI)
# ==========================================
class Colors:
    RED = '\033[38;5;196m'
    WHITE = '\033[38;5;231m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    CYAN = '\033[38;5;51m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ==========================================
# 🧠 TOOLKIT CORE CLASS
# ==========================================
class TermuxToolkit:
    def __init__(self):
        self.data_list = []
        self.banner_text = ""
        self.first_run = True 

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def typewriter(self, text, speed=0.005):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)

    def animated_loading(self, text, duration=1.5):
        chars =["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        end_time = time.time() + duration
        idx = 0
        while time.time() < end_time:
            sys.stdout.write(f"\r{Colors.RED}[{Colors.WHITE}{chars[idx]}{Colors.RED}]{Colors.RESET} {Colors.WHITE}{text}{Colors.RESET}")
            sys.stdout.flush()
            idx = (idx + 1) % len(chars)
            time.sleep(0.08)
        sys.stdout.write(f"\r{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.RESET} {Colors.WHITE}{text} - {Colors.GREEN}Done!{' '*10}{Colors.RESET}\n")

    def open_facebook_page(self):
        self.clear_screen()
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Follow TEAM-CZUCA Official Facebook Page...{Colors.RESET}")
        time.sleep(1)
        try:
            subprocess.run(['termux-open-url', FB_PAGE_URL], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            try:
                import webbrowser
                webbrowser.open(FB_PAGE_URL)
            except:
                pass
        time.sleep(1)

    def show_banner(self):
        self.clear_screen()
        if not self.banner_text:
            self.banner_text = "=== TEAM-CZUCA ADVANCED TOOLKIT ==="
        lines = self.banner_text.strip().splitlines()
        for i, line in enumerate(lines):
            color = Colors.RED if i % 2 == 0 else Colors.WHITE
            print(f"{color}{Colors.BOLD}{line}{Colors.RESET}")
        print()

    def fetch_resources(self):
        # Load Banner
        try:
            if os.path.exists(BANNER_FILE):
                with open(BANNER_FILE, 'r', encoding='utf-8') as f:
                    self.banner_text = f.read()
            else:
                req_banner = urllib.request.Request(REMOTE_BANNER_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_banner, timeout=5) as response:
                    self.banner_text = response.read().decode('utf-8')
                    with open(BANNER_FILE, 'w', encoding='utf-8') as f:
                        f.write(self.banner_text)
        except:
            self.banner_text = "=== TEAM-CZUCA TOOLKIT ==="

        # Load List
        if os.path.exists(LOCAL_LIST):
            self._load_local_data()
        else:
            try:
                req_list = urllib.request.Request(REMOTE_LIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_list, timeout=5) as response:
                    content = response.read().decode('utf-8')
                    self._parse_data(content)
                    with open(LOCAL_LIST, 'w', encoding='utf-8') as f:
                        f.write(content)
            except:
                pass

    def update_toolkit(self):
        """Git Pull Method"""
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Checking for updates via GitHub...{Colors.RESET}")
        self.animated_loading("Syncing Repository", 2.0)
        try:
            if os.path.exists(".git"):
                process = subprocess.run(['git', 'pull'], capture_output=True, text=True)
                if "Already up to date" in process.stdout:
                    print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Already latest version!{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Updated successfully!{Colors.RESET}")
                    # Refresh Cache
                    urllib.request.urlretrieve(REMOTE_BANNER_URL, BANNER_FILE)
                    urllib.request.urlretrieve(REMOTE_LIST_URL, LOCAL_LIST)
            else:
                print(f"{Colors.RED}[!] .git folder not found. Please clone again.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Update Failed: {e}{Colors.RESET}")
        time.sleep(2)

    def _load_local_data(self):
        try:
            with open(LOCAL_LIST, 'r', encoding='utf-8') as f:
                self._parse_data(f.read())
        except:
            pass

    def _parse_data(self, raw_text):
        self.data_list = []
        lines = raw_text.strip().splitlines()
        for line in lines:
            if '|' in line:
                name, url = line.split('|', 1)
                self.data_list.append({"name": name.strip(), "url": url.strip()})

    def open_link(self, url):
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Opening Target...{Colors.RESET}")
        try:
            subprocess.run(['termux-open-url', url], check=True)
        except:
            import webbrowser
            webbrowser.open(url)
        time.sleep(1)

    def show_menu(self):
        while True:
            self.show_banner()
            print(f"{Colors.RED} ━━━ {Colors.WHITE}✦ TARGET LIST ✦ {Colors.RED}━━━{Colors.RESET}\n")
            
            # --- MULTI-COLUMN LOGIC (MAX 10 ROWS) ---
            rows_limit = 10
            total_items = len(self.data_list)
            
            for i in range(rows_limit):
                row_line = ""
                # এই লুপটি প্রতি সারিতে কলাম তৈরি করে (i, i+10, i+20...)
                for j in range(i, total_items, rows_limit):
                    item = self.data_list[j]
                    idx_str = f"{(j + 1):02d}"
                    # কলামের প্রস্থ ২৫ ক্যারেক্টার রাখা হয়েছে যাতে লেখা এলোমেলো না হয়
                    column_content = f"  {Colors.RED}[{Colors.WHITE}{idx_str}{Colors.RED}]{Colors.WHITE} ➢ {Colors.GREEN}{item['name'][:15]:<15}{Colors.RESET}"
                    row_line += column_content
                
                if row_line.strip():
                    if self.first_run:
                        self.typewriter(row_line + "\n", 0.002)
                    else:
                        print(row_line)

            # --- SYSTEM OPTIONS ---
            print(f"\n{Colors.RED} ━━━ {Colors.WHITE}⚙ SYSTEM OPTIONS ⚙ {Colors.RED}━━━{Colors.RESET}\n")
            sys_options = f"  {Colors.RED}[{Colors.WHITE}88{Colors.RED}]{Colors.WHITE} ➢ {Colors.YELLOW}Update{Colors.RESET}    "
            sys_options += f"{Colors.RED}[{Colors.WHITE}00{Colors.RED}]{Colors.WHITE} ➢ {Colors.RED}Exit{Colors.RESET}"
            
            if self.first_run:
                self.typewriter(sys_options + "\n\n", 0.005)
            else:
                print(sys_options + "\n")
            
            self.first_run = False 

            try:
                choice = input(f" {Colors.RED}CZUCA {Colors.WHITE}❯ {Colors.GREEN}").strip()
                if choice in ['0', '00']:
                    sys.exit(0)
                elif choice == '88':
                    self.update_toolkit()
                    os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])
                elif choice.isdigit():
                    choice_idx = int(choice)
                    if 1 <= choice_idx <= len(self.data_list):
                        self.open_link(self.data_list[choice_idx - 1]['url'])
                    else:
                        print(f"{Colors.RED}[!] Invalid Choice.{Colors.RESET}")
                        time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)

# ==========================================
# 🚀 EXECUTION
# ==========================================
if __name__ == "__main__":
    app = TermuxToolkit()
    app.open_facebook_page() 
    app.fetch_resources()    
    app.show_menu()
