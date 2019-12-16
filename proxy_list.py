from selenium import webdriver
from pathlib import Path

co = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'

co.add_argument("log-level=3")
co.add_argument('--headless')
co.add_argument('--disable-gpu')
co.add_argument('--disable-dev-shm-usage')
# co.add_argument('--window-size=1920,1080')
# co.add_argument('--single-process')
co.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
co.add_argument('--user-agent={'+user_agent+'}')
co.add_argument('--allow-running-insecure-content')
co.add_argument('--disable-web-security')
co.add_argument('--no-referrers')
co.add_argument("'chrome.prefs': {'profile.managed_default_content_settings.images': 2}")

def get_proxies(co=co):
    import platform
    if platform.system() == 'Darwin':
        driver_path = Path('.') / 'webdriver/mac/chromedriver'
    else:
        driver_path = Path('.') / 'webdriver/linux/chromedriver'

    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=co)
    driver.get("https://free-proxy-list.net/")

    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES

