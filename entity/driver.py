# import time
# import os
# import glob
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# # Configurando as opções do Chrome para abrir em tela cheia
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--start-maximized")
#
#
# servico = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=servico, options=chrome_options)
# driver.maximize_window()
#
# try:
#     # Acessar a página inicial do Escavador
#     driver.get("https://www.escavador.com/")
#
#     # Esperar até que a página carregue completamente
#     time.sleep(5)
#
#     # Mudar para o frame onde o campo de busca está localizado (se houver)
#     procurar = driver.find_element("xpath", "/html/body/div/div/main/div[2]/main/div/section[1]/div[3]/form/div[1]/input")
#     procurar.send_keys("Victor André Pinho de Oliveira")
#     time.sleep(5)
#
#     # clicar
#     clicar = driver.find_element("xpath", "/html/body/div/div/main/div[2]/main/div/section[1]/div[3]/form/div[1]/button")
#     clicar.click()
#     time.sleep(5)
#
#     print("Página carregada com sucesso!")
#
# except Exception as e:
#     print(f"Erro: {e}")
#
# finally:
#     driver.quit()
