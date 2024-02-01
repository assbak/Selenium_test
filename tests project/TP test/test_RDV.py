import unittest
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
import time
import data
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

    
    def test_data_csv(self):
        file = r"c:\Users\Administrateur\Documents\GitHub\Selenium_test\tests project\TP test\data_RDV.csv"
        with open(file, mode='r', encoding="utf8") as f1:
            next(f1) # Skip the first line
            test_cases = []
            for idx, line in enumerate(f1):
                fields = line.strip().split(";")
                test_data = {}
                facility = {
                    "Tokyo Cura": "//*[@id='combo_facility']/option[1]",
                    "HongKong Cura": "//*[@id='combo_facility']/option[2]",
                    "Seoul Cura": "//*[@id='combo_facility']/option[3]"
                }
                Hosp_Read = {
                    "Not": "",
                    "Yes": "//*[@id='chk_hospotal_readmission']"
                }
                Program = {
                    "Medicaid": "radio_program_medicaid",
                    "Medicare": "radio_program_medicare",
                    "None": "radio_program_none"
                }
                Date = {
                    "Past month": -30,
                    "Next month": 30,
                    "current Month": 0
                }
                Comment = {
                    "Empty": "",
                    "With": "Merci pour votre prise de rendez vous, a bientot"
                }
                # test_data[fields[1]] = facility[fields[1]]
                # test_data[fields[2]] = Hosp_Read[fields[2]]
                # test_data[fields[3]] = Program[fields[3]]
                # test_data[fields[4]] = Date[fields[4]]
                # test_data[fields[5]] = Comment[fields[5]]
                test_datal = []
                
                test_datal.append(facility[fields[1]])
                test_datal.append( Hosp_Read[fields[2]])
                test_datal.append( Program[fields[3]])
                test_datal.append(Date[fields[4]])
                test_datal.append(Comment[fields[5]])
                test_cases.append(test_datal)
        print(test_cases)
        return test_cases
            
        
    def test_valid_RDV_MC(self):
        test_cases = self.test_data_csv()
        for test_case in test_cases:
            self.PageCon()
                
            makepointbtn = self.driver.find_element(By.ID, "btn-make-appointment")
            time.sleep(5)
            #Récupérer l'élément correspondant au bouton de menu sur la page d'accueil et ouvrir le menu
            sideBarBtn = self.driver.find_element(By.ID, "menu-toggle")
            sideBarBtn.click()
            time.sleep(5)
            #LoginBtn = driver.find_element(By.XPATH, "//*[@id=\"sidebar-wrapper\"]/ul/li[3]/a")
            LoginNavBtn = self.driver.find_element(By.LINK_TEXT, "Login")
            time.sleep(2)
            LoginNavBtn.click()

            # #Vérifier que la page de login est bien affichée def Log_user
            assert EC.url_contains("login")
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//label[text()='Username']")))
            #Récupérer les éléments correspondants aux champs de saisie du Login, du password et au bouton Login
            usernameTextbox = self.driver.find_element(By.ID,"txt-username")
            passwordTextbox = self.driver.find_element(By.ID,"txt-password")
            loginBtn = self.driver.find_element(By.ID,"btn-login")

            # #Saisir les identifiants et se connecter
            usernameTextbox.clear()
            usernameTextbox.send_keys("John Doe")

            passwordTextbox.clear()
            passwordTextbox.send_keys("ThisIsNotAPassword")

            loginBtn.click()
            # #Vérifier que l'utilisateur est bien connecté en s'assurant que le menu "Logout" est bien présent dans le menu
            # #Utiliser la fonction WebDriverWait pour attendre que l'élément "Logout" soit bien chargé dans le DOM avant de le récupérer
            logoutBtn = wait.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sidebar-wrapper > ul > li:nth-child(6) > a")))
            assert logoutBtn.text in self.driver.page_source
            time.sleep(5)

            combofacBtn = self.driver.find_element(By.ID, "combo_facility")
            combofacBtn.click()
            combofacBtn1 = self.driver.find_element(By.XPATH, test_case[0])
            combofacBtn1.click()
            time.sleep(5)
            if test_case[1] != "":
                checkbox = self.driver.find_element(By.XPATH, test_case[1])
                checkbox.click()
            radiofacBtn1 = self.driver.find_element(By.ID, test_case[2])
            radiofacBtn1.click()
                
            time.sleep(5)
            #Renseigner la date de RDV
            today = date.today()
            delta = timedelta(days = test_case[3])
            appointmentDate = today + delta
            appointmentDate = appointmentDate.strftime("%d/%m/%Y")
            self.driver.find_element(By.ID,"txt_visit_date").send_keys(appointmentDate)

                #Renseigner des commentaires
            if test_case[4] != "":
                self.driver.find_element(By.ID,"txt_comment").send_keys(test_case[4])

                #Enregistrer le RDV
            self.driver.find_element(By.ID,"btn-book-appointment").click()

                #Valider que le RDV est bien enregistré
            self.assertIn(wait.WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"summary\"]/div/div/div[1]/h2"))).text, self.driver.page_source)


            time.sleep(5)
            sideBarBtn = self.driver.find_element(By.ID, "menu-toggle")
            sideBarBtn.click()
            time.sleep(5)
            #LoginBtn = driver.find_element(By.XPATH, "//*[@id=\"sidebar-wrapper\"]/ul/li[3]/a")
            LogoutNavBtn = self.driver.find_element(By.LINK_TEXT, "Logout")
            time.sleep(2)
            LogoutNavBtn.click()
    
            
       
        

    
    def tearDown(self):
        self.driver.quit()
    #     #Laisser le navigateur ouvert quelques secondes avant de le fermer
    #     wait.WebDriverWait(self.driver, 10)
    #     #Fermer le navigateur
    #     #self.driver.close()

if __name__ == '__main__':
    unittest.main()