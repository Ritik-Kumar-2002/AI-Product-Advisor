🛍️ AI-Product-Advisor (SmartBuy AI)

🎯 Project Overview

Shopping is part of our daily life, but we often get confused about a product: Should I buy this or not? Does it fulfil my requirements?

Most of the time we don't have time to read all the reviews. We just want a short, complete summary of the product.

To solve this problem, I built SmartBuy AI, an AI product advisor. The user pastes a product page URL, the app reads the page and shows the key details, and then the user can chat with an AI assistant that answers questions about the product and advises whether to buy it.

📂 Data Source

There is no fixed dataset. Product data is fetched live from the product web page the user provides. A real Chrome browser (Playwright) reads the full page text, and an LLM extracts the product details from it.

🧰 Tech Used
Python
Streamlit
Playwright
BeautifulSoup
Requests
LangChain
Pydantic
OpenRouter (LLM access)
Web Scraping

🔄 Workflow
1. Paste a product URL
          ↓
2. Browser Fetch
   (Playwright reads the full page text)
          ↓
3. LLM Extraction
   (LLM extracts product details, validated with Pydantic)
          ↓
4. Product Card
   (Streamlit shows name, price, rating, features, specs)
          ↓
5. AI Chatbot
   (Streamlit + LangChain + LLM answers product questions)
   
🧪 Usage
Paste a product page URL into the text box.
Click Analyze Product. A Chrome window opens briefly while the page is read.
Review the product card on the left.
Ask questions in the chat on the right, for example:
"Is this good for daily use?"
"What do customers complain about?"
"Should I buy this at this price?"
