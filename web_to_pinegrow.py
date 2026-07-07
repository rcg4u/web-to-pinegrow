import json
import sys
import urllib.request
import re
from html.parser import HTMLParser

class HTMLToMarkdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.markdown = []
        self.current_tag = None
        self.title = ""
        self.in_title = False
        self._temp_href = ""

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        if tag == "title":
            self.in_title = True
        elif tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            level = int(tag[1])
            self.markdown.append(chr(10) + chr(10) + ("#" * level) + " ")
        elif tag == "p":
            self.markdown.append(chr(10) + chr(10))
        elif tag == "br":
            self.markdown.append(chr(10))
        elif tag == "li":
            self.markdown.append(chr(10) + "* ")
        elif tag in ["strong", "b"]:
            self.markdown.append("**")
        elif tag in ["em", "i"]:
            self.markdown.append("*")
        elif tag == "a":
            href = attrs_dict.get("href", "")
            self.markdown.append("[")
            self._temp_href = href
        elif tag == "img":
            alt = attrs_dict.get("alt", "Image")
            src = attrs_dict.get("src", "")
            self.markdown.append("![" + alt + "](" + src + ")")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in ["strong", "b"]:
            self.markdown.append("**")
        elif tag in ["em", "i"]:
            self.markdown.append("*")
        elif tag == "a":
            self.markdown.append("](" + self._temp_href + ")")
            self._temp_href = ""
        self.current_tag = None

    def handle_data(self, data):
        if self.in_title:
            self.title += data.strip()
        
        if self.current_tag not in ["script", "style"]:
            self.markdown.append(data)

    def get_markdown(self):
        raw_md = "".join(self.markdown)
        clean_md = re.sub(chr(10) + "{3,}", chr(10) + chr(10), raw_md)
        return self.title.strip(), clean_md.strip()

def scrape_website(url):
    print("Scraping " + url + "...")
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode("utf-8", errors="ignore")
            
        parser = HTMLToMarkdown()
        parser.feed(html_content)
        title, markdown_content = parser.get_markdown()
        
        if not title:
            title = "Untitled Page"
            
        formatted_content = "Title: " + title + chr(10) + chr(10) + "URL Source: " + url + chr(10) + chr(10) + "Markdown Content:" + chr(10) + markdown_content
        
        source_entry = {
            "type": "PgPineConeContentSourceUrl",
            "url": url,
            "content": formatted_content
        }
        
        return source_entry
    except Exception as e:
        print("Error scanning " + url + ": " + str(e), file=sys.stderr)
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python web_to_pinegrow.py <url1> [url2] ... [output_file.json]")
        print("Example: python web_to_pinegrow.py https://example.com my_knowledge.json")
        sys.exit(1)
        
    urls = []
    output_file = "pinegrow_knowledge_source.json"
    
    args = sys.argv[1:]
    if args[-1].endswith(".json"):
        output_file = args[-1]
        urls = args[:-1]
    else:
        urls = args
        
    if not urls:
        print("Error: No URLs provided.")
        sys.exit(1)
        
    knowledge_source = {"sources": []}
    
    for url in urls:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        entry = scrape_website(url)
        if entry:
            knowledge_source["sources"].append(entry)
            
    if knowledge_source["sources"]:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(knowledge_source, f, indent=2, ensure_ascii=False)
        print(chr(10) + "Success! Saved " + str(len(knowledge_source["sources"])) + " source(s) to '" + output_file + "'")
    else:
        print(chr(10) + "Failed to extract any content from the provided URLs.")

if __name__ == "__main__":
    main()
