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
# 🎨 NEON COLOR SYSTEM
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
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Connecting to TEAM-CZUCA Facebook Page...{Colors.RESET}")
        try:
            subprocess.run(['termux-open-url', FB_PAGE_URL], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        """প্রাথমিক ডাটা লোড (লোকাল এবং রিমোট)"""
        # Load Banner from local or download
        try:
            if os.path.exists(BANNER_FILE):
                with open(BANNER_FILE, 'r', encoding='utf-8') as f:
                    self.banner_text = f.read()
            else:
                self.banner_text = "=== TEAM-CZUCA CCTV TOOL ==="
        except:
            pass
        
        # Load List from local cache
        if os.path.exists(LOCAL_LIST):
            self._load_local_data()
        else:
            # First time download if not exists
            self.refresh_data_files()

    def refresh_data_files(self):
        """সরাসরি সার্ভার থেকে লেটেস্ট লিস্ট এবং ব্যানার ডাউনলোড করার মেথড"""
        try:
            # Download Banner
            urllib.request.urlretrieve(REMOTE_BANNER_URL, BANNER_FILE)
            # Download Wordlist/Target List
            urllib.request.urlretrieve(REMOTE_LIST_URL, LOCAL_LIST)
            # রিফ্রেশ করার পর ডাটা পুনরায় পার্স করা
            self._load_local_data()
            return True
        except:
            return False

    def update_toolkit(self):
        """Git Pull এবং ডাটা ফাইল সিঙ্ক করার মেথড (Option 88)"""
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Initializing Deep System Update...{Colors.RESET}")
        
        # ১. গিট পুল এর মাধ্যমে কোড আপডেট
        self.animated_loading("Syncing Core Software via Git", 1.5)
        git_updated = False
        try:
            if os.path.exists(".git"):
                process = subprocess.run(['git', 'pull'], capture_output=True, text=True)
                if "Already up to date" not in process.stdout:
                    git_updated = True
            else:
                print(f"{Colors.RED}[!] .git not found. Skipping code sync.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Git Error: {e}{Colors.RESET}")

        # ২. সার্ভার থেকে নতুন লিস্ট এবং ব্যানার ডাউনলোড (এটি সবসময় কাজ করবে)
        self.animated_loading("Fetching Latest Target Wordlists", 1.5)
        data_updated = self.refresh_data_files()

        if git_updated or data_updated:
            print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} System & Database updated successfully!{Colors.RESET}")
        else:
            print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Everything is already up to date!{Colors.RESET}")
        
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
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Redirecting to camera feed...{Colors.RESET}")
        try:
            subprocess.run(['termux-open-url', url], check=True)
        except:
            import webbrowser
            webbrowser.open(url)
        time.sleep(1)

    def show_menu(self):
        while True:
            self.show_banner()
            print(f"{Colors.RED} ━━━ {Colors.WHITE}✦ CAMERA LIST ✦ {Colors.RED}━━━{Colors.RESET}\n")
            
            # --- MULTI-COLUMN LOGIC (MAX 10 ROWS) ---
            rows_limit = 20
            total_items = len(self.data_list)
            
            if total_items == 0:
                print(f"    {Colors.RED}[!] No Cameras found....{Colors.RESET}")
            else:
                for i in range(rows_limit):
                    row_line = ""
                    for j in range(i, total_items, rows_limit):
                        item = self.data_list[j]
                        idx_str = f"{(j + 1):02d}"
                        column_content = f"  {Colors.RED}[{Colors.WHITE}{idx_str}{Colors.RED}]{Colors.WHITE} ➢ {Colors.GREEN}{item['name'][:14]:<14}{Colors.RESET}"
                        row_line += column_content
                    
                    if row_line.strip():
                        if self.first_run:
                            self.typewriter(row_line + "\n", 0.002)
                        else:
                            print(row_line)

            # --- SYSTEM OPTIONS ---
            print(f"\n{Colors.RED} ━━━ {Colors.WHITE}⚙ SYSTEM OPTIONS ⚙ {Colors.RED}━━━{Colors.RESET}\n")
            sys_options = f"  {Colors.RED}[{Colors.WHITE}88{Colors.RED}]{Colors.WHITE} ➢ {Colors.YELLOW}Update{Colors.RESET}    "
            sys_options += f"{Colors.RED}[{Colors.WHITE}00{Colors.RED}]{Colors.WHITE} ➢ {Colors.RED}Exit System{Colors.RESET}"
            
            if self.first_run:
                self.typewriter(sys_options + "\n\n", 0.005)
            else:
                print(sys_options + "\n")
            
            self.first_run = False 

            try:
                choice = input(f" {Colors.RED}CZUCA {Colors.WHITE}❯ {Colors.GREEN}").strip()
                if choice in ['0', '00']:
                    sys.exit(0)
                elif choice == 'U':
                    self.update_toolkit()
                    # আপডেট শেষে টুল রিস্টার্ট করা যাতে নতুন লিস্ট লোড হয়
                    os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])
                elif choice.isdigit():
                    choice_idx = int(choice)
                    if 1 <= choice_idx <= len(self.data_list):
                        self.open_link(self.data_list[choice_idx - 1]['url'])
                    else:
                        print(f"{Colors.RED}[!] Target ID not found.{Colors.RESET}")
                        time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)

# ==========================================
# 🚀 START
# ==========================================
if __name__ == "__main__":
    app = TermuxToolkit()
    app.open_facebook_page() 
    app.fetch_resources()    
    app.show_menu()
