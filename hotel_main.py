# Dependencies
### catatan cari available dan tidaknya menggunkans selenium bukan bautifulsoup.
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd  # To store data in dataframe
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time

start = time.time()
ids = []
hotels = []
cities = []
check_in_dates = []
check_out_dates = []
re_attempt = []
# Open the CSV file with the open function
with open('Hotels to Scrape.csv', newline='') as csvfile:
    # Read the CSV file using the csv.reader module
    reader = csv.reader(csvfile)

    # Loop through each row in the CSV file
    for row in reader:
        # Access the first column of each row
        id_hotel = row[0]
        hotel = row[1]
        city = row[3]
        check_in_date = row[10]
        check_out_date = row[12]
        ids.append(id_hotel)
        cities.append(city)
        hotels.append(hotel)
        check_in_dates.append(check_in_date)
        check_out_dates.append(check_out_date)

# Create list of ids, hotels, check-in, check-out
ids.pop(0)
hotels.pop(0)
cities.pop(0)
check_in_dates.pop(0)
check_out_dates.pop(0)

URL = 'https://www.google.com/travel/hotels'
final_data = []
OTA_list = []  # Online Travel Agent
price_list = []

for i in range(len(ids)-116):  # Delete -116 if you want to scrape in one run all the row in csv
    OTA_list = []  # Online Travel Agent
    price_list = []
    # setting the webdriver for chrome
    service = Service(executable_path="C:\Development\chromedriver.exe")  # Path for Chrome web driver
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=service, options=options)
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    driver.get(URL)
    sleep(1)
    hotel_name = hotels[i]
    city = cities[i]
    try:
        # enter hotel name
        x_button = driver.find_element(By.CLASS_NAME, 'SS0SXe').find_element(By.TAG_NAME, 'button')
        actions.move_to_element(x_button).click().perform()
        search_bar = driver.find_elements(By.TAG_NAME, 'input')[1]
        print(f"Entering The Hotel Name: {hotel_name}.")
        search_bar.send_keys(hotel_name + " " + city)
        search_bar.send_keys(Keys.ENTER)
        sleep(2)
        try:
            container = driver.find_element(By.CLASS_NAME, 'PVOOXe')
        except:
            container = False
        if container:
            print("Price option does not exists. Hence, go back to main page and input the hotel name without address.")
            driver.get(URL)
            sleep(5)
            x_button = driver.find_element(By.CLASS_NAME, 'SS0SXe').find_element(By.TAG_NAME, 'button')
            actions.move_to_element(x_button).click().perform()
            search_bar = driver.find_elements(By.TAG_NAME, 'input')[1]
            search_bar.send_keys(hotel_name)
            search_bar.send_keys(Keys.ENTER)
        else:
            print("No container. Hence, we continue to the next process.")
        sleep(4)
        try:
            price_tab = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prices"]')))
            actions.move_to_element(price_tab).click().perform()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except:
            price_tab = wait.until(EC.element_to_be_clickable((By.ID, 'prices')))
            actions.move_to_element(price_tab).click().perform()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Change the currency
        sleep(1)
        try:
            currency = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prices"]/div/c-wiz[2]/footer/div[1]/c-wiz/button')))
            currency.click()
        except:
            currency = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prices"]/c-wiz[2]/div/c-wiz[2]/footer/div[1]/c-wiz/button')))
            currency.click()
        sleep(4)
        usd = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="USD"]')))
        actions.move_to_element(usd).click().perform()
        done_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[6]/div/div[2]/div[3]/div[2]/button')
        sleep(1)
        done_button.click()

        # Check-in date
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(3)
        check_in = driver.find_element(By.XPATH,
                                       '//*[@id="prices"]/c-wiz/c-wiz/div/div/div/div/div/div/div/section/div[1]/div[1]/div[1]/div/div[2]/div[1]')

        actions.move_to_element(check_in).click().perform()
        try:
            survey_popup = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'scSharedMaterialbuttonroot scSharedMaterialbuttonnavigational scSharedMaterialbuttonicon-only')))
            actions.move_to_element(survey_popup).click().perform()
            print("Close pop-up survey.")
        except:
            print("No pop-up survey.")
        date_check_in = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[aria-label='{check_in_dates[i]}']")))
        print(f'Input check-in date: {check_in_dates[i]}.')
        sleep(3)
        actions.move_to_element(date_check_in).click().perform()
        date_check_out = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[aria-label='{check_out_dates[i]}']")))
        print(f'Input check-out date: {check_out_dates[i]}.')
        sleep(3)
        actions.move_to_element(date_check_out).click().perform()
        sleep(2)
        try:
            google_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/a')))
        except:
            google_icon = False
        try:
            sign_in = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gb_ja gb_ka gb_ge gb_gd')))
        except:
            sign_in = False
        if google_icon:
            # create an ActionChains instance and move the mouse to the desired location
            actions.move_to_element(google_icon).move_by_offset(0, 100)
            # perform the click action
            actions.click().perform()
        else:
            sleep(2)
            sign_in = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'gb_1c')))
            actions.move_to_element(sign_in).move_by_offset(-100, 0)
            actions.click().perform()
            print("Click a point close to sign in button.")

        sleep(3)
        # scraping process
        print("Scraping process.")
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        sleep(3)
        try:
            not_available = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prices"]/c-wiz/c-wiz/div/div/div/div/div/div/div/section/div[2]/c-wiz/c-wiz/div[1]/div/div')))
            not_available_window2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prices"]/c-wiz[1]/c-wiz/div/div/div/div/div/div/div/section/div[2]/c-wiz/c-wiz/div[1]')))
            if not_available:
                not_available = not_available
                print('Not available is true from try if.')
            elif not_available_window2:
                not_available = not_available_window2
                print('Not available is true from try if 2.')
        except:
            not_available = False
            print('Not available is false.')
        try:
            contact_this_property = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'MEVoGd AdWm1c')))
            contact_this_property_window2 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="prices"]/c-wiz[1]/c-wiz/div/div/div/div/div/div/div/section/div[2]/c-wiz/div[1]/div[1]/div[1]')))

            if contact_this_property:
                contact_this_property = contact_this_property
                print("Contact this property from try if.")
            elif contact_this_property:
                contact_this_property = contact_this_property_window2
                print("Contact this property from try if 2.")
        except:
            contact_this_property = False
            print('Contact this property is false.')
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(1)

        if not_available:
            # create dictionary
            id_hotel = ids[i]
            check_outs = check_out_dates[i]
            check_ins = check_in_dates[i]
            data = {
                'ID': id_hotel,
                'Hotel': hotel_name,
                'Agents': 'Not Available',
                'Check_in': check_ins,
                'Check_out': check_outs,
                'Price': 'Not Available',
            }
            final_data.append(data)
            print(f'Row {i+1}: {hotel_name} is not available.')
            sleep(2)
        elif contact_this_property:
            # create dictionary
            id_hotel = ids[i]
            check_outs = check_out_dates[i]
            check_ins = check_in_dates[i]
            data = {
                'ID': id_hotel,
                'Hotel': hotel_name,
                'Agents': 'Contact this property',
                'Check_in': check_ins,
                'Check_out': check_outs,
                'Price': 'Contact this property',
            }
            final_data.append(data)
            print(f'Row {i + 1}: {hotel_name} Contact this property.')
            sleep(2)
        else:
            # Retrieve the Online agent travels and the prices
            try:
                sleep(2)
                more_option = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'bbRZy')))
                actions.move_to_element(more_option).click().perform()
                print('Click "more-option" bar.')
                sleep(2)
            except:
                print('No "more-option" button. Continue Scraping.')

            driver.execute_script("window.scrollTo(0, 0);")
            price_container = wait.until(EC.element_to_be_clickable(
                (
                By.XPATH, '//*[@id="prices"]/c-wiz/c-wiz/div/div/div/div/div/div/div/section/div[2]/c-wiz/div/div/div[2]')))
            names = price_container.find_elements(By.CLASS_NAME, 'NiGhzc')
            prices_row = price_container.find_elements(By.CLASS_NAME, 'pNExyb')
            for name in names:
                name_text = name.text.replace('\n', " ")
                OTA_list.append(name_text)
                while ("" in OTA_list):
                    OTA_list.remove("")
            for price in prices_row:
                price_text = price.text
                price_list.append(price_text)
                while ("" in price_list):
                    price_list.remove("")
            print(f'Price list {len(price_list)}')
            print(price_list)
            print(f'OTA list {len(OTA_list)}')
            print(OTA_list)

            # create dictionary
            id_hotel = ids[i]
            hotel_title = hotels[i]
            check_outs = check_out_dates[i]
            check_ins = check_in_dates[i]
            for j in range(len(OTA_list)):
                data = {
                    'ID': id_hotel,
                    'Hotel': hotel_title,
                    'Agents': OTA_list[j],
                    'Check_in': check_ins,
                    'Check_out': check_outs,
                    'Price': price_list[j],
                }
                final_data.append(data)
            print(f"Row {i+1}: {hotel_name} successfully scraped.")

    except:
        # create dictionary
        id_hotel = ids[i]
        hotel_title = hotels[i]
        check_outs = check_out_dates[i]
        check_ins = check_in_dates[i]
        hotel_name = hotels[i]
        data = {
            'ID': id_hotel,
            'Hotel': hotel_name,
            'Agents': 'None',
            'Check_in': check_ins,
            'Check_out': check_outs,
            'Price': 'None',
        }
        re_attempt.append(data)
        print("Failed to scrape.")
    if i % 10 == 0:
        sleep(5)
    else:
        sleep(3)
    driver.close()


#  create csv file
df = pd.DataFrame(final_data)
df.to_csv('final_data.csv', index=False)

print("Data created successfully")
end = time.time()
print(f"Completed in {(end - start)/60:.2f} minutes")
print("************")
print(f"List of failed row : {re_attempt}")
print(f"Number of failed: {len(re_attempt)}")



