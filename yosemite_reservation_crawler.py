import time
from selenium import webdriver
import logging
import requests


LOGGER = logging.getLogger(__name__)

hdlr = logging.FileHandler('log_yosemite.log')
LOGGER.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOGGER.addHandler(hdlr)

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
capabilities = webdriver.DesiredCapabilities().CHROME.copy()
capabilities["acceptSslCerts"] = True
browser = webdriver.Remote(command_executor="http://172.17.0.2:4444/wd/hub",
                           desired_capabilities=capabilities,
                           options=options)

LOGGER.info("looking for reservation availablity In Yosemite")
browser_url = 'https://www.recreation.gov/ticket/facility/300015'
browser.implicitly_wait(5)
browser.get(browser_url)
time.sleep(5)
browser.save_screenshot('before.png')
try:
    LOGGER.info("Trying to click")
    browser.find_element_by_class_name('SingleDatePickerInput_calendarIcon_1')\
        .click()
    time.sleep(3)
    browser.save_screenshot('after.png')
except Exception as ex:
    LOGGER.error("Exception caught while looking for css element: "
                 + str(ex))

all_spans = browser.find_elements_by_xpath(
    "//div[@class='CalendarMonth_caption CalendarMonth_caption_1']")
for span in all_spans:
    LOGGER.info(span.text.lower())
    # if "august" in span.text.lower():
    child2 = browser.find_element_by_class_name("CalendarDay__default_2")
    aria_label = child2.get_attribute("aria-label")
    LOGGER.info("Appointment for {}".format(aria_label))
    if "August 27, 2020" in aria_label or "August 28, 2020" in aria_label:
        LOGGER.info("FOUND THE DATE!!")
        try:
            browser.save_screenshot('after.png')
            url = "http://docker.for.mac.localhost:4545/text"
            LOGGER.info("Sending text")
            res = requests.post(url=url,
                                json={"title": "Book Yosemite Reservation",
                                      "text": "Reservation for {}. {}"
                                      .format(aria_label, browser_url)})
            LOGGER.info("Result of REST request is: " + str(res.status_code))
            url = "http://docker.for.mac.localhost:4545/email"
            LOGGER.info("Sending email")
            res = requests.post(url=url,
                                json={"title": "Book Yosemite Reservation",
                                      "text": "Reservation for {}. {}"
                                      .format(aria_label, browser_url)})
            LOGGER.info("Result of REST request is: " + str(res.status_code))
            url = "http://docker.for.mac.localhost:4545/notify"
            LOGGER.info("Sending mac notification")
            res = requests.post(url=url,
                                json={"title": "Book Yosemite Reservation",
                                      "text": "Reservation for {}. {}"
                                      .format(aria_label, browser_url)})
            LOGGER.info("Result of REST request is: " + str(res.status_code))
        except Exception as ex:
            LOGGER.error("Exception caught while sending notification: "
                         + str(ex))
        break
    else:
        break
browser.quit()
