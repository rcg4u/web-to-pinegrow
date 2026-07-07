# web-to-pinegrow
### **Pinegrow Knowledge Source Generator**

I have updated the script to ensure the output filename defaults to `content-sources.json` and created a comprehensive README to guide you through its features.

#### **Updated Script Features**
*   **Default Output**: Always saves to `content-sources.json` unless you explicitly override it.
*   **Spider Mode**: Recursively crawls internal links within the same domain to build a complete knowledge base.
*   **Social Discovery**: Scans for profile links (Facebook, X/Twitter, LinkedIn, Instagram, TikTok, etc.) and adds them as individual text source entries.
*   **Pinegrow Formatting**: Strictly adheres to the `PgPineConeContentSourceUrl` and `PgPineConeContentSourceText` structures.

***

### **README.md**

# Pinegrow Web-to-Source Generator

A Python-based utility designed to scan websites and generate a `content-sources.json` file compatible with the Pinegrow PineCone knowledge source format.

## **Features**
- **Web Scraping**: Converts website content into structured Markdown entries.
- **Spidering**: Automatically discovers and crawls internal pages within the same domain.
- **Social Media Detection**: Extracts social media profiles and adds them as factual text sources.
- **Pinegrow Compatibility**: Generates the exact JSON schema required for Pinegrow's AI assistant.

## **Installation**
The script uses standard Python 3 libraries. No external dependencies (like BeautifulSoup or Requests) are required, making it lightweight and portable.

```bash
# Ensure you have Python 3 installed
python --version
```

## **Usage**

### **Basic Scan**
Scrape a single page and save it to `content-sources.json`.
```bash
python web_to_pinegrow.py https://example.com
```

### **Full Site Spider & Social Scan**
Crawl the entire site (up to the default limit) and extract all social media links.
```bash
python web_to_pinegrow.py https://example.com --spider --social
```

### **Advanced Options**
| Flag | Description |
| :--- | :--- |
| `--spider` | Crawl internal links discovered on the page. |
| `--social` | Find and add social media profiles as text sources. |
| `--limit [N]` | Maximum number of pages to crawl (Default: 30). |
| `-o [file]` | Override the default `content-sources.json` filename. |

## **JSON Structure Example**
The output file will look like this:
```json
{
  "sources": [
    {
      "type": "PgPineConeContentSourceUrl",
      "url": "https://example.com",
      "content": "Title: Home\n\nURL Source: https://example.com\n\nMarkdown Content: ..."
    },
    {
      "type": "PgPineConeContentSourceText",
      "text": "Social Media Profile: https://twitter.com/username"
    }
  ]
}
```

***

**Download the final script here:** [web_to_pinegrow.py](artifacts://web_to_pinegrow.py)

You can now run this against any site to generate your `content-sources.json` file for Pinegrow. If you need any further adjustments to the scraping logic or social media filters, let me know!
