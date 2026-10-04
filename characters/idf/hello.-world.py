#!/usr/bin/env python3
"""
Tactical Legends - Characters/IDF Module Initializer & Diagnostics
"""

import time
import sys

RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
GREEN = "\033[32;1m"
RED = "\033[31;1m"


def animate_dots(count=3, delay=0.1):
    for _ in range(count):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(delay)


def main():
    print(CYAN + "===============================================" + RESET)
    print(CYAN + "        ⚔️  Tactical Legends ⚔️" + RESET)
    print(CYAN + "      IDF Tactical Operatives Engine" + RESET)
    print(CYAN + "===============================================" + RESET)
    print("Prepare to command elite squads, forge relics,")
    print("and shape the fate of Oistaria.\n")

    print(">>> Initializing IDF operative roster...")
    for i in range(1, 6):
        sys.stdout.write(YELLOW + f"Loading unit {i} " + RESET)
        animate_dots(3, 0.05)
        time.sleep(0.05)
        print(GREEN + " ✅ Ready" + RESET)

    print(CYAN + "\n===============================================" + RESET)
    print(GREEN + "   All units deployed. Tactical systems online." + RESET)
    print(CYAN + "===============================================" + RESET)
    print(GREEN + "⚡ Let the legend begin... ⚡" + RESET)


if __name__ == "__main__":
    main()
