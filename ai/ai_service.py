import openai
from ai_crawler import settings

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def get_event_list_re_expression(self, content: str) -> str:
        promt = f"""
        You are given a list of links
        Give me the regular expression which filter the links to find only links to individual events on the page. The answer should be regular expression without any additional text: {content}
        """
        answer = self.client.responses.create(
            model="gpt-4.1-nano",
            input=promt,
        )
        return answer.output_text.strip()

    def get_event_container_xpath_expression(self, content: str) -> str:
        answer = self.client.responses.create(
            model="gpt-4.1-nano",
            input=f"Give me the xpath expression which selects the event container on the page, answer should be only correct xpath without any additional text: {content}",
        )
        return answer.output_text.strip()

    def get_event_xpath_expressions(self, content: str, param_name:str) -> str:
        prompt = f"""
You are an expert in HTML parsing and data extraction.
Given the HTML element  that contains info about single event:

{content}
    
give me the xpath expression, which would work for any analogue html element, that selects the {param_name} field.
Do not base it on the text content of the element, but rather on the structure of the HTML.
The answer should not contain additional text or symbols, just the xpath expression.
"""
        answer = self.client.responses.create(
            model="gpt-4.1-nano",
            input=prompt,
        )
        return answer.output_text.strip()


openai_service = OpenAIService(api_key=settings.OPEN_AI_KEY)
