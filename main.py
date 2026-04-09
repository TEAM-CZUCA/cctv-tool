#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil
import platform
import urllib.request
import subprocess

# ==========================================
# ⚙️ CONFIGURATION & VERSIONING
# ==========================================
VERSION = "1.1.0"  # আপনার বর্তমান টুলের ভার্সন
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/TEAM-CZUCA/termux-setup/main/version.txt"
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
# 🎨 UCA COLORS
# ==========================================
class Colors:
    R = '\033[1;31m'
    G = '\033[1;32m'
    C = '\033[1;36m'
    Y = '\033[1;33m'
    P = '\033[1;35m'
    W = '\033[1;37m'
    BK = '\033[1;30m'
    RESET = '\033[0m'

def get_cols():
    try: return shutil.get_terminal_size().columns
    except: return 60

# ==========================================
# 🧠 TOOLKIT CORE CLASS
# ==========================================
class TermuxToolkit:
    def __init__(self):
        self.data_list = []
        self.banner_text = ""
        self.cols = get_cols()

    def clear_screen(self):
        os.system('cls' if platform.system() == "Windows" else 'clear')

    # --- 1. GITHUB VERSION CHECK ---
    def check_for_updates(self):
        sys.stdout.write(f"{Colors.BK} [CHECK] VERIFYING VERSION WITH CZUCA SERVER...{Colors.RESET}")
        sys.stdout.flush()
        try:
            req = urllib.request.Request(REMOTE_VERSION_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                remote_version = response.read().decode('utf-8').strip()
                if remote_version != VERSION:
                    sys.stdout.write(f"\r {Colors.Y}[!] NEW UPDATE DETECTED: {remote_version} (Current: {VERSION}){Colors.RESET}\n")
                    return True
                else:
                    sys.stdout.write(f"\r {Colors.G}[✔] SYSTEM IS UP TO DATE (v{VERSION}){' '*20}{Colors.RESET}\n")
                    return False
        except:
            sys.stdout.write(f"\r {Colors.R}[!] FAILED TO CHECK UPDATES (OFFLINE MODE){' '*15}{Colors.RESET}\n")
            return False

    # --- 2. UCA INTRO ANIMATION ---
    def intro_animation(self):
        self.clear_screen()
        print(f"\n{Colors.BK} [INIT] ESTABLISHING CONNECTION TO CZUCA SERVER...{Colors.RESET}")
        time.sleep(0.3)
        logs = ["LOADING_CZUCA_MODULES", "VERIFYING_USER_PERMISSIONS", "FETCHING_THEME_DATABASE", "ACCESS_GRANTED"]
        for log in logs:
            sys.stdout.write(f"\r {Colors.C}:: SYSTEM_BOOT >> {log:<30} {Colors.G}[OK]{Colors.RESET}")
            time.sleep(0.1)
            print()

    # --- 3. AUTO UPDATE & SELF REPLACEMENT ---
    def install_loaders_update(self):
        self.clear_screen()
        print(f"\n{Colors.G}[*] INITIALIZING SYSTEM OVERRIDE (UPDATE PROTOCOL)...{Colors.RESET}\n")
        
        # আপডেট এর ধাপগুলো
        steps = [
            ("SYNCING GITHUB REPO", self._git_sync),
            ("UPGRADING PACKAGES", self._pkg_upgrade),
            ("INSTALLING DEPENDENCIES", self._pip_requirements),
            ("FETCHING LATEST ASSETS", self._fetch_assets)
        ]
        
        for step_name, func in steps:
            print(f" {Colors.C}[PROCESS] {step_name:<30} ", end="", flush=True)
            try:
                func()
                print(f"{Colors.G}[DONE]{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.R}[FAIL]{Colors.RESET}")
            time.sleep(0.3)
        
        print(f"\n{Colors.Y} [LOG] SYSTEM REBOOTING TO APPLY CHANGES...{Colors.RESET}")
        time.sleep(1.5)
        
        # সেলফ-রিস্টার্ট (Self-Replacement Logic)
        os.execv(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:])

    def _git_sync(self):
        # গিট রিপোজিটরি আপডেট করবে
        if os.path.exists(".git"):
            subprocess.run(['git', 'pull', 'origin', 'main'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # যদি গিট না থাকে তবে সরাসরি ফাইল ডাউনলোড করবে (আগের মত)
            req = urllib.request.Request(REMOTE_CORE_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                with open(os.path.abspath(__file__), 'w', encoding='utf-8') as f:
                    f.write(response.read().decode('utf-8'))

    def _pkg_upgrade(self):
        if shutil.which("pkg"):
            os.system("pkg update -y && pkg upgrade -y > /dev/null 2>&1")

    def _pip_requirements(self):
        if os.path.exists("requirements.txt"):
            os.system("pip install -r requirements.txt --quiet")

    def _fetch_assets(self):
        # ব্যানার ও লিস্ট আপডেট
        urllib.request.urlretrieve(REMOTE_BANNER_URL, BANNER_FILE)
        urllib.request.urlretrieve(REMOTE_LIST_URL, LOCAL_LIST)

    def silent_startup_check(self):
        """ডাটা লোড করা"""
        if os.path.exists(BANNER_FILE):
            with open(BANNER_FILE, 'r', encoding='utf-8') as f: self.banner_text = f.read()
        if os.path.exists(LOCAL_LIST):
            with open(LOCAL_LIST, 'r', encoding='utf-8') as f: self._parse_data(f.read())

    def _parse_data(self, raw_text):
        self.data_list = []
        for line in raw_text.strip().splitlines():
            if '|' in line:
                name, url = line.split('|', 1)
                self.data_list.append({"name": name.strip(), "url": url.strip()})

    def open_link(self, url):
        print(f"\n {Colors.C}└─➤ {Colors.W}Launching Target...{Colors.RESET}")
        try:
            subprocess.run(['termux-open-url', url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            import webbrowser
            webbrowser.open(url)
        time.sleep(1)

    def print_uca_header(self):
        self.clear_screen()
        print(f"{Colors.C}╔{'═'*(self.cols-2)}╗")
        title = f" {Colors.R}● {Colors.W}CZUCA TERMINAL v{VERSION} {Colors.R}● "
        pad = (self.cols - len(title) + 12) // 2
        print(f"{Colors.C}║{' '*pad}{title}{' '*(self.cols-len(title)-pad+12)}{Colors.C}║")
        print(f"{Colors.C}╠{'═'*(self.cols-2)}╣")
        print(f"{Colors.C}╚{'═'*(self.cols-2)}╝{Colors.RESET}\n")
        if self.banner_text: print(f"{Colors.W}{self.banner_text}{Colors.RESET}")
        print(f"{Colors.BK}{'='*self.cols}{Colors.RESET}")

    def show_menu(self):
        while True:
            self.cols = get_cols()
            self.print_uca_header()
            print(f"\n {Colors.C}┌──[ {Colors.P}PAYLOAD LIST{Colors.C} ]")
            for index, item in enumerate(self.data_list, start=1):
                print(f" {Colors.C}├─[{Colors.W}{index:02d}{Colors.C}] {Colors.G}➢ {Colors.W}{item['name']}{Colors.RESET}")
            
            print(f" {Colors.C}│\n {Colors.C}├──[ {Colors.P}SYSTEM OPTIONS{Colors.C} ]")
            print(f" {Colors.C}├─[{Colors.Y}88{Colors.C}] {Colors.Y}➢ FULL SYSTEM UPDATE{Colors.RESET}")
            print(f" {Colors.C}└─[{Colors.R}00{Colors.C}] {Colors.R}➢ TERMINATE{Colors.RESET}")
            
            try:
                choice = input(f"\n {Colors.C}┌──[ {Colors.R}CZUCA{Colors.C} ]\n └─➤ {Colors.Y}EXECUTE :: {Colors.W}").strip()
                if choice == '00': break
                elif choice == '88': self.install_loaders_update()
                elif choice.isdigit() and 1 <= int(choice) <= len(self.data_list):
                    self.open_link(self.data_list[int(choice)-1]['url'])
            except KeyboardInterrupt: break

# ==========================================
# 🚀 MAIN EXECUTION
# ==========================================
def main():
    app = TermuxToolkit()
    app.intro_animation()
    
    # বুট হওয়ার সময় ভার্সন চেক
    if app.check_for_updates():
        up_choice = input(f"\n {Colors.Y}[?] Do you want to update to the latest version? (y/n): {Colors.RESET}").lower()
        if up_choice == 'y':
            app.install_loaders_update()

    # ফেসবুক পেজ ওপেন (ঐচ্ছিক - আপনি চাইলে সরাতে পারেন)
    # subprocess.run(['termux-open-url', FB_PAGE_URL], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    app.silent_startup_check()
    app.show_menu()

if __name__ == "__main__":
    main()
