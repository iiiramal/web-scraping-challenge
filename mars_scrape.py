
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape ():

    app_dictionary = {}

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # Print all ten headlines
    content_titles = news_soup.find_all('div', class_='content_title')

    # A blank list to hold the headlines
    headlines = []
    # Loop over td elements
    for titles in content_titles:
                headlines.append(titles.text) 

    #for headline in headlines:
        #print(headline)         

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = headlines[0]

    app_dictionary['headline'] = news_title

    # Print all ten headlines
    content_teasers = news_soup.find_all('div', class_='article_teaser_body')

    # A blank list to hold the headlines
    teasers = []

    # Loop over td elements
    for teaser in content_teasers:
                teasers.append(teaser.text) 

    # Use the parent element to find the paragraph text

    news_p = teasers[0]

    app_dictionary['description'] = news_p

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Convert the browser html to a soup object
    html2 = browser.html
    image_soup = soup(html2, 'html.parser')
    slide_elem2 = image_soup.select_one('div.list_text')

    # Find and click the full image button
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # Parse the resulting html with soup
    html3 = browser.html
    image_soup_2 = soup(html3, 'html.parser')

    # find the relative image url
    img_url_rel = image_soup_2.find('img', class_='fancybox-image')["src"]

    # Use the base url to create an absolute url
    img_url = (f"{url}/{img_url_rel}")

    app_dictionary['mars_image'] = img_url

    # ## Mars Facts

    # Use `pd.read_html` to pull the data from the Mars-Earth Comparison section
    pandas_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(pandas_url)
    mars_df = tables[0]
    mars_df.columns = ['Description', 'Mars', 'Earth']
    #mars_df.head()
    mars_table = mars_df.to_html()

    app_dictionary['mars_table'] = mars_table

    # ## Hemispheres

    # In[ ]:


    url = 'https://marshemispheres.com/'

    browser.visit(url)
    browser.is_element_present_by_css('div.item', wait_time=1)

    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Get a list of all of the hemispheres
    links = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        data = {}
        browser.find_by_css('a.product-item img')[i].click()
        
        # We have to find the elements on each loop to avoid a stale element exception
        #a = links.find_by_css[i]['a']
        sample = browser.find_by_text('Sample').first
        
        # Next, we find the Sample image anchor tag and extract the href
        data["url"] = sample['href']
        
        # Get Hemisphere title
        title = browser.find_by_css('h2.title')
        data['title'] = title.value
        print(data)
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(data)
        
        # Finally, we navigate backwards
        browser.back()

    app_dictionary['hemisphere_image_data'] = hemisphere_image_urls

    testdic = {"1": 1, "2": 2}

    browser.quit()

    return app_dictionary
    
    #for key in app_dictionary:
        #print (key, ':', app_dictionary[key])






