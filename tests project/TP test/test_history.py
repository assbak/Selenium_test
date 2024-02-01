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

	
	
	
	

class LoginProcess(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
    def PageCon(self):
        driver = self.driver
        self.driver.get("https://katalon-demo-cura.herokuapp.com/")
        assert "CURA Healthcare Service" in driver.title
        
# CT1: Afficher profil utilisateur
    def test_profile1(self):
        driver = self.driver
        self.driver = self.PageCon()
        
        makepointbtn = driver.find_element(By.ID, "btn-make-appointment")
        time.sleep(5)
        #Récupérer l'élément correspondant au bouton de menu sur la page d'accueil et ouvrir le menu
        sideBarBtn = driver.find_element(By.ID, "menu-toggle")
        sideBarBtn.click()
        time.sleep(5)
        #LoginBtn = driver.find_element(By.XPATH, "//*[@id=\"sidebar-wrapper\"]/ul/li[3]/a")
        LoginNavBtn = driver.find_element(By.LINK_TEXT, "Login")
        time.sleep(2)
        LoginNavBtn.click()

        # #Vérifier que la page de login est bien affichée def Log_user
        assert EC.url_contains("login")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']")))
        #Récupérer les éléments correspondants aux champs de saisie du Login, du password et au bouton Login
        usernameTextbox = driver.find_element(By.ID,"txt-username")
        passwordTextbox = driver.find_element(By.ID,"txt-password")
        loginBtn = driver.find_element(By.ID,"btn-login")

        # #Saisir les identifiants et se connecter
        usernameTextbox.clear()
        usernameTextbox.send_keys("John Doe")

        passwordTextbox.clear()
        passwordTextbox.send_keys("ThisIsNotAPassword")

        loginBtn.click()

        # #Vérifier que l'utilisateur est bien connecté en s'assurant que le menu "Logout" est bien présent dans le menu
        # #Utiliser la fonction WebDriverWait pour attendre que l'élément "Logout" soit bien chargé dans le DOM avant de le récupérer
        logoutBtn = wait.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar-wrapper > ul > li:nth-child(6) > a")))
        assert logoutBtn.text in driver.page_source
        time.sleep(5)

        combofacBtn = driver.find_element(By.ID, "combo_facility")
        combofacBtn.click()
        combofacBtn1 = driver.find_element(By.XPATH, "//*[@id='combo_facility']/option[1]")
        combofacBtn1.click()
        time.sleep(5)
        radiofacBtn1 = driver.find_element(By.ID, "radio_program_medicare")
        radiofacBtn1.click()
        
        time.sleep(5)
        #Renseigner la date de RDV
        today = date.today()
        delta = timedelta(days=10)
        appointmentDate = today + delta
        appointmentDate = appointmentDate.strftime("%d/%m/%Y")
        driver.find_element(By.ID,"txt_visit_date").send_keys(appointmentDate)

        #Renseigner des commentaires
        driver.find_element(By.ID,"txt_comment").send_keys("Mon RDV")

        #Enregistrer le RDV
        driver.find_element(By.ID,"btn-book-appointment").click()

        #Valider que le RDV est bien enregistré
        self.assertIn(wait.WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"summary\"]/div/div/div[1]/h2"))).text, driver.page_source)

        time.sleep(5)
        #Récupérer l'élément correspondant au bouton de menu sur la page d'accueil et ouvrir le menu
        sideBarBtn = driver.find_element(By.ID, "menu-toggle")
        sideBarBtn.click()
        time.sleep(5)
        #LoginBtn = driver.find_element(By.XPATH, "//*[@id=\"sidebar-wrapper\"]/ul/li[3]/a")
        ProfilNavBtn = driver.find_element(By.LINK_TEXT, "History")
        ProfilNavBtn.click()
        time.sleep(2)
        LoginNavBtn.click()

    def tearDown(self):
        #Laisser le navigateur ouvert quelques secondes avant de le fermer
        wait.WebDriverWait(self.driver, 10)
        #Fermer le navigateur
        self.driver.quit()
        #self.driver.close()

if __name__ == '__main__':
    unittest.main()