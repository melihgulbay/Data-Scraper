import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv
from datetime import datetime


def scrape_property_details(driver, url):
    try:
        print(f"\nNavigating to URL: {url}")
        driver.get(url)
        
        # Extract district name from URL (e.g., 'adalar' from '.../istanbul-adalar')
        bolge = url.split('?')[0].split('/')[-1].split('-')[-1].capitalize()
        
        # Set up wait time for dynamic content loading
        wait = WebDriverWait(driver, 10)
        
        # Find all property listings on the page
        property_rows = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "searchResultsItem")))
        results = []
        
        # Iterate through each property listing
        for row in property_rows:
            property_details = {}
            
            try:
                # Store property information in a dictionary
                property_details['Bölge'] = bolge  # District
                
                # Extract square meters (Gross)
                brut = row.find_element(By.CSS_SELECTOR, "td.searchResultsAttributeValue").text.strip()
                property_details['m² (Brüt)'] = brut
                
                # Extract number of rooms
                oda = row.find_elements(By.CSS_SELECTOR, "td.searchResultsAttributeValue")[1].text.strip()
                property_details['Oda Sayısı'] = oda
                
                # Extract price
                fiyat = row.find_element(By.CSS_SELECTOR, "td.searchResultsPriceValue span").text.strip()
                property_details['Fiyat'] = fiyat
                
                # Extract neighborhood
                mahalle = row.find_element(By.CSS_SELECTOR, "td.searchResultsLocationValue").text.strip()
                property_details['Mahalle'] = mahalle
                
                results.append(property_details)
                
            except Exception as e:
                print(f"Error extracting property details: {str(e)}")
                continue
                
        return results
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


def scrape_multiple_properties(urls):
    results = []
    driver = None
    
    try:
        # Configure Chrome options for stable scraping
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        driver = uc.Chrome(options=options)
        
        # Process each URL and collect results
        for url in urls:
            try:
                result = scrape_property_details(driver, url)
                if result:
                    results.extend(result)  # Combine results from all pages
                time.sleep(10)  # Delay between requests to avoid rate limiting
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        # Ensure browser is properly closed even if errors occur
        if driver:
            try:
                driver.close()
                driver.quit()
            except:
                pass
    
    return results

def save_to_csv(results):
    if not results:
        print("No results to save")
        return
        
    # Create unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"property_details_{timestamp}.csv"
    
    # Define CSV column headers
    fieldnames = [
        'Bölge',
        'm² (Brüt)',
        'Oda Sayısı',
        'Fiyat',
        'Mahalle'
    ]
    
    # Write results to CSV file using semicolon delimiter (common in Turkish Excel)
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(fieldnames)
        
        for result in results:
            row = [
                result.get('Bölge', ''),
                result.get('m² (Brüt)', ''),
                result.get('Oda Sayısı', ''),
                result.get('Fiyat', ''),
                result.get('Mahalle', '')
            ]
            writer.writerow(row)
    
    print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    print("Starting the scraper...")
    
    # List of URLs to scrape
    urls = [
            "https://www.sahibinden.com/satilik-daire/istanbul-adalar?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-arnavutkoy?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-atasehir?pagingSize=50",    
            "https://www.sahibinden.com/satilik-daire/istanbul-avcilar?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-bagcilar?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-bahcelievler?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-bakirkoy?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-basaksehir?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-bayrampasa?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-besiktas?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-beykoz?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-beylikduzu?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-beyoglu?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-buyukcekmece?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-catalca?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-cekmekoy?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-esenler?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-esenyurt?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-eyupsultan?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-fatih?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-gaziosmanpasa?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-gungoren?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-kadikoy?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-kagithane?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-kartal?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-kucukcekmece?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-maltepe?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-pendik?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-sancaktepe?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-sariyer?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-silivri?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-sultanbeyli?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-sultangazi?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-sile?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-sisli?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-tuzla?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-umraniye?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-uskudar?pagingSize=50",  
            "https://www.sahibinden.com/satilik-daire/istanbul-zeytinburnu?pagingSize=50", 
    ]
    # Scrape all properties
    results = scrape_multiple_properties(urls)
    
    # Print results
    if results:
        print("\nExtracted Property Details:")
        for result in results:
            print("\nProperty:")
            for key, value in result.items():
                print(f"{key}: {value}")
            print("-" * 50)
    
    # Save results to CSV
    save_to_csv(results)
