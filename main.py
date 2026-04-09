#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import platform
import urllib.request
import urllib.error
import subprocess

# ==========================================
# ⚙️ CONFIGURATION & PATHS
# ==========================================
REMOTE_BANNER_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/banner.txt"
REMOTE_LIST_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/wordlist/main/list.txt"
REMOTE_CORE_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/main.py"

FB_PAGE_URL = "https://www.facebook.com/CyberZulfiqarUnderCoverAgency"

HOME_DIR = os.environ.get('HOME', os.path.expanduser('~'))
APP_DIR = os.path.join(HOME_DIR, '.czuca_toolkit')

if not os.path.exists(APP_DIR):
    os.makedirs(APP_DIR)

LOCAL_LIST = os.path.join(APP_DIR, "list.txt")
BANNER_FILE = os.path.join(APP_DIR, "banner.txt")

# ==========================================
# 🎨 UCA COLORS (ANSI)
# ==========================================
class Colors:
    R = '\033[1;31m'  # Red
    G = '\033[1;32m'  # Green
    C = '\033[1;36m'  # Cyan
    Y = '\033[1;33m'  # Yellow
    P = '\033[1;35m'  # Purple
    W = '\033[1;37m'  # White
    BK = '\033[1;30m' # Black
    RESET = '\033[0m'

system_os = platform.system()

def get_cols():
    try:
        cols, _ = shutil.get_terminal_size()
    except:
        cols = 60
    return cols

# ==========================================
# 🧠 TOOLKIT CORE CLASS
# ==========================================
class TermuxToolkit:
    def __init__(self):
        self.data_list = []
        self.banner_text = ""
        self.cols = get_cols()

    def clear_screen(self):
        if system_os == "Windows": os.system('cls')
        else: os.system('clear')

    # --- 1. UCA INTRO BOOT ANIMATION ---
    def intro_animation(self):
        self.clear_screen()
        print(f"\n{Colors.BK} [INIT] ESTABLISHING CONNECTION TO CZUCA SERVER...{Colors.RESET}")
        time.sleep(0.5)
        
        logs =[
            "LOADING_CZUCA_MODULES",
            "VERIFYING_USER_PERMISSIONS",
            "FETCHING_THEME_DATABASE",
            "OPTIMIZING_NETWORK_TUNNEL",
            "ACCESS_GRANTED_CORE_SYSTEM"
        ]
        
        for log in logs:
            sys.stdout.write(f"\r {Colors.C}:: SYSTEM_BOOT >> {log:<30} {Colors.Y}[WAIT]")
            time.sleep(0.2)
            sys.stdout.write(f"\r {Colors.C}:: SYSTEM_BOOT >> {log:<30} {Colors.G}[OK]  \n")
            time.sleep(0.1)
        
        time.sleep(0.5)

    def open_facebook_page(self):
        self.clear_screen()
        print(f"\n{Colors.C}[*]{Colors.W} INITIATING REDIRECT TO CZUCA HEADQUARTERS...{Colors.RESET}")
        time.sleep(0.5)
        try:
            subprocess.run(['termux-open-url', FB_PAGE_URL], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            try:
                import webbrowser
                webbrowser.open(FB_PAGE_URL)
            except:
                pass
        time.sleep(1.5)

    def silent_startup_check(self):
        """Silently load data into memory on boot"""
        sys.stdout.write(f"\r {Colors.Y}:: MOUNTING LOCAL DATABASES...{Colors.RESET} ")
        sys.stdout.flush()
        
        # Load Banner
        try:
            if os.path.exists(BANNER_FILE):
                with open(BANNER_FILE, 'r', encoding='utf-8') as f:
                    self.banner_text = f.read()
        except: pass

        # Load List
        if os.path.exists(LOCAL_LIST):
            try:
                with open(LOCAL_LIST, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self._parse_data(content)
            except: pass
            
        sys.stdout.write(f"\r {Colors.G}:: MOUNTING LOCAL DATABASES...[OK] {' '*10}{Colors.RESET}\n")
        time.sleep(0.5)

    # --- 2. UCA UPDATE LOADER (5 STEPS ANIMATION) ---
    def install_loaders_update(self):
        self.clear_screen()
        print(f"\n{Colors.G}[*] INITIALIZING UPDATE PROTOCOLS...{Colors.RESET}\n")
        time.sleep(0.5)
        
        # Update Steps Mapping
        steps =[
            ("CONFIGURING SECURE TUNNEL", lambda: time.sleep(0.5)),
            ("DOWNLOADING HIGH-RES ASSETS", self._fetch_banner),
            ("FETCHING TARGET PAYLOADS", self._fetch_list),
            ("INJECTING CORE KERNEL", self._fetch_core),
            ("FINALIZING SYSTEM VERIFICATION", lambda: time.sleep(0.5))
        ]
        
        for step_name, func in steps:
            # Fake Spinner Animation for visual effect
            for i in range(10): # Spinnig for 1 second
                chars = "/-\\|"
                sys.stdout.write(f"\r {Colors.C}[PROCESS] {step_name}... {Colors.Y}{chars[i%4]} {Colors.RESET}")
                sys.stdout.flush()
                time.sleep(0.1)
            
            # Execute actual download/update task
            try:
                func()
                sys.stdout.write(f"\r {Colors.C}[PROCESS] {step_name:<30} {Colors.G}[DONE]{' '*5}\n")
            except Exception as e:
                sys.stdout.write(f"\r {Colors.C}[PROCESS] {step_name:<30} {Colors.R}[FAIL]{' '*5}\n")
            time.sleep(0.2)
        
        print(f"\n{Colors.BK} [LOG] SYSTEM REBOOT REQUIRED...{Colors.RESET}")
        time.sleep(1.5)
        # Execute Auto-Restart
        os.execv(sys.executable,[sys.executable, os.path.abspath(__file__)])

    # --- UPDATE BACKGROUND WORKERS ---
    def _fetch_banner(self):
        req = urllib.request.Request(REMOTE_BANNER_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            self.banner_text = response.read().decode('utf-8')
            with open(BANNER_FILE, 'w', encoding='utf-8') as f:
                f.write(self.banner_text)

    def _fetch_list(self):
        req = urllib.request.Request(REMOTE_LIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            content = response.read().decode('utf-8')
            self._parse_data(content)
            with open(LOCAL_LIST, 'w', encoding='utf-8') as f:
                f.write(content)

    def _fetch_core(self):
        req = urllib.request.Request(REMOTE_CORE_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            core_code = response.read().decode('utf-8')
            if "class TermuxToolkit:" in core_code:
                with open(os.path.abspath(__file__), 'w', encoding='utf-8') as f:
                    f.write(core_code)
            else:
                raise Exception("Corrupt Core")

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
            self.data_list = [{"name": "No Data Found. Update Toolkit (88).", "url": ""}]

    # --- SYSTEM LINKS ---
    def open_link(self, url):
        if url.startswith("http://") or url.startswith("https://"):
            print(f"\n {Colors.C}┌──[ {Colors.P}TARGETING{Colors.C} ]")
            print(f" {Colors.C}└─➤ {Colors.W}Launching URL...{Colors.RESET}")
            time.sleep(0.5)
            try:
                subprocess.run(['termux-open-url', url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"     {Colors.G}[✔] TARGET OPENED IN BROWSER{Colors.RESET}")
            except Exception:
                try:
                    import webbrowser
                    webbrowser.open(url)
                    print(f"     {Colors.G}[✔] TARGET OPENED{Colors.RESET}")
                except Exception as e:
                    print(f"     {Colors.R}[!] FAILED: {e}{Colors.RESET}")
        else:
            print(f"\n {Colors.R}[!] INVALID URL: {url}{Colors.RESET}")
        time.sleep(2)

    # --- UCA THEMED UI ---
    def print_uca_header(self):
        self.clear_screen()
        # Top Bar
        print(f"{Colors.C}╔{'═'*(self.cols-2)}╗")
        title = f" {Colors.R}● {Colors.W}CZUCA ADVANCED TERMINAL {Colors.R}● "
        pad = (self.cols - 29) // 2
        print(f"{Colors.C}║{' '*pad}{title}{' '*pad}{Colors.C}║")
        print(f"{Colors.C}╠{'═'*(self.cols-2)}╣")
        print(f"{Colors.C}║ {Colors.BK}[NET]: {Colors.G}SECURE  {Colors.BK}[STATUS]: {Colors.Y}ONLINE  {Colors.BK}[DEV]: {Colors.W}CZUCA{Colors.C}{' '*(self.cols-45)}║")
        
        # Banner Print
        print(f"{Colors.C}╚{'═'*(self.cols-2)}╝{Colors.RESET}\n")
        
        if self.banner_text:
            lines = self.banner_text.strip().splitlines()
            for i, line in enumerate(lines):
                c = Colors.R if i % 2 == 0 else Colors.W
                print(f"{c}{Colors.W}{line}{Colors.RESET}")
        else:
            print(f"{Colors.C}=== TEAM-CZUCA ADVANCED TOOLKIT ==={Colors.RESET}")
        
        print(f"\n{Colors.BK}{'='*self.cols}{Colors.RESET}")

    def show_menu(self):
        while True:
            self.cols = get_cols() # Recalculate terminal size dynamically
            self.print_uca_header()
            
            # --- TARGET MENU ---
            print(f"\n {Colors.C}┌──[ {Colors.P}PAYLOAD LIST{Colors.C} ]")
            for index, item in enumerate(self.data_list, start=1):
                print(f" {Colors.C}├─[{Colors.W}{index:02d}{Colors.C}] {Colors.G}➢ {Colors.W}{item['name']}{Colors.RESET}")
            
            # --- OPTIONS ---
            print(f" {Colors.C}│")
            print(f" {Colors.C}├──[ {Colors.P}SYSTEM OVERRIDE{Colors.C} ]")
            print(f" {Colors.C}├─[{Colors.Y}88{Colors.C}] {Colors.Y}➢ SYSTEM UPDATE (CORE + ASSETS){Colors.RESET}")
            print(f" {Colors.C}└─[{Colors.R}00{Colors.C}] {Colors.R}➢ TERMINATE CONNECTION{Colors.RESET}")
            
            # --- INPUT TERMINAL ---
            try:
                print(f"\n {Colors.C}┌──[ {Colors.R}CZUCA {Colors.W}ROOT {Colors.C}]")
                choice = input(f" {Colors.C}└─➤ {Colors.Y}EXECUTE :: {Colors.W}").strip()
                print(Colors.RESET, end="")
                
                if choice == '00' or choice == '0':
                    print(f"\n {Colors.R}[!] CONNECTION TERMINATED. LOGGING OUT...{Colors.RESET}\n")
                    sys.exit(0)
                
                elif choice == '88':
                    # Trigger UCA 5-Step Update Loader
                    self.install_loaders_update()
                
                elif choice.isdigit():
                    choice_idx = int(choice)
                    if 1 <= choice_idx <= len(self.data_list):
                        self.open_link(self.data_list[choice_idx - 1]['url'])
                    else:
                        print(f" {Colors.R}[!] UNKNOWN TARGET ID.{Colors.RESET}")
                        time.sleep(1)
                else:
                    print(f" {Colors.R}[!] COMMAND NOT RECOGNIZED.{Colors.RESET}")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print(f"\n\n {Colors.R}[!] FORCE EXIT TRIGGERED. ABORTING...{Colors.RESET}")
                sys.exit(0)

# ==========================================
# 🚀 MAIN EXECUTION SYSTEM
# ==========================================
def main():
    app = TermuxToolkit()
    
    # 1. UCA Intro Boot Animation
    app.intro_animation()
    
    # 2. Open FB Page (Always on boot)
    app.open_facebook_page()
    
    # 3. Check and load internal database smoothly
    app.silent_startup_check()
    
    # 4. Display Premium Terminal Menu
    app.show_menu()

if __name__ == "__main__":
    main()
