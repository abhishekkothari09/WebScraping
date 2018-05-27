import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uOpen
from docx import Document

def html_parsing(my_url):

    # Open the connection and get the page.
    opn = uOpen(my_url)
    page_html = opn.read()
    opn.close()

    # HTML parsing
    page_soup = soup(page_html, 'html.parser')
    return page_soup


def remove_links(page_soup):

    # Get the <p> tags and remove the hyperlinks and images
    ptags = page_soup.findAll("p")
    for ptag in ptags:
        print(ptag.text)
        document.add_paragraph(ptag.text)

# First page
my_url = 'https://en.wikipedia.org/wiki/Film'
page_soup = html_parsing(my_url)
document = Document()
cleaned = remove_links(page_soup)
document.save('demo.docx')