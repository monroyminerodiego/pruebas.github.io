from bs4 import BeautifulSoup
import requests
import json
import time

class Scrapper:
    
    # =============== CONSTRUCTOR ===============
    def __init__(self,URL:str,verbose:bool = False, daemon:bool = False):
        '''
        Initializes a new instance of the Scrapper class.

        ### Args:
        * `URL` (str): The URL of the page to scrape.
        * `verbose` (bool, optional): Flag to enable verbose output. Defaults to False.
        * `daemon` (bool, optional): Flag to determine if the class is instanced as a daemon. Defaults to False.

        ### Attributes:
        * `URL` (str): Stores the URL of the page to scrape.
        * `verbose` (bool): Stores the verbose flag status.
        * `daemon` (bool): Stores the daemon flag status.
        * `soup` (BeautifulSoup | None): The parsed HTML of the page, initialized by `__load_soup`.
        * `names` (str | None): Product names, initialized by `__load_names`.
        * `prices` (str | None): Product prices, initialized by `__load_prices`.
        * `descriptions` (str | None): Product descriptions, initialized by `__load_descriptions`.
        * `images` (list | None): Product images, initialized by `__load_images`.

        ### Methods:
        * `__load_soup`: Loads the HTML of the page into `soup`.
        * `__load_names`: Extracts product names and stores them in `names`.
        * `__load_prices`: Extracts product prices and stores them in `prices`.
        * `__load_descriptions`: Extracts product descriptions and stores them in `descriptions`.
        * `__load_images`: Extracts product images and stores them in `images`.
        * `load_all_attributes`: Calls private methods to load all attributes.
        * `get_all_attributes`: Returns a dictionary containing all product details.

        ### Notes:
        * If the class is instanced with the `daemon` flag set to True, it automatically loads all attributes.
        '''
        # Defining the variables
        self.URL     = URL
        self.verbose = verbose
        self.daemon  = daemon
        self.__inform("Class initialized correctly...")

        # If class instanced as a daemon, loads soup automatically
        if self.daemon:
            self.__load_all_attributes()
        
    # =============== PRIVATE METHODS ===============
    def __inform(self,message:str):
        '''
        Method used to print messages in console depending on `verbose` flag.

        ### Args:
        * `message` (str): The message to be printed in console
        '''
        if self.verbose: print(message)
    
    def __load_soup(self):
        '''
        Method created to declare the soup as an attribute of the class.

        ### Notes:
        * This method generates an attribute called `soup`, which can take 2 values: BeautifulSoup object | None
        '''
        execution_time = time.time()
        
        response = requests.get(self.URL)
        if response.status_code == 200:
            html = response.text
            self.soup = BeautifulSoup(html,'lxml')
        else:
            self.soup = None

        self.__inform(f"Execution time for generating soup: {time.time() - execution_time:.2f} seconds")

    def __load_names(self):
        '''
        Private method to load the product names.

        This method searches for the product name in the parsed HTML and sets the `names` attribute of the class.
        If the product name is not found, it sets a default message.
        '''
        attributes1 = self.soup.find('div', class_= 'ui-pdp-container__col col-2 mr-32')
        nm = attributes1.find('h1', class_ = 'ui-pdp-title')
        if nm:
            self.names = nm.get_text()
        else:
            self.names = 'The product name was not found.'
    
    def __load_prices(self):
        '''
        Private method to load the product prices.

        This method searches for the product price in the parsed HTML and sets the `prices` attribute of the class.
        If the product price is not found, it sets a default message.
        '''
        attributes2 = self.soup.find('div', class_= 'ui-pdp-container__col col-2 mr-32')
        pr = attributes2.find('span', class_ = 'andes-money-amount__fraction')
        if pr:
            self.prices = pr.get_text()
        else:
            self.prices = 'The product price was not found.'

    def __load_descriptions(self):
        '''
        Private method to load the product descriptions.

        This method searches for the product description in the parsed HTML and sets the `descriptions` attribute of the class.
        If the product description is not found, it sets a default message.
        '''
        attributes3 = self.soup.find('p', class_= 'ui-pdp-description__content')
        if attributes3:
            self.descriptions = attributes3.get_text()
        else:
            self.descriptions = 'The product description was not found.'

    def __load_images(self):
        '''
        Private method to load the product images.

        This method searches for image tags in the parsed HTML and stores the image URLs in the `images` attribute of the class.
        '''
        img_tags = self.soup.select('div[class*="ui-pdp-gallery"] span[class*="ui-pdp-gallery"] figure[class*="ui-pdp-gallery"] img')
        self.images = []
        for im in img_tags:
            img = im.get('data-zoom')
            self.images.append(img)

    def __load_all_attributes(self):
        '''
        Loads all the attributes of the class by calling private methods.

        This method checks if each attribute (soup, names, prices, descriptions, images) is already loaded. If not, it calls the corresponding method to load it.
        '''
        if not(hasattr(self,'soup')): self.__load_soup()
        if not(hasattr(self,'names')): self.__load_names()
        if not(hasattr(self,'prices')): self.__load_prices()
        if not(hasattr(self,'descriptions')): self.__load_descriptions()
        if not(hasattr(self,'images')): self.__load_images()
        
    # =============== PUBLIC METHODS ===============        
    def get_all_attributes(self):
        '''
        Retrieves all the main attributes of the product.

        ### Returns:
        * `dict`: A dictionary containing product details like name, prices, descriptions, and images.
        '''
        execution_time = time.time()
        if not(hasattr(self,'soup')): self.__load_all_attributes()
        all_def = {
            "name": self.names,
            "prices": self.prices,
            "descriptions": self.descriptions,
            "images": self.images
        }
        self.__inform(f"Execution time for generating all attributes: {time.time() - execution_time:.2f} seconds")
        return all_def
    
# =============== DEBUGGING ===============
if __name__ == '__main__':

    link = 'https://www.mercadolibre.com.mx/laptop-lenovo-ideapad-156-ryzen-3-7320u-8gb-256gb-ssd/p/MLM21816271?pdp_filters=category:MLM1652#searchVariation=MLM21816271&position=3&search_layout=stack&type=product&tracking_id=dd9d1c17-227c-4f8d-87e6-09b3c7969cad'
    
    test = Scrapper(
        URL     = link,
        verbose = True,
        daemon  = True,
    )
    
    print('\n\n',test.get_all_attributes())
    