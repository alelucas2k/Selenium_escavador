from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from handlers_factory import HandlerFactory

class ScraperFacade:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.handler_chain = HandlerFactory.criar_cadeia()

    def buscar_professor(self, professor):
        context = {'driver': self.driver, 'professor': professor}
        self.handler_chain.handle(context)

    def fechar(self):
        self.driver.quit()