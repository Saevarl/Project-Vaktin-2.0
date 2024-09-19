from bs4 import BeautifulSoup

class Parser:
    @staticmethod
    def extract_body_content(html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        if body_content:
            return str(body_content)
        return ""

    @staticmethod
    def clean_body_content(body_content):
        soup = BeautifulSoup(body_content, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Extract hrefs from <a> tags and include them in the text
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            a_tag.insert(0, f"[Link: {href}] ")

        # Get the text content
        cleaned_content = soup.get_text(separator="\n")
        cleaned_content = "\n".join(
            line.strip() for line in cleaned_content.splitlines() if line.strip()
        )


        return cleaned_content
    @staticmethod
    def split_dom_content(dom_content, max_length=6000):
        return [
            dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
        ]
