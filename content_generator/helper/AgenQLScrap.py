from playwright.sync_api import sync_playwright

import json

class WebScrapping:

    @staticmethod
    def generate_articleScrapping(article_link):
        print("Getting the article using link provided")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 1. Visit website
            page.goto("https://dev.agentql.com/playground")  # Replace with your target URL

            page.wait_for_timeout(5000)
            viewport = page.viewport_size or {"width": 1280, "height": 720}  # fallback if not set
            center_x = viewport["width"] // 2
            center_y = viewport["height"] // 2
            page.mouse.click(center_x, center_y)

            print("------input url")
            # 2. Type in a textbox
            page.fill('#url-input', article_link)
            page.press('#url-input', 'Enter')  # Adjust selector

            page.wait_for_timeout(5000)

            page.click('#ace-editor')
            page.keyboard.press("Control+A")
            paste_string = """{
          article
        }"""

            print("------pasting the query")
            page.keyboard.insert_text(paste_string)

            page.wait_for_timeout(5000)

            print("------clicking the search")
            # 3. Click a button
            page.click('#generate-response-button')

            # 4. Wait for result to load (optional, depending on JS behavior)
            page.wait_for_selector('.whitespace-pre-wrap', timeout=20000)

            # 5. Extract content from element with class
            result = page.inner_text('.whitespace-pre-wrap')  # Replace with actual class

            data = json.loads(result)

            # Access the "article" field
            article_text = data["article"]

            browser.close()
            return article_text
