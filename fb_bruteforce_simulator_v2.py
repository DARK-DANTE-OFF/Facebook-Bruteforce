import time
import random
import threading
from colorama import Fore
from queue import Queue

# CONFIGURATION
TARGET_EMAIL = "victime@example.com"
CORRECT_PASSWORD = "password123"
MAX_ATTEMPTS_BEFORE_CAPTCHA = 5  # Déclencheur CAPTCHA
THREADS = 5  # Nombre de threads parallèles
LOG_FILE = "bruteforce_log.txt"

# Variables globales
attempt_counter = 0
captcha_triggered = False
found = False
lock = threading.Lock()

def try_login(email, password):
    global attempt_counter, captcha_triggered, found

    with lock:
        if found:
            return
        attempt_counter += 1

        # Simuler un captcha après X tentatives
        if attempt_counter >= MAX_ATTEMPTS_BEFORE_CAPTCHA:
            captcha_triggered = True

        print(Fore.YELLOW + f"[•] Tentative : {email} | {password}")
        time.sleep(random.uniform(0.5, 1.2))  # Latence réseau simulée

        # Log chaque tentative
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"Tentative : {email} | {password}\n")

        if password == CORRECT_PASSWORD:
            found = True
            print(Fore.GREEN + f"\n[✓] Succès ! Mot de passe trouvé : {password}")
            return

def worker(q):
    while not q.empty() and not found:
        password = q.get()
        try_login(TARGET_EMAIL, password)
        q.task_done()

def main():
    print(Fore.CYAN + "=== FB Bruteforce Simulator v2 – DARK_DANTE_OFF Edition ===\n")
    wordlist_path = input(Fore.CYAN + "[+] Entrez le chemin du fichier wordlist : ")

    try:
        with open(wordlist_path, 'r') as file:
            passwords = [line.strip() for line in file.readlines()]

        q = Queue()
        for password in passwords:
            q.put(password)

        threads = []
        for _ in range(THREADS):
            t = threading.Thread(target=worker, args=(q,))
            t.start()
            threads.append(t)

        while any(t.is_alive() for t in threads):
            if captcha_triggered and not found:
                print(Fore.RED + "\n[!] CAPTCHA déclenché ! Le bruteforce est temporairement bloqué...")
                break
            time.sleep(0.5)

        if not found and not captcha_triggered:
            print(Fore.RED + "\n[✗] Mot de passe non trouvé dans la wordlist.")
    except FileNotFoundError:
        print(Fore.RED + "\n[!] Wordlist introuvable. Vérifiez le chemin !")

if __name__ == "__main__":
    main()
