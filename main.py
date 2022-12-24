from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from conf import password, phones_code


class Telegram_user_finder():
    def __init__(self, password=None, phone=None):
        # Заменить, если будет другой браузер
        # Инициализация браузера
        self.driver = webdriver.Chrome()
        # Явное ожидание
        self.wait = wait = WebDriverWait(self.driver, 10)
        # Пароль для двуэтапной авторизации
        self.password = password 
        # Номер телефона, с которого начать надо
        self.phone = phone if phone else "9000000001"
        
    

    def login(self):
        '''
        Вставляем пароль и жмём на подтверждение
        '''
        password_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"auth-pages\"]/div/div[2]/div[5]/div/div[2]/div/input[2]")))
        password_input.send_keys(self.password)

        confirm_bttn = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id=\"auth-pages\"]/div/div[2]/div[5]/div/div[2]/button")))
        confirm_bttn.click()


    def open_addUser_menu(self):
        '''
        Открываем двумя нажатиями меню контактов
        '''
        side_bar_opener = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'sidebar-tools-button')]")))
        side_bar_opener.click()

        contacts = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'tgico-user')]")))
        contacts.click()

        # Без ожидания не всегда контакты успевают прогрузиться
        time.sleep(1)


    def add_user(self, name="."):
        '''
        Добавляем пользователя в меню контактов
        '''
        # Кнопка начала добавления
        add_user = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(@class, 'tgico-add')]")))
        add_user.click()

        # Вводим имя
        add_user = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div[2]/div[1]/div[1]")))
        add_user.send_keys(name)

        # Телефон
        add_user = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div[3]/div[1]")))
        add_user.send_keys(self.phone)

        # Confirm
        add_user = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div[1]/button")))
        add_user.click()

        # Если не получилось добавить номер
        try:
            add_user = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/div[1]/span")))
            add_user.click()
            print("Телефон:", self.phone, "ошибка добавления")
        except Exception:
            print("Телефон:", self.phone)
        

    def start(self):
        self.driver.get("https://web.telegram.org/k/")
        
        if self.password:
            self.login()

        self.open_addUser_menu()

        while self.phone != None:
            self.add_user()
            self.get_phone()
        

    def get_phone(self):
        '''
        Получаем следующий телефон
        '''
        phone = int(self.phone)

        self.phone = phone + 1


a = Telegram_user_finder(password)
a.start()

