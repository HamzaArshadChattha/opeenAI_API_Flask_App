import openai

class ChatGptBotAPI:
    def __init__(self, open_api_key):
        self.api_key = open_api_key
        self.model = "gpt-3.5-turbo"
        self.prompts = []

    def get_prompts(self):
        return self.prompts

    def create_prompt(self, prompt):
        try:
            if len(prompt) > 0:
                prompt_obj = {"role": "user", "prompt": prompt, 'response': ''}
                
                self.prompts.append(prompt_obj)
                self.prompts[-1]['id'] = len(self.prompts) - 1
                return prompt_obj
            else:
                return False
        except:
            return False
        
    def get_response(self, prompt_index):
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model = self.model,
            messages = [{'role': 'user', 'content': self.prompts[prompt_index]['prompt']}]
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        self.prompts[prompt_index]['response'] = ChatGPT_reply

        return ChatGPT_reply

    def update_prompt(self, prompt_index, new_prompt):
        self.prompts[prompt_index]['prompt'] = new_prompt
        return {'prompt': self.prompts[prompt_index]['prompt'], 'id': prompt_index}

    def delete_prompt(self, prompt_index):
        return self.prompts.pop(prompt_index)


