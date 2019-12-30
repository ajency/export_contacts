from yahooHandle import YahooHandle


class AolHandle(YahooHandle):
    """docstring for Aol"""

    def __init__(self, executor):
        self.driver = executor.driver
        self.logger = executor.logger
        self.socketio = executor.socketio
        self.screenshot = executor.screenshot
        self.account = executor.account

        self.login_url = "https://login.aol.com/account/"
        self.logout_url = "https://login.aol.com/account/"
        self.check_login_url = "https://login.aol.com/account/"