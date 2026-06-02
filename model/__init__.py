import os
from colorama import Fore, Style
import requests
import json


class Model:
    def __init__(self, save_hist = True,url="https://api.deepai.org/hacking_is_a_serious_crime"):
        self.url = url
        self.save_history = save_hist
        self.allowed_exts = ["txt","pdf","docx"]
        self.available_models = {
            "default": "online",
            "standard":"standard",
            "gpt4": "",
            "ds3.2": "deepseek-v3.2",
            "gemini": "gemini-2.5-flash-lite",
            "gemma4": "gemma-4"
        }
        self.instructions = self._load_instructions()
        self.history = [
            {
                "role": "system",
                "content": self.instructions
            },{
                "role":"user",
                "content":"bonjour"
            }
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "api-key": "tryit-29313838055-92efd3f13305fd73765982f1e4bd8c0b",
            "Origin": "https://deepai.org",
            "Connection": "keep-alive"
        }

    def get_answer(self, query, MODEL=None):
        # add the user answer
        self.history.append({
            "role": "user",
            # "content": query
            "content": f"n'oublier pas à respecter les instructions de système et de répondre juste à la question de l'utilisateur , répondre à : {query}"
        })
        # history to json 
        if self.save_history :
            self.save_history_to_json()
        
        # build new history
        new_hist = json.dumps(self.history)
        # print(str(new_hist))
        body = {
            "chat_style": (None, "chat"),
            "chatHistory": (None, new_hist),
            "model": (None, self.available_models["default"] if MODEL is None else MODEL),
            "session_uuid": (None, "bb3d57a9-405f-40e9-a6dc-0a831175d7b4"),
            "hacker_is_stinky": (None, "very_stinky"),
            "enabled_tools": (None, '["image_generator","image_editor"]'),
        }

        response = requests.post(self.url, headers=self.headers, files=body)
        # add the model answer to the history
        self.history.append({
            "role": "assistant",
            "content": response.text
        })
        return response.text

    def _load_instructions(self, file="instructions.txt"):
        import os
        if not os.path.exists(file):
            print("Could not load instructions from '{}' ".format(file))
            return ""
        with open(file, "r") as instructions:
            return instructions.read().strip()

    # load history of talks
    def load_history(self, path: str):
        self.history = []
        return ""

    def load_knowledge(self, path: str):
        files = os.listdir(path)
        # read files as type
    def save_history_to_json(self):
        # save only chat history not system instructtions 
        temp = self.history[1:]
        import os
        l = len(os.listdir("./model/histories"))
        with open(f"./model/histories/{l}.json","w") as file :
            json.dump(temp,file)