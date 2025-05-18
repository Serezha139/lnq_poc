from bs4 import BeautifulSoup


def shrink_html(html: str):
    soup = BeautifulSoup(html, "lxml")

    # Remove irrelevant tags
    for tag in soup(["script", "style", "noscript", "meta", "footer", "form", "nav"]):
        tag.decompose()

    # Extract and format meaningful content
    output = []

    # Headings
    for tag in soup.find_all(["h1", "h2", "h3"]):
        output.append(f"{tag.name.upper()}: {tag.get_text(strip=True)}")

    # Paragraphs
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            output.append(f"P: {text}")

    # Image descriptions
    for img in soup.find_all("img"):
        alt = img.get("alt")
        src = img.get("src")
        if alt or src:
            output.append(f"IMG: alt='{alt}' src='{src}'")

    # Links
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        output.append(f"LNK: text='{text}' url='{a['href']}'")

    # Location/date/time-like strings
    for div in soup.find_all("div"):
        text = div.get_text(strip=True)
        if any(keyword in text.lower() for keyword in ["amsterdam", "date", "time", "location", "venue"]):
            output.append(f"INF: {text}")

    # Deduplicate and return
    return "\n".join(dict.fromkeys(output))
