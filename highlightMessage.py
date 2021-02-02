from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager


def get_info_of_msg(s):
    return s[s.index(']')+2:].strip(' :'), datetime.strptime(s[1:s.index(']')], '%H:%M, %d/%m/%Y')


def scroll(tab, today_day):
    print("Starting scrolling....")
    while True:
        print('Scroll')
        tab.send_keys(Keys.CONTROL, Keys.HOME)
        sleep(10)
        div = tab.find_element_by_class_name('copyable-text')
        _, oldest_msg = get_info_of_msg(div.get_attribute('data-pre-plain-text'))
        if today_day != oldest_msg.day:
            break


class WspBot:
    def __init__(self, person, message):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get("https://web.whatsapp.com/")
        sleep(10)
        self.driver.find_element_by_xpath("//span[contains(text(), '{}')]".format(person)).click()
        sleep(10)
        self.analyse_messages(message)

    def analyse_messages(self, message):
        msgs = self.get_messages()
        for msg in msgs:
            if message.lower() in msg[-1].lower():
                print(msg[0], "said", msg[-1], "at", msg[1])

    def get_messages(self):
        tab_element = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div[4]/div/div[3]/div/div")
        today_msgs = set()
        today_day = datetime.today().day
        scroll(tab_element, today_day)
        divs = tab_element.find_elements_by_class_name('copyable-text')
        for div in divs:
            try:
                name, msg_date = get_info_of_msg(div.get_attribute('data-pre-plain-text'))
            except AttributeError:
                continue
            if today_day == msg_date.day:
                try:
                    today_msgs.add((name, msg_date, div.find_element_by_class_name('_1wlJG').find_element_by_tag_name(
                        'span').find_element_by_tag_name('span').text))
                except:
                    today_msgs.add((msg_date, 'emoji'))
        return today_msgs


chat = input("Please input the name of the chat \n --> ")
message = input("Please input the message you would like to look for \n --> ")
bot = WspBot(person=chat, message=message)
