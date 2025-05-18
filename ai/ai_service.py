import json
import re
from ollama import chat
import openai
from ai_crawler import settings
from ai.utils import shrink_html
from event.dto import EventDTO
from event.service import event_service


def clean_answer(xpath: str) -> str:
    # Remove all leading and trailing quotes
    while xpath.startswith(("'", '"', '`')) and xpath.endswith(("'", '"', '`')):
        xpath = xpath[1:-1].strip()
    # Remove 'xpath' prefix and strip leading/trailing whitespace
    xpath = xpath.lstrip("xpath").strip()

    return xpath

def extract_json_from_openai_response(response_text):
    """
    Extracts a JSON string from an OpenAI API response and parses it into a Python dictionary.

    :param response_text: The text response from the OpenAI API.
    :return: A Python dictionary containing the parsed JSON data.
    :raises ValueError: If no valid JSON string is found in the response.
    """
    try:
        # Use a regex to find JSON-like content in the response
        json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the response.")

        # Extract the JSON string
        json_string = json_match.group(0)

        # Parse the JSON string into a Python dictionary
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")


def extract_json_deepseek(response_text):
    split = response_text.split("```json")
    if len(split) > 1:
        response_text = split[1]
    split_2 = response_text.split("</think>")
    if len(split_2) > 1:
        response_text = split_2[0]

    # Use a regex to find JSON-like content in the response
    json_match = re.search(r'\{.*?\}', response_text, re.DOTALL)
    if not json_match:
        raise ValueError("No JSON object found in the response.")

    # Extract the JSON string
    json_string = json_match.group(0)

    # Parse the JSON string into a Python dictionary
    return json.loads(json_string)



class OpenAIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.request_method = self.make_request if settings.USE_OPENAI else self.make_request_ollama

    def get_event_list_re_expression(self, content: str) -> str:
        promt = f"""
        You are given a list of links.
        Give me the regular expression which filter the links to find only links to individual events.
        The answer should be only regular expression without any additional text or symbols or ANY quotes: {content}
        """
        answer = self.request_method(promt)
        answer = clean_answer(answer)
        return answer

    def get_event_container_xpath_expression(self, content: str) -> str:
        promt = f"""
        You are given a HTML page that contains info about single event.
        I need xpath expression which selects html element which contains all information about the event.
        Try to make it simple, its okay to capture some additional elements.
        The answer should be only xpath expression without any additional text or symbols or ANY quotes around it: {content}
        """
        answer = self.request_method(promt)
        answer = clean_answer(answer)
        return answer


    def get_event_json(self, content: str) -> EventDTO:
        html = shrink_html(content)
        prompt = f"""
        This is the information about the event in text format:
        {html}
        Please convert it to JSON file containing the following fields: title, description, link, cover, google_maps_uri, city, country, address, start_datetime, end_datetime.
        If it is impossible to extract some of the fields, please set them to empty string.
        The structure of the JSON should be flat - no embedded objects or arrays.
        start_datetime and end_datetime should be in ISO format.
        link is a single link to the event on a third-party site.
        cover is an image link to the event.
        If there is only one date, set start_datetime and end_datetime to the same value 00 AM.
        The answer should be a valid JSON object without any additional text.
        """
        answer = self.request_method(prompt)
        try:
            event_dto = event_service.from_dict(answer)
        except Exception as e:
            answer = self.reconsider_answer(answer)

        return answer

    def make_request(self, prompt: str) -> dict:
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=prompt,
            temperature=0,
        )
        answer = response.output_text.strip()
        return extract_json_from_openai_response(answer)

    def make_request_ollama(self, prompt: str) -> dict:
        response = chat(
            model="deepseek-r1:7b",
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )
        answer = response['message']['content'].strip()
        print(f"Answer event data: {answer}")
        return extract_json_deepseek(answer)

    def reconsider_answer(self, previous_answer):
        prompt = f"""
        I have a JSON object with the event data:
        {previous_answer}
        I requested a json with the following fields:
        title, description, link, cover, google_maps_uri, city, country, address, start_datetime, end_datetime.
        Please check if all fields are filled correctly and if not, please fix them.
        The structure of the JSON should be flat - no embedded objects or arrays.
        start_datetime and end_datetime should be in ISO format.
        The answer should be a valid JSON object without any additional text.
        """
        answer = self.request_method(prompt)
        return answer


openai_service = OpenAIService(api_key=settings.OPEN_AI_KEY)
