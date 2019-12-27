import time
from selenium.common.exceptions import TimeoutException
from common_functions import *
import json
from yahooHandle import YahooHandle
from pathlib import Path


class LinkedInHandle():
    """docstring for LinkedIn"""

    def __init__(self, executor):
        super(LinkedInHandle, self).__init__()
        self.driver = executor.driver
        self.logger = executor.logger
        self.socketio = executor.socketio
        self.screenshot = executor.screenshot
        self.account = executor.account
        self.yahooHandle = YahooHandle(executor)
        self.session_id = executor.session_id

        self.login_url = "https://www.linkedin.com/login"
        self.logout_url = "https://www.linkedin.com/mynetwork/import-contacts/"
        self.check_login_url = "https://www.linkedin.com/mynetwork/import-contacts/"
        self.import_url = "https://www.linkedin.com/mynetwork/import-contacts/"
        self.export_url = "https://www.linkedin.com/mynetwork/import-contacts/saved-contacts/"

    def login(self):
        self.driver.get(self.login_url)
        credentials = self.account.get('linkedIn')
        username = credentials.get('username')
        password = credentials.get('password')
        if search_element_by_id(self.driver, 'username'):
            try:
                user = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
                user.send_keys(username)
                pwd = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
                pwd.send_keys(password)
                # submit_form
                login = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app__container"]/main/div/form/div[3]/button')))
                login.click()
                time.sleep(1)
                self.check_email_login_otp_verification()
                if self.is_logged_in():
                    return True
                else:
                    return False
            except Exception as e:
                return False
        else:
            return False

    def logout(self):
        try:
            self.driver.get(self.logout_url)
            clk = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-trigger"]')))
            clk.click()
            time.sleep(2)
            # Logout
            logout = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="nav-settings__dropdown-options"]/li[5]/ul/li')))
            logout.click()
            time.sleep(2)
            return True
        except:
            return False

    def is_logged_in(self):
        try:
            p_info_title = self.driver.wait.until(
                EC.visibility_of_any_elements_located((By.CSS_SELECTOR, "#mynetwork-tab-icon")))
            if p_info_title:
                return True
            else:
                return False
        except TimeoutException:
            return False


    def check_email_login_otp_verification(self):
        try:
            email_verification_link_present = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "input__email_verification_pin")))
            if email_verification_link_present:
                self.socketio.emit('action', 'Email verification required for linked in login')
                otp_payload = {
                    'input_type': 'otp',
                    'handler': 'linkedIn',
                    'key': 'email_login_otp',
                    'message': 'Linked In Login OTP'
                }
                self.socketio.emit('prompt_user', json.dumps(otp_payload))
                otp_entered = WebDriverWait(self.driver, 100).until(lambda driver: len(
                    driver.find_element_by_css_selector("#input__email_verification_pin").get_attribute("value")) == 6)
                if otp_entered:
                    confirm_btn = self.driver.wait.until(
                        EC.presence_of_element_located((By.ID, "email-pin-submit-button")))
                    confirm_btn.click()
                    time.sleep(1)
                else:
                    pass
            else:
                pass
        except TimeoutException:
            pass

    def submit_email_login_otp(self, otp):
        otp_input = self.driver.wait.until(EC.presence_of_element_located((By.ID, "input__email_verification_pin")))
        otp_input.send_keys(otp)




    def import_contacts(self,provider):
        self.driver.get(self.import_url)
        self.socketio.emit('action', 'Importing contact from ' + provider)
        email_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@aria-describedby=\"artdeco-hoverable-"+provider+"-icon\"]")))
        email_btn.click()
        time.sleep(2)

        confirm_oauth = False
        if provider == 'yahoo':
            confirm_oauth = self.yahooHandle.confirm_import()
        if confirm_oauth:
            try:
                time.sleep(5)
                select_all_checkbox = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.mn-abi-results__nav-item-checkbox label")))
                select_all_checkbox.click()
                time.sleep(5)

                add_confirm_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ember313")))
                add_confirm_btn.click()
                time.sleep(5)

                skip_connection_btn = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ember445")))
                skip_connection_btn.click()
                time.sleep(5)
                return True
            except Exception as ex:
                print(ex)
                return False
        return True


    def export_contacts(self, email):
        self.driver.get(self.export_url)
        contactList = []
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
        except Exception as e:
            pass

        try:
            time.sleep(5)
            # Total Contacts
            # summary = find_element_by_xpath_with_timeout(self.driver, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p', [], 10)
            summary = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ember42"]/div/div/div[1]/div/section/div[1]/p')))
            totalContacts = int(summary.text.split(" ")[0])
            self.socketio.emit("action", "Total contacts found : " + str(totalContacts))
            time.sleep(1)
            # scroll to bottom
            prompt = 0
            while prompt < 100:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(0.2)
                prompt += 1

            listResults = self.driver.find_elements_by_xpath('//ul[@class="abi-saved-contacts__contact-list"]/li')
            if len(listResults) > 0:
                print("Exporting of contacts is In progress")
                print("____________________________")
                for people in listResults:
                    contactDetails = {}
                    contactDivId = people.get_attribute('id')

                    unwantedTextSelector = 'div.abi-saved-contacts-row__details > button > div.abi-saved-contacts-contact-summary > div > span.contact-summary__name.t-sans.t-16.t-black.t-bold.mr1 > span'
                    linkedInNameSelector = 'div.abi-saved-contacts-row__details > button > div.abi-saved-contacts-contact-summary > div > span.contact-summary__name.t-sans.t-16.t-black.t-bold.mr1'
                    linkedInDesignationSelector = 'div.abi-saved-contacts-row__details > button > div.abi-saved-contacts-contact-summary > p'
                    unwantedText = people.find_element_by_css_selector(unwantedTextSelector).text
                    linkedInName = people.find_element_by_css_selector(linkedInNameSelector).text
                    linkedInName = linkedInName.replace(unwantedText, '').strip('\n')
                    linkedInName = linkedInName.replace(unwantedText, '').strip(' ')
                    try:
                        linkedInDesignation = people.find_element_by_css_selector(linkedInDesignationSelector).text
                    except Exception as e:
                        linkedInDesignation = ''

                    # open modal to get email & linkedIn Url
                    contactClk = self.driver.find_element_by_xpath(
                        '//*[@id="' + contactDivId + '"]/div[@class="abi-saved-contacts-row__details"]/button[@class="abi-saved-contacts-row__description"]')
                    self.driver.execute_script("arguments[0].click();", contactClk)
                    time.sleep(0.2)
                    # get details from linkedin
                    count = 1
                    contactDetailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div'
                    linkedContactDetails = self.driver.find_elements_by_xpath(contactDetailSelector)
                    # Default email selector
                    linkedInEmailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div[1]/p'
                    for detail in linkedContactDetails:
                        label = detail.find_element_by_xpath('.//label').text
                        if label == 'Email address':
                            linkedInEmailSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[2]/div[' + str(
                                count) + ']/p'
                            break
                        count += 1

                    linkedInUrlSelector = '//*[@id="artdeco-modal-outlet"]/div/div/div[2]/div/div/div[1]/div[2]/div/div/span/a'
                    linkedInEmail = self.driver.find_element_by_xpath(linkedInEmailSelector).text
                    try:
                        linkedInUrl = self.driver.find_element_by_xpath(linkedInUrlSelector).get_attribute('href')
                    # linkedInUrl = 'https://www.linkedin.com'+linkedInUrl
                    except Exception as e:
                        linkedInUrl = ''

                    # clode modal
                    cancelSelector = '//*[@id="artdeco-modal-outlet"]/div/div/button'
                    # cancelClk = find_element_by_xpath_with_timeout(self.driver, cancelSelector, [], 10)
                    cancelClk = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, cancelSelector)))
                    self.driver.execute_script("arguments[0].click();", cancelClk)
                    contactDetails = [linkedInEmail, linkedInName, linkedInDesignation, linkedInUrl]
                    contactList.append(contactDetails)
                self.process_contacts(contactList, email.get('username'))
            return True
        except Exception as e:
            return False




    def process_contacts(self, contacts, source_id):
        import csv

        csv_path = 'static/csv/' + self.session_id
        Path(csv_path).mkdir(parents=True, exist_ok=True)
        filename = csv_path + "/" + source_id.replace('.', '') + '.csv'

        with open(filename, 'w') as outcsv:
            writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            writer.writerow(['Email', 'Name', 'Designation', 'Profile'])
            for item in contacts:
                writer.writerow([item[0], item[1], item[2], item[3]])



