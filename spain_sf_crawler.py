import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import notification
import logging
import requests


LOGGER = logging.getLogger(__name__)

hdlr = logging.FileHandler('log_spain_sf.log')
LOGGER.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
LOGGER.addHandler(hdlr)


browser = webdriver.Remote("http://172.17.0.3:4444/wd/hub",
                           DesiredCapabilities.CHROME)

LOGGER.info("looking for visa appointment at Spain Consulate in San Francisco")
url = 'https://app.bookitit.com/es/hosteds/widgetdefault/' \
      '21a8d76163e6f2dc0e5ca528c922d37c3#services'
browser.implicitly_wait(40)
browser.get(url)
time.sleep(15)
browser.save_screenshot('before.png')
try:
    browser.find_element_by_css_selector('#idListServices > '
                                         'div.clsBktServiceDataContainer'
                                         '.clsBktServiceAttMultiserviceNumber'
                                         '-1'
                                         '.clsBktServiceAttMultiservice-0'
                                         '.clsBktServiceAttParentGroup-bkt3851'
                                         '1 '
                                         '> div.clsBktServiceName.clsHP > '
                                         'a').click()
except Exception as ex:
    LOGGER.error("Exception caught while looking for css element: "
                 + str(ex))

time.sleep(10)

res = browser.current_url

LOGGER.info(res)

y = browser.find_element_by_css_selector("#idDivBktDatetimeSelectedDate")
LOGGER.info(y.text)

if 'noviembre' not in y.text.lower():
    # LOGGER.info("Mon")
    LOGGER.info("Appointment available for {}"
                .format(y.text.encode('utf-8')))
elif 'noviembre' in y.text.lower():
    LOGGER.debug("November IT IS!!")
    try:
        browser.save_screenshot('after.png')
        url = "http://docker.for.mac.localhost:4545/text"
        LOGGER.debug("Sending text")
        res = requests.post(url=url,
                            json={"title": "Book Spain Visa Appointment",
                                  "text": "Appointment available for {}"
                                  .format(y.text.encode('utf-8'))})
        LOGGER.info("Result of REST request is: " + str(res.status_code))
        LOGGER.debug("Sending Email")
        url = "http://docker.for.mac.localhost:4545/email"
        LOGGER.debug("Sending email")
        res = requests.post(url=url,
                            json={"title": "Book Spain Visa Appointment",
                                  "text": "Appointment available for {}"
                                  .format(y.text.encode('utf-8'))})
        LOGGER.info("Result of REST request is: " + str(res.status_code))
        url = "http://docker.for.mac.localhost:4545/notify"
        LOGGER.debug("Sending mac notification")
        res = requests.post(url=url,
                            json={"title": "Book Spain Visa Appointment",
                                  "text": "Appointment available for {}"
                                  .format(y.text.encode('utf-8'))})
        LOGGER.debug("Result of REST request is: " + str(res.status_code))
    except Exception as ex:
        LOGGER.error("Exception caught while sending notification: "
                     + str(ex))
# Closes the browser
browser.quit()
