import rumps
import subprocess

class FirewallIndicatorApp(rumps.App):
    def __init__(self):
        super(FirewallIndicatorApp, self).__init__("Firewall Status", icon=None, quit_button=None)
        self.menu = ["Firewall Status", "Quit"]
        self.icon_path_enabled = "enabled_icon.png"  # path to your firewall enabled icon
        self.icon_path_disabled = "disabled_icon.png"  # path to your firewall disabled icon
        self.update_firewall_status()

    def get_firewall_state(self):
        try:
            result = subprocess.run(
                ['defaults', 'read', '/Library/Preferences/com.apple.alf', 'globalstate'],
                capture_output=True,
                text=True
            )
            state = result.stdout.strip()
            return int(state)
        except Exception as e:
            print(f"Error reading firewall state: {e}")
            return None

    def update_firewall_status(self, _=None):
        state = self.get_firewall_state()
        if state == 0:
            self.title = "Firewall: Disabled"
            self.icon = self.icon_path_disabled
        elif state == 1 or state == 2:
            self.title = "Firewall: Enabled"
            self.icon = self.icon_path_enabled
        else:
            self.title = "Firewall: Unknown"

    @rumps.clicked("Firewall Status")
    def update_status(self, _):
        self.update_firewall_status()

    @rumps.clicked("Quit")
    def quit_app(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    app = FirewallIndicatorApp()
    app.run()

