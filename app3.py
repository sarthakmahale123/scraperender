import json
from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app3 = Flask(__name__)

# Function to scrape data from Flipkart
def scrape_flipkart():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # List to store scraped product data
    scraped_data = []

    try:
        # Iterate over multiple pages
        for page_number in range(1, 6):  # Scraping first 5 pages, adjust as needed
            # Navigate to the webpage
            driver.get(f"https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page_number}")

            # Wait for the product elements to be present
            products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, '_1AtVbE')]")))

            # Loop through each product element
            for product in products:
                try:
                    # Find elements containing product name, price, and specifications
                    name_element = product.find_element(By.XPATH, ".//div[@class='_4rR01T']")
                    rating_element = product.find_element(By.XPATH, ".//div[@class='gUuXy-']")
                    price_element = product.find_element(By.XPATH, ".//div[@class='_3I9_wc _27UcVY']")
                    spec_elements = product.find_elements(By.XPATH, ".//li[@class='rgWa7D']")

                    # Extract text content from the elements
                    product_name = name_element.text
                    product_price = price_element.text
                    product_rating = rating_element.text

                    specifications = [spec_element.text for spec_element in spec_elements]

                    # Create a dictionary for the current product
                    product_data = {
                        "Product Name": product_name,
                        "Product Price": product_price,
                        "Product Rating": product_rating,
                        "Specifications": specifications
                    }

                    # Append the product data to the list
                    scraped_data.append(product_data)
                except Exception as e:
                    print(f"Error while extracting product details from Flipkart: {e}")
    except Exception as e:
        print(f"Error while scraping Flipkart: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

    return scraped_data

# Function to scrape data from Croma
def scrape_croma():
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome()

    # List to store scraped product data
    scraped_data = []

    try:
        # Navigate to the webpage
        driver.get("https://www.croma.com/searchB?q=laptops%3Arelevance&text=laptops")

        # Wait for the product elements to be present
        products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'product-item')]")))

        # Loop through each product element
        for product in products:
            try:
                # Find elements containing product name, price, and specifications
                name_element = product.find_element(By.XPATH, ".//div[@class='plp-prod-title-rating-cont']")
                rating_element = product.find_element(By.XPATH, ".//div[@class='cp-rating plp-ratings ratings-plp-line']")
                price_element = product.find_element(By.XPATH, ".//span[@class='amount plp-srp-new-amount']")
                spec_elements = product.find_elements(By.XPATH, ".//div[@class='product-msg-wrapper plp-offer-band']")

                # Extract text content from the elements
                product_name = name_element.text
                product_price = price_element.text
                product_rating = rating_element.text

                specifications = [spec_element.text for spec_element in spec_elements]

                # Create a dictionary for the current product
                product_data = {
                    "Product Name": product_name,
                    "Product Price": product_price,
                    "Product Rating": product_rating,
                    "Specifications": specifications
                }

                # Append the product data to the list
                scraped_data.append(product_data)
            except Exception as e:
                print(f"Error while extracting product details from Croma: {e}")

    except Exception as e:
        print(f"Error while scraping Croma: {e}")
    finally:
        # Close the WebDriver
        driver.quit()

    return scraped_data

@app3.route('/scrape_products')
def scrape_products():
    # Scrape data from Flipkart
    flipkart_data = scrape_flipkart()

    # Scrape data from Croma
    croma_data = scrape_croma()

    # Combine data from both sources
    combined_data = flipkart_data + croma_data

    # Convert combined data to JSON format
    json_data = json.dumps(combined_data, indent=4)

    return json_data

if __name__ == '__main__':
    app3.run(debug=True)
