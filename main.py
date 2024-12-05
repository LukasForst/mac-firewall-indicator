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
                ['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getglobalstate'],
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Error reading firewall state: {e}")
            return None

    def update_firewall_status(self, _=None):
        state = self.get_firewall_state()
        if 'Firewall is disabled.' in state or 'State = 0' in state:
            self.title = "Firewall: Disabled"
            self.icon = self.icon_path_disabled
        elif 'Firewall is enabled.' in state or 'State = 1' in state:
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

