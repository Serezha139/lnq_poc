import scrapy_playwright


async def load_page_content(response):
    """
    Load the page content using Playwright.
    """
    page = response.meta["playwright_page"]
    content = await page.content()
    await page.close()
    # log content to file
    with open("page_content.html", "w", encoding="utf-8") as f:
        f.write(content)
    return content