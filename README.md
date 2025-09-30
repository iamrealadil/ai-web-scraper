# AI Webscraper

#### Video Demo: [<AI WEBSCRAPER>](https://drive.google.com/file/d/1PqNWL7QXOy6VQhFzFjXwWAsc8ZDdoJBW/view?usp=sharing)

#### Description:

AI Webscraper is a Python-based project designed to scrape content from any website and intelligently extract structured information using artificial intelligence. The application combines the power of **Selenium** for browser automation, **BeautifulSoup** for HTML parsing and cleaning, and **OpenAI's GPT-3.5-turbo** through the **litellm** package to intelligently parse and extract data based on user-defined descriptions.  

The goal of this project is to allow users to collect meaningful data from websites quickly and efficiently, without manually sifting through HTML or unstructured text. This project demonstrates the integration of web scraping, text processing, and AI-powered data extraction into a cohesive Python application.

---

## Project Structure

project/
│
├── main.py # Main application with Streamlit interface
├── test_main.py # Pytest test file for main.py functions
├── requirements.txt # Dependencies required for the project
└── README.md # This file


---

### main.py

This is the core file of the project and contains the following functions:

1. **main()**  
   - Entry point of the application.
   - Sets up the Streamlit interface.
   - Allows users to input a URL, scrape the website, and parse content using AI.

2. **scrape_website(website)**  
   - Opens a browser using Selenium to retrieve the HTML of a given URL.
   - Returns the raw HTML content of the page.

3. **extract_body_content(html_content)**  
   - Extracts only the `<body>` portion of the HTML.
   - Ensures scripts, styles, and other extraneous parts of the page are ignored in later processing.

4. **extract_cleaned_content(body_content)**  
   - Cleans the body content by removing `<script>` and `<style>` tags.
   - Returns readable text with unnecessary whitespace removed.

5. **split_dom_content(dom_content, max_lenght=6000)**  
   - Splits large text into smaller chunks to ensure AI processing stays within token limits.
   - Returns a list of string chunks.

6. **parse_with_ai(dom_chunks, parse_description)**  
   - Uses GPT-3.5-turbo to extract structured information based on a user-provided description.
   - Returns a structured string output from the AI.

7. **ai(prompt_text)**  
   - Helper function to call the OpenAI API using the litellm package.
   - Returns the AI’s extracted data.

---

### test_main.py

The test file uses **pytest** to validate the functionality of core functions:

- `test_extract_body_content()` – Ensures only the `<body>` HTML is returned.  
- `test_extract_cleaned_content()` – Confirms that scripts and styles are removed and the text is cleaned.  
- `test_split_dom_content()` – Verifies that text is split correctly into chunks based on `max_lenght`.  
- `test_parse_with_ai_mock()` – Mocks the AI function to ensure the `parse_with_ai` function concatenates AI outputs correctly.

---

### Requirements

All dependencies are listed in `requirements.txt`:

streamlit
selenium
beautifulsoup4
litellm
pytest


These libraries are required for web scraping, AI integration, testing, and the user interface.

---

### Usage

1. **Install dependencies:**

```bash
pip install -r requirements.txt

2. Run the application:
streamlit run main.py

3. Scraping workflow:

Enter the URL of a website.

Click "Scrape Website" to retrieve the page content.

Enter a description of the data you want to extract (e.g., “Extract property type, price, and bedrooms”).

Click "Parse Content" to generate structured output using AI.


Example Output:
Apartment | 150,000 AED | 2 Bedrooms | 3 Bathrooms
Villa     | 300,000 AED | 4 Bedrooms | 5 Bathrooms

Design Decisions

- Streamlit Interface: Chosen for simplicity and immediate visual feedback to users.

- Selenium: Allows dynamic web pages with JavaScript content to be scraped accurately.

- BeautifulSoup: Cleans the raw HTML to make AI parsing more reliable.

- AI Parsing: GPT-3.5-turbo provides flexible extraction of complex or irregular data from raw text.

- Chunking: Large web pages are split into chunks to prevent token limits from causing AI failures.

This project demonstrates modular programming with clearly separated responsibilities, making it easy to extend, maintain, or replace components in the future.

Testing

Run all tests using pytest:

pytest


All core functions are covered by automated tests to ensure robustness.

