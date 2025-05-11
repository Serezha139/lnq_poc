import openai
from ai_crawler import settings

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def get_event_list_xpath_expression(self, content: str) -> str:
        promt = f"""
        Give me the xpath expression which selects all the links of all of the event details on the page. The answer should be an xpath expression without any additional text: {content}
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

    def get_event_info(self, html_content: str) -> str:
        prompt = f"""
        Extract the following fields from the provided HTML container. If a field is not present, return null. 
        The fields are: 
        original_site, original_uri, _id, cover, thumb, title, description, link, city, country, address, lat, lng, google_maps_uri, start_date, end_date, dates, allDay, timeFrom, timeTill.
        Return the result as a JSON object without any additional text or symbols.

        HTML content:
        {html_content}
        """
        answer = self.client.responses.create(
            model="gpt-4.1-nano",
            input=prompt,
        )
        return answer.output_text.strip()


openai_service = OpenAIService(api_key=settings.OPEN_AI_KEY)
