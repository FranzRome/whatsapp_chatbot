from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# import sys
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


class WhatsappChatbot:
    
    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def login(self):
        driver = self.driver
        driver.get('https://web.whatsapp.com/')
        input("Login with QR code, select a chat and press ENTER to continue")

    def new_tab(self, url):
        self.driver.execute_script('window.open("''' + url + '''", "_blank");''')
        self.driver.implicitly_wait(10)

    def switch_tab(self, index):
        driver = self.driver
        handles = driver.window_handles
        driver.switch_to.window(handles[index])
        driver.implicitly_wait(10)

    def open_wiki_tab(self):
        self.new_tab("https://it.wikipedia.org/wiki/Pagina_principale")

    def search_in_wiki(self, search):
        driver = self.driver
        search_bar = driver.find_element(By.XPATH, "//input[@id='searchInput']")
        search_bar.clear()
        search_bar.send_keys(search)
        search_bar.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        # driver.find_element_by_xpath("//a[@title='"+ search +"']").click()

    def is_search_result(self):
        return len(self.driver.find_elements(By.XPATH, "//a[@data-serp-pos='0']")) > 0

    def open_google_tab(self):
        self.new_tab("https://www.google.it/")

    def wiki_text(self, iterations):
        text = ""
        driver = self.driver
        elements = driver.find_elements(By.TAG_NAME, "p")
        for i in range(iterations):
            text += elements[i].text

        return text

    def open_lmgtfy_tab(self):
        self.new_tab("https://lmgtfy.com/")

    # Close browser window (not the console)
    def close_browser(self):
        self.driver.close()

    def search_chat(self, name):
        driver = self.driver
        actions = ActionChains(driver)

        print("searching for " + name)
        elem = self.driver.find_element(By.XPATH, "//input[@class='jN-F5 copyable-text selectable-text']")
        elem.clear()
        actions.click(elem)
        actions.perform()
        elem.send_keys(name)

    def open_chat_first_chat(self):
        driver = self.driver
        elem = driver.find_element(By.XPATH, "//div[@class='_2wP_Y']")
        elem.click()

    def send_message(self, msg: str):
        driver = self.driver
        web_obj = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/div[4]/div[1]/"
                                               "footer/div[1]/div[2]/div/div[2]")
        web_obj.send_keys(str(msg))
        web_obj.send_keys(Keys.RETURN)

    # Read the last message in the selected chat
    def last_message(self):
        driver = self.driver
        elements = driver.find_elements(By.XPATH, "//span[@class='_3-8er selectable-text copyable-text']")
        # print(len(elements))
        return str(elements[-1].text)

    @staticmethod
    def is_question(phrase):
        if phrase[-1] == '?':
            return True
        else:
            return False
        
    @staticmethod
    def is_for_bot(phrase):
        if phrase[0] == '!':
            return True
        else:
            return False


if __name__ == '__main__':
    # Variables and components
    refresh_sleep = 1
    last_message = ""  # Last message sent in the selected chat
    bot = WhatsappChatbot()
    chatbot_name = "Chatty"
    chatbot = ChatBot(chatbot_name)
    trainer = ChatterBotCorpusTrainer(chatbot)
    trainer.train("chatterbot.corpus.italian")
    bot.login()

    presentation = input("Presentation? ")

    if presentation == 'y':
        bot.send_message("Ciao! Sono, l'aiutante di Francesco fatto per chattare con te!")
        bot.send_message("Per mandarmi un messagio scrivi una frase preceduta da '!'")

    while True:
        last_message = bot.last_message()
        if last_message == 'quit':
            bot.send_message("Arrivederci!")
            break

        if bot.is_for_bot(last_message):
            last_message = last_message[1:]
            print("User: " + last_message)
            response = chatbot.get_response(last_message)
            # print("CleverBot: " + response)
            bot.send_message(response)
