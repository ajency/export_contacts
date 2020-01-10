from .driver import Driver

def get_proxies():
    web_driver = Driver(None)
    driver = web_driver.initialize_chrome_driver(True, [])

    driver.get("https://free-proxy-list.net/")
    PROXIES = []
    proxies = driver.find_elements_by_css_selector("tr[role='row']")
    for p in proxies:
        result = p.text.split(" ")

        if result[-1] == "yes":
            PROXIES.append(result[0]+":"+result[1])

    driver.close()
    return PROXIES

