import streamlit as st
import time
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from litellm import completion

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string (''). "
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def ai(prompt_text):
    response = completion(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system","content":"You are a helpful assistant that extracts requested data from text."},
            {"role":"user","content":prompt_text}
        ],
        max_tokens=1000
    )
    return response['choices'][0]['message']['content']

def scrape_website(website):
    print("Connecting to Scraping Browser...")
    chrome_driver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(chrome_driver_path),options=options)

    try:
        driver.get(website)
        html = driver.page_source
        return html
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content,"html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    else:
        return ""

def extract_cleaned_content(body_content):
    soup = BeautifulSoup(body_content,"html.parser")

    for script_or_style in soup(["script","style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content,max_lenght=6000):
    return[
        dom_content[i:i+max_lenght] for i in range(0,len(dom_content),max_lenght)
    ]

def parse_with_ai(dom_chunks,parse_description):
    parsed_result = []

    for i,chunk in enumerate(dom_chunks,start=1):
        prompt_text = template.format(dom_content=chunk,parse_description=parse_description)
        response_text = ai(prompt_text)
        parsed_result.append(response_text)
        print(f"Parsed batch {i} of {len(dom_chunks)}")

    return "\n".join(parsed_result)


def main():
    st.set_page_config(page_title = "AI WEBSCRAPER", page_icon= "🤖", layout="centered")
    st.title("🤖 AI WEBSCRAPER")
    url = st.text_input("Enter Website URL")
    
    if st.button("Scrape Website"):
        with st.spinner("Scrapping the Website"):
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = extract_cleaned_content(body_content)

            st.session_state.dom_content = cleaned_content

            with st.expander("View Dom Content"):
                st.text_area("DOM Content",cleaned_content,height=300)
    
    if "dom_content" in st.session_state:
        parse_description = st.text_area("Describe what you want to parse?")

        if st.button("Parse Content"):
            with st.spinner("Parsing content...."):
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_ai(dom_chunks,parse_description)
                st.write(result)



if __name__ == "__main__":
    main()



