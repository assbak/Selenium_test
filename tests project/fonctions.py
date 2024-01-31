from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
import time
def Loginprocess(link):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(link)

    assert "CURA Healthcare Service" in driver.title

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

    # #Vérifier que la page de login est bien affichée
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
    # #Laisser le navigateur ouvert quelques secondes avant de le fermer
    wait.WebDriverWait(driver, 5)