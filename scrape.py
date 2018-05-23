from selenium import webdriver
from time import sleep
from csv import  DictWriter
import config


b = webdriver.Chrome()

b.get(config.vars['URL'])

b.implicitly_wait(3)

results = []

# Select Sell 
operation_type = b.find_element_by_css_selector('div#select-type')
operation_type.click()

# assert operation_type.find_element_by_css_selector('span').text == 'SELL'

country_dropdown = b.find_element_by_css_selector('img#country-flag')
country_input = b.find_element_by_css_selector('input#country-input')
country_dropdown_results = b.find_elements_by_css_selector('ul#country-dropdown')

country_dropdown.click()
country_input.send_keys(config.vars['COUNTRY'])
country_dropdown_results[0].click()

sleep(1)

offers_page_link = b.find_elements_by_css_selector('a.payment-method')[0]
offers_page_link.click()

### OFFERS PAGE

# show all offers (click 'View more' button until it disappears)
btn = b.find_elements_by_css_selector('button')

while btn:
	btn[0].click()
	sleep(.5)
	btn = b.find_elements_by_css_selector('button')

offers = b.find_elements_by_css_selector(f'div.{config.vars["CLASS_OFFER"]}')

for offer in offers:

	offer_details = offer.text.split('\n')

	user = offer_details[0]
	trades = offer_details[1]
	bank = offer_details[3]
	location = f'{offer_details[4]}, {offer_details[5]}'
	amounts = offer_details[6]
	price = offer_details[8]

	results.append({
		'user': user,
		'trades': trades,
		'bank': bank,
		'location': location,
		'amounts': amounts,
		'price': price
		})


with open('offers.csv', 'w') as file:
	headers = ['user', 'trades', 'bank', 'location', 'amounts', 'price']
	csv_writer = DictWriter(file, fieldnames=headers)
	csv_writer.writeheader()

	for result in results:
		csv_writer.writerow(result)

b.quit()