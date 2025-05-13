from urllib.parse import urljoin


async def load_page_content(response):
    """
    Load the page content using Playwright.
    """
    page = response.meta["playwright_page"]
    content = await page.content()
    await page.close()
    return content



def extract_links_from_element(element, base_url=None):
    """
    Extracts all links (href attributes) from an HTML element.

    Args:
        element (lxml.html.HtmlElement): The HTML element to extract links from.
        base_url (str, optional): The base URL to resolve relative links. Defaults to None.

    Returns:
        list: A list of links as strings.
    """
    links = []
    for link_element in element.xpath(".//a[@href]"):  # Find all <a> elements with href attributes
        href = link_element.get("href")
        if base_url:
            href = urljoin(base_url, href)  # Resolve relative URLs
        links.append(href)
    return links

def safe_extract(html_element, xpath_expression, default=None):
    """
    Safely extracts the text content from an HTML element using an XPath expression.

    Args:
        html_element (lxml.html.HtmlElement): The HTML element to query.
        xpath_expression (str): The XPath expression to evaluate.
        default (any): The default value to return if extraction fails.

    Returns:
        str: The text content of the first matching element, or the default value.
    """
    try:
        result = html_element.xpath(xpath_expression)
        if result and len(result) > 0:
            return result[0].text_content()
    except Exception:
        pass
    return default