from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

s = Service('./chromedriver')
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(15)
actions = ActionChains(driver)

driver.get("https://account.mail.ru/login")
input_mail = driver.find_element(By.NAME, 'username')
input_mail.send_keys("study.ai_172@mail.ru")
input_mail.send_keys(Keys.ENTER)
input_mail = driver.find_element(By.NAME, "password")
input_mail.send_keys("NextPassword172#")
input_mail.send_keys(Keys.ENTER)
#Открываем первое письмо
driver.find_element(By.CSS_SELECTOR, 'a.llc').click()

#Создаем пустой список для загрузки в него данных из почты
e_mails = []

#Запускаем бесконечный цикл... правда, работает он немного странно, до конца ни разу не доходил,
# максимум на 17 письме вылетает
while True:
     try:
         contact = driver.find_element(By.CLASS_NAME, 'letter-contact').text
         data = driver.find_element(By.CLASS_NAME, 'letter__date').text
         topic = driver.find_element(By.CLASS_NAME, 'thread-subject').text
         message = driver.find_element(By.CLASS_NAME, 'letter-body__body-content').text
         mail = {'contact': contact,
                 'date': data,
                 'topic': topic,
                 'message': message,}
         e_mails.append(mail)
         #не смог через селектор выбрать кнопку прокрутки писем внутри письма (стрелка вниз),
         # поэтому воспользовался комбинацией клавиш Ctrl + стрелка вниз
         actions.key_down(Keys.CONTROL).key_down(Keys.DOWN).key_up(Keys.DOWN).key_up(Keys.CONTROL)
         actions.perform()
     except:
         break

driver.close()

client = MongoClient('localhost', 27017)
email_db = client.email_db
for item in e_mails:
     email_db.mail.update_one({'date': e_mails[0]},
                             {'$setOnInsert': {'contact': e_mails[1],
                             'topic': e_mails[2],
                             'message': e_mails[3]}},
                             upsert=True)

