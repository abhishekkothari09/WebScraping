import bs4
from urllib.request import urlopen as uOpen
from bs4 import BeautifulSoup as soup

def html_parsing(my_url):

	# Open the connection and get the page.
	opn = uOpen(my_url)
	page_html = opn.read()
	opn.close()

	# HTML parsing
	page_soup = soup(page_html, 'html.parser')
	return page_soup


def get_write(page_soup):

	# get the product
	containers = page_soup.findAll("div",{"class":"zg_itemImmersion"})
	for container in containers:

		# Rank
		rank = container.div.span.text.strip()
	 
		# Title of the book
		title_container = container.find("div",{"class":"zg_itemWrapper"})
		title = title_container.a.text.strip()

		# Author
		author_container = container.find("div",{"class":"a-row a-size-small"})
		author = author_container.text.strip()

		# Rating
		rating_container = container.find("span",{"class":"a-icon-alt"})
		try:
			rating = rating_container.text.replace("out of 5 stars","").strip()
		except AttributeError:
			rating = "Not released yet.!"

		#Edition
		edition_container = container.find("span",{"class":"a-size-small a-color-secondary"})
		edition = edition_container.text.strip()

		#Price
		price_container = container.find("span",{"class":"p13n-sc-price"})
		if price_container is None:
			price_container = container.find("span",{"class":"a-size-base a-color-price"})
		price = price_container.text.strip()
		
		# Write the data in .csv file
		f.write(rank + "," + title.replace(",","!") + "," + author + "," +  rating + "," +  edition + "," +  price + "\n")

# First page
my_url = 'https://www.amazon.com/gp/bestsellers/books/283155/ref=s9_acsd_ri_bw_clnk_r?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-8&pf_rd_r=0GQ703YCPEPTTH440M53&pf_rd_r=0GQ703YCPEPTTH440M53&pf_rd_t=101&pf_rd_p=b8c0a303-a08e-4b0b-bd49-040811fd7080&pf_rd_p=b8c0a303-a08e-4b0b-bd49-040811fd7080&pf_rd_i=283155'
filename = 'amazon_books.csv'
f = open(filename,'w')

header = "Rank, Title, Author, Rating ( out of 5 ), Edition, Price\n"
f.write(header)

page_soup = html_parsing(my_url)
get_write(page_soup)

# Other pages in order
pages = page_soup.findAll("ol",{"class":"zg_pagination"})
total_pages = len(pages[0].findAll("li"))

for page in range(1,total_pages+1):
	if page is 1:
		continue
	else:
		t = "zg_page" + str(page)
		next_page = pages[0].find("li",{"id":t}).a["href"]
		page_soup = html_parsing(next_page)
		get_write(page_soup)

f.close()

