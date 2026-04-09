#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import urllib.request
import urllib.error
import subprocess

# ==========================================
# ⚙️ CONFIGURATION & PATHS
# ==========================================
# GitHub Raw URLs
REMOTE_BANNER_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/banner.txt"
REMOTE_LIST_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/wordlist/main/list.txt"

# Core Script URL (To Auto-Update This Python File)
# আপনি আপনার main.py গিটহাবে আপলোড করে এখানকার লিংকটি আপডেট করে দিবেন
REMOTE_CORE_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/main.py"

# Termux Secure Storage Paths
HOME_DIR = os.environ.get('HOME', os.path.expanduser('~'))
APP_DIR = os.path.join(HOME_DIR, '.czuca_toolkit')

# Create directory if it doesn't exist
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

    def fetch_resources(self, is_update=False):
        if is_update:
            print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Initiating Live Deep Update...{Colors.RESET}")
            self.animated_loading("Connecting to TEAM-CZUCA Servers...", 1.5)
        else:
            self.animated_loading("Initializing System & Checking Servers...", 1.0)

        # 1. Fetch Banner
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

        # 2. Fetch List
        try:
            req_list = urllib.request.Request(REMOTE_LIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req_list, timeout=5) as response:
                content = response.read().decode('utf-8')
                self._parse_data(content)
                with open(LOCAL_LIST, 'w', encoding='utf-8') as f:
                    f.write(content)
                if is_update:
                    self.animated_loading("Downloading Latest Payloads...", 1.2)
        except (urllib.error.URLError, Exception) as e:
            if is_update:
                print(f"{Colors.RED}[!] Connection Failed: {e}{Colors.RESET}")
                time.sleep(2)
            self._load_local_data()

        # 3. Fetch Core Script (Auto-Update main.py itself)
        if is_update:
            self.animated_loading("Checking for Core Software Updates...", 1.2)
            try:
                req_core = urllib.request.Request(REMOTE_CORE_URL, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_core, timeout=5) as response:
                    core_code = response.read().decode('utf-8')
                    # Verification Check (To ensure we don't download empty file)
                    if "class TermuxToolkit:" in core_code:
                        with open(os.path.abspath(__file__), 'w', encoding='utf-8') as f:
                            f.write(core_code)
                        print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Core Script Updated Successfully!{Colors.RESET}")
            except Exception:
                pass # Ignore if core update fails

        if is_update:
            print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} System Update Completed!{Colors.RESET}")
            time.sleep(1)

    def _load_local_data(self):
        if os.path.exists(LOCAL_LIST):
            try:
                with open(LOCAL_LIST, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._parse_data(content)
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
            print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Launching target URL...{Colors.RESET}")
            time.sleep(0.5)
            try:
                subprocess.run(['termux-open-url', url], check=True)
                print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Target Opened in System Browser!{Colors.RESET}")
            except Exception:
                try:
                    import webbrowser
                    webbrowser.open(url)
                    print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Target Opened!{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[!] Failed to open browser: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Invalid URL target: {url}{Colors.RESET}")
        time.sleep(2)

    def print_menu_item(self, index, name, speed=0.01):
        idx_str = f"{index:02d}"
        line = f"   {Colors.RED}[{Colors.WHITE}{idx_str}{Colors.RED}]{Colors.WHITE} ➢  {Colors.GREEN}{name}{Colors.RESET}\n"
        if self.first_run:
            self.typewriter(line, speed)
            time.sleep(0.05)
        else:
            sys.stdout.write(line)

    def install_global_shortcut(self):
        """Install toolkit to Termux bin directory for global access"""
        prefix = os.environ.get('PREFIX', '/data/data/com.termux/files/usr')
        bin_path = os.path.join(prefix, 'bin', 'czuca')
        
        print(f"\n{Colors.RED}[{Colors.WHITE}*{Colors.RED}]{Colors.WHITE} Installing Global Command...{Colors.RESET}")
        time.sleep(1)
        
        try:
            shutil.copyfile(os.path.abspath(__file__), bin_path)
            os.chmod(bin_path, 0o755) # Make it executable
            print(f"{Colors.RED}[{Colors.GREEN}✔{Colors.RED}]{Colors.WHITE} Success! You can now just type {Colors.GREEN}'czuca'{Colors.WHITE} anywhere to run this toolkit!{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to create global command: {e}{Colors.RESET}")
        time.sleep(3)

    def show_menu(self):
        while True:
            self.show_banner()
            
            # --- TARGET LIST ---
            title_1 = f"\n{Colors.RED} ━━━ {Colors.WHITE}✦ TARGET LIST ✦ {Colors.RED}━━━{Colors.RESET}\n\n"
            if self.first_run:
                self.typewriter(title_1, 0.005)
            else:
                sys.stdout.write(title_1)
            
            for index, item in enumerate(self.data_list, start=1):
                self.print_menu_item(index, item['name'])
            
            # --- SYSTEM OPTIONS ---
            title_2 = f"\n{Colors.RED} ━━━ {Colors.WHITE}⚙ SYSTEM OPTIONS ⚙ {Colors.RED}━━━{Colors.RESET}\n\n"
            if self.first_run:
                self.typewriter(title_2, 0.005)
            else:
                sys.stdout.write(title_2)

            self.print_menu_item(88, f"{Colors.YELLOW}Update Toolkit (Data & Core){Colors.RESET}")
            self.print_menu_item(99, f"{Colors.CYAN}Create Global Command (czuca){Colors.RESET}")
            self.print_menu_item(0, f"{Colors.RED}Exit System{Colors.RESET}")
            print()
            
            self.first_run = False 

            # --- INPUT ---
            try:
                choice = input(f" {Colors.RED}CZUCA {Colors.WHITE}❯ {Colors.GREEN}").strip()
                print(Colors.RESET, end="")
                
                if choice == '00' or choice == '0':
                    self.typewriter(f"\n{Colors.RED}[!] Terminating Session. Goodbye!{Colors.RESET}\n", 0.02)
                    sys.exit(0)
                
                elif choice == '99':
                    self.install_global_shortcut()
                
                elif choice == '88':
                    self.fetch_resources(is_update=True)
                    print(f"\n{Colors.RED}[{Colors.GREEN}↻{Colors.RED}]{Colors.WHITE} Applying Core Updates & Restarting...{Colors.RESET}")
                    time.sleep(1.5)
                    # Hard Restart Tool to Load New Core Source Code
                    os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)])
                
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
