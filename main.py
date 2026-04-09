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
# GitHub URLs (For fallback or data)
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
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Redirecting to TEAM-CZUCA Official Facebook Page...{Colors.RESET}")
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
            if self.first_run:
                self.typewriter(f"{color}{Colors.BOLD}{line}{Colors.RESET}\n", speed=0.002)
            else:
                print(f"{color}{Colors.BOLD}{line}{Colors.RESET}")
        print()

    def fetch_resources(self):
        """প্রাথমিক ডাটা লোড করার জন্য"""
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
                print(f"{Colors.RED}[!] Error: No Internet connection to fetch list.{Colors.RESET}")
                sys.exit(1)

    def update_toolkit(self):
        """Git Pull এর মাধ্যমে টুল আপডেট করার মেথড"""
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Checking for updates via GitHub...{Colors.RESET}")
        self.animated_loading("Syncing with TEAM-CZUCA Repository", 2.0)
        
        try:
            # বর্তমান ডিরেক্টরি কি গিট রিপোজিটরি কি না চেক করা
            if os.path.exists(".git"):
                # Git Pull কমান্ড চালানো
                process = subprocess.run(['git', 'pull'], capture_output=True, text=True)
                
                if "Already up to date" in process.stdout:
                    print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} You are already using the latest version!{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Successfully updated to latest version!{Colors.RESET}")
                    # আপডেট হওয়ার পর ব্যানার এবং লিস্ট নতুন করে ডাউনলোড করা (যদি কোনো চেইঞ্জ থাকে)
                    self.refresh_files_after_git()
            else:
                print(f"{Colors.RED}[!] Error: .git folder not found. Please 'git clone' the repo.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Update Failed: {e}{Colors.RESET}")
        
        time.sleep(2)

    def refresh_files_after_git(self):
        """Git Pull এর পর এক্সট্রা ফাইল রিফ্রেশ করার জন্য"""
        try:
            # Banner update
            urllib.request.urlretrieve(REMOTE_BANNER_URL, BANNER_FILE)
            # List update
            urllib.request.urlretrieve(REMOTE_LIST_URL, LOCAL_LIST)
        except:
            pass

    def _load_local_data(self):
        try:
            with open(LOCAL_LIST, 'r', encoding='utf-8') as f:
                content = f.read()
                self._parse_data(content)
        except:
            pass

    def _parse_data(self, raw_text):
        self.data_list =[]
        lines = raw_text.strip().splitlines()
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            if '|' in line:
                name, url = line.split('|', 1)
                self.data_list.append({"name": name.strip(), "url": url.strip()})

    def open_link(self, url):
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Launching target...{Colors.RESET}")
        try:
            subprocess.run(['termux-open-url', url], check=True)
        except:
            import webbrowser
            webbrowser.open(url)
        time.sleep(1)

    def print_menu_item(self, index, name, speed=0.01):
        idx_str = f"{index:02d}"
        line = f"   {Colors.RED}[{Colors.WHITE}{idx_str}{Colors.RED}]{Colors.WHITE} ➢  {Colors.GREEN}{name}{Colors.RESET}\n"
        if self.first_run:
            self.typewriter(line, speed)
            time.sleep(0.05)
        else:
            sys.stdout.write(line)

    def show_menu(self):
        while True:
            self.show_banner()
            
            # --- TARGET LIST ---
            title_1 = f"\n{Colors.RED} ━━━ {Colors.WHITE}✦ TARGET LIST ✦ {Colors.RED}━━━{Colors.RESET}\n\n"
            if self.first_run: self.typewriter(title_1, 0.005)
            else: sys.stdout.write(title_1)
            
            for index, item in enumerate(self.data_list, start=1):
                self.print_menu_item(index, item['name'])
            
            # --- SYSTEM OPTIONS ---
            title_2 = f"\n{Colors.RED} ━━━ {Colors.WHITE}⚙ SYSTEM OPTIONS ⚙ {Colors.RED}━━━{Colors.RESET}\n\n"
            if self.first_run: self.typewriter(title_2, 0.005)
            else: sys.stdout.write(title_2)

            self.print_menu_item(88, f"{Colors.YELLOW}Full Update (Git Pull & Sync){Colors.RESET}")
            self.print_menu_item(0, f"{Colors.RED}Exit System{Colors.RESET}")
            print()
            
            self.first_run = False 

            try:
                choice = input(f" {Colors.RED}CZUCA {Colors.WHITE}❯ {Colors.GREEN}").strip()
                
                if choice == '00' or choice == '0':
                    sys.exit(0)
                
                elif choice == '88':
                    # ==========================================
                    # 🔄 GIT PULL UPDATE & RESTART
                    # ==========================================
                    self.update_toolkit()
                    # টুলের কোড পরিবর্তন হয়ে থাকলে সেটি পুনরায় লোড করতে স্ক্রিপ্টটি রিস্টার্ট হবে
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
# 🚀 MAIN EXECUTION
# ==========================================
def main():
    app = TermuxToolkit()
    app.open_facebook_page() 
    app.fetch_resources()    
    app.show_menu()          

if __name__ == "__main__":
    main()
