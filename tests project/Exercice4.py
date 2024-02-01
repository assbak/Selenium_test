import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
import time
from selenium.webdriver.support.ui import Select
from datetime import date
from datetime import timedelta
class BasePage:
    def __init__(self, driver):
        self.driver = driver

class HomePage(BasePage):
    def navigate(self):
        self.driver.get("https://katalon-demo-cura.herokuapp.com/")

    def open_nav(self):
        sideBarBtn = self.driver.find_element(By.ID, "menu-toggle")
        sideBarBtn.click()

    def click_login(self):
        LoginNavBtn = self.driver.find_element(By.LINK_TEXT, "Login")
        LoginNavBtn.click()
    def book_appointment(self, facility, program, visit_date, comment):
        combofacBtn = self.driver.find_element(By.ID, "combo_facility")
        combofacBtn.click()
        combofacBtn1 = self.driver.find_element(By.XPATH, f"//*[@id='combo_facility']/option[@value='{facility}']")
        combofacBtn1.click()
        time.sleep(5)
        radiofacBtn1 = self.driver.find_element(By.ID, program)
        radiofacBtn1.click()
        
        time.sleep(5)
        #Renseigner la date de RDV
        self.driver.find_element(By.ID,"txt_visit_date").send_keys(visit_date)

        #Renseigner des commentaires
        self.driver.find_element(By.ID,"txt_comment").send_keys(comment)

        #Enregistrer le RDV
        self.driver.find_element(By.ID,"btn-book-appointment").click()

        #Valider que le RDV est bien enregistré
        self.assertIn(wait.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"summary\"]/div/div/div[1]/h2"))).text, self.driver.page_source)

class LoginPage(BasePage):
    def enter_credentials(self, username, password):
        usernameTextbox = self.driver.find_element(By.ID,"txt-username")
        passwordTextbox = self.driver.find_element(By.ID,"txt-password")

        usernameTextbox.clear()
        usernameTextbox.send_keys(username)

        passwordTextbox.clear()
        passwordTextbox.send_keys(password)

    def click_login_button(self):
        loginBtn = self.driver.find_element(By.ID,"btn-login")
        loginBtn.click()

    def verify_logged_in(self):
        logoutBtn = wait.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar-wrapper > ul > li:nth-child(6) > a")))
        return logoutBtn.text in self.driver.page_source
class LoginProcess(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.home_page = HomePage(self.driver)
        self.login_page = LoginPage(self.driver)

    def test_invalid_pw_user_login(self):
        self.home_page.navigate()
        self.home_page.open_nav()
        self.home_page.click_login()

        assert EC.url_contains("login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']")))

        self.login_page.enter_credentials("John Doe", "ThisIsAPassword")
        self.login_page.click_login_button()

        assert self.login_page.verify_logged_in()

    def test_invalid_username_login(self):
        self.home_page.navigate()
        self.home_page.open_nav()
        self.home_page.click_login()

        assert EC.url_contains("login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']")))

        self.login_page.enter_credentials("Jack", "ThisIsNotAPassword")
        self.login_page.click_login_button()

        assert self.login_page.verify_logged_in()

    def test_valid_RDV(self):
        self.home_page.navigate()
        self.home_page.open_nav()
        self.home_page.click_login()

        assert EC.url_contains("login")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']")))

        self.login_page.enter_credentials("John Doe", "ThisIsNotAPassword")
        self.login_page.click_login_button()

        assert self.login_page.verify_logged_in()

        today = date.today()
        delta = timedelta(days=10)
        appointmentDate = today + delta
        appointmentDate = appointmentDate.strftime("%d/%m/%Y")
        self.home_page.book_appointment("1", "radio_program_medicare", appointmentDate, "Mon RDV")

    def tearDown(self):
        wait.WebDriverWait(self.driver, 10)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
