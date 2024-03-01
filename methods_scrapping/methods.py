from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException, TimeoutException


def waiting_for_element_click(driver, xpath, time=30):

    """
        Aguarda o carregamento da pagina com o elemento desejado

        args: 
        driver = instancia do selenium
        xpath = xpathdo elemento
        time = tempo maximo de espera
        
    """

    while True:

        try:

            WebDriverWait(driver, time).until(ec.presence_of_element_located((By.XPATH, xpath))).click()
            return 'click exetudcado'

        except ElementClickInterceptedException as e:
     
            continue

        except StaleElementReferenceException as e:

            continue

        except Exception as e:

            return f'Nao foi possivel clicar no elemento - erro: {e}'
        

def transform_element_text(driver, xpath, time=30):

    """"
        Captura o texto do elemento

        args:
        driver = instancia do selenium
        xpath = xpath do elemento
        time = tempo maximo de espera

    """

    try:

        text = WebDriverWait(driver, time).until(ec.presence_of_element_located((By.XPATH, xpath))).text
        return text
    
    except TimeoutException as e:

        return ""
    
