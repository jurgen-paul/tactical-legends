public class Main {
    // ANSI escape codes
    public static final String RESET = "\u001B[0m";
    public static final String CYAN = "\u001B[36m";
    public static final String YELLOW = "\u001B[33m";
    public static final String GREEN = "\u001B[32;1m"; // bright green
    public static final String RED = "\u001B[31;1m";   // bright red
    public static final String BEEP = "\u0007";        // ASCII bell (beep)

    public static void main(String[] args) {
        // Intro banner
        System.out.println(CYAN + "===============================================" + RESET);
        System.out.println(CYAN + "        ⚔️  Tactical Legends ⚔️" + RESET);
        System.out.println(CYAN + "         Rise of the Oistarian" + RESET);
        System.out.println(CYAN + "===============================================" + RESET);
        System.out.println("Prepare to command elite squads, forge relics,");
        System.out.println("and shape the fate of Oistaria.\n");

        // Simulation initialization
        System.out.println(">>> Initializing battlefield simulation...");
        for (int i = 1; i <= 5; i++) {
            System.out.print(YELLOW + "Loading unit " + i + " " + RESET);
            animateDots(3, 250); // Show animated dots
            try {
                Thread.sleep(400); // Simulate loading delay
                System.out.println(GREEN + "✅ Ready" + RESET);
            } catch (InterruptedException e) {
                flashRedWarning("Initialization interrupted!");
                showCriticalOverrideBanner();
            }
        }

        // Final status
        System.out.println(CYAN + "\n===============================================" + RESET);
        System.out.println(GREEN + "   All units deployed. Tactical systems online." + RESET);
        System.out.println(CYAN + "===============================================" + RESET);
        System.out.println(GREEN + "⚡ Let the legend begin... ⚡" + RESET);
    }

    /**
     * Utility method to animate loading dots
     */
    private static void animateDots(int count, int delay) {
        for (int i = 0; i < count; i++) {
            try {
                Thread.sleep(delay);
            } catch (InterruptedException e) {
                // Ignore interruption for animation
            }
            System.out.print(".");
        }
    }

    /**
     * Flash a red warning message with an audible beep
     */
    private static void flashRedWarning(String message) {
        for (int i = 0; i < 3; i++) {
            System.out.println(RED + message + BEEP + RESET); // red + beep
            try {
                Thread.sleep(300);
            } catch (InterruptedException ignored) {}
            System.out.println(RESET); // Clear/reset
            try {
                Thread.sleep(200);
            } catch (InterruptedException ignored) {}
        }
    }

    /**
     * Show dramatic ASCII banner for critical override
     */
    private static void showCriticalOverrideBanner() {
        System.out.println(RED + BEEP);
        System.out.println(RED + "################################################" + RESET);
        System.out.println(RED + "###   !!! CRITICAL SYSTEMS OVERRIDE !!!      ###" + RESET);
        System.out.println(RED + "###   Tactical Command Lockdown Engaged      ###" + RESET);
        System.out.println(RED + "################################################" + RESET);
        System.out.println(RED + BEEP);
    }
}

