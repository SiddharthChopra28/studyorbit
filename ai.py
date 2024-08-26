from hugchat import hugchat
from hugchat.login import Login


EMAIL = "siddharth_c1@me.iitr.ac.in"
PASSWD = "Anacondas@123"
cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors

class ChatBot:
    def __init__(self):
        sign = Login(EMAIL, PASSWD)
        self.cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

        self.chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

        self.chatbot.delete_all_conversations()

        self.chatbot.new_conversation(switch_to = True) # switch to the new conversation


    def msg(self, text):
        message_result = self.chatbot.chat(text)

        return message_result


