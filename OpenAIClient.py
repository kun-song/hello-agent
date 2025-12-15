from openai import OpenAI
import Config

class OpenAICompatibleClient:
    def __init__(self, model: str, api_key: str, base_url: str = None):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        

    def generate(self, prompt: str, system_prompt: str) -> str:
        print("正在调用大语言模型...")

        try:
            messages=[
                {'role': 'user', 'content': prompt},
                {'role': 'system', 'content': system_prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            answer = response.choices[0].message.content
            print("大语言模型调用成功。")
            print(f"模型响应内容:\n{answer}\n")
            return answer
        except Exception as e:
            print(f"调用大语言模型时出错: {e}")
            return "抱歉，无法生成响应。"

if __name__ == "__main__":
    client = OpenAICompatibleClient(model=Config.model, api_key=Config.api_key, base_url=Config.base_url)
    prompt = "请简要介绍一下人工智能的发展历史。"
    system_prompt = "你是一个知识渊博的助手，能够提供准确且 简洁的信息。"
    response = client.generate(prompt, system_prompt)
    print("生成的响应：")
    print(response)