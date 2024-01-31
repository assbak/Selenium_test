import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        self.driver.get("https://katalon-demo-cura.herokuapp.com/")
        
        login_button = self.driver.find_element_by_link_text('Login')
        login_button.click()
        
        username = self.driver.find_element_by_name('username')
        password = self.driver.find_element_by_name('password')

        username.send_keys('your_username')
        password.send_keys('your_password')

        password.submit()

        time.sleep(10)

if __name__ == "__main__":
    unittest.main()

