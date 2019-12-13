from selenium import webdriver
from pathlib import Path

co = webdriver.ChromeOptions()
co.add_argument("log-level=3")
co.add_argument("--headless")

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

