from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

s = Service('./chromedriver')
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(15)

driver.get("https://account.mail.ru/login")
input_mail = driver.find_element(By.NAME, 'username')
input_mail.send_keys("study.ai_172@mail.ru")
input_mail.send_keys(Keys.ENTER)
input_mail = driver.find_element(By.NAME, "password")
input_mail.send_keys("NextPassword172#")
input_mail.send_keys(Keys.ENTER)
driver.find_element(By.CSS_SELECTOR, 'a.llc').click()

e_mails = []

while True:
    try:
        contact = driver.find_element(By.CLASS_NAME, 'letter-contact').text
        data = driver.find_element(By.CLASS_NAME, 'letter__date').text
        topic = driver.find_element(By.CLASS_NAME, 'thread-subject').text
        message = driver.find_element(By.TAG_NAME, 'tbody').text
        mail = {'contact': contact,
                'date': data,
                'topic': topic,
                'message': message,}
        e_mails.append(mail)
        driver.find_element(By.CLASS_NAME, 'button2__ico')
    except:
        print("Выход")
driver.close()

client = MongoClient('localhost', 27017)
email_db = client.email_db

for item in e_mails:
    email_db.mail.update_one({'date': e_mails['date']},
                                         {'$setOnInsert': {'contact': e_mails['contact'],
                                                           'topic': e_mails['topic'],
                                                           'message': e_mails['message']}},
                                         upsert=True)

