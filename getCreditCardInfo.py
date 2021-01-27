from selenium import webdriver
from pathlib import Path
import time, random, countries, os
import mysql.connector as connectSQL


def insertData():
    mySQL = connectSQL.connect(
        host='localhost',
        user='root',
        password='',
        database='Credit_Cards'
    )
    myCursor = mySQL.cursor()
    sql = '''INSERT INTO
			Users (CardNumber, Name, Address, Country, CVV, EXP)
			VALUES (%s,%s,%s,%s,%s,%s)'''

    values = [
        (getCardNumber, getName, getAddress, getCountry, getCVV, getEXP)
    ]

    myCursor.executemany(sql, values)
    mySQL.commit()
    print(myCursor.rowcount, 'was inserted')


def find_driver():
    PATH = []
    os.chdir('/')
    for root, dirs, files in os.walk(os.getcwd()):
        if 'msedgedriver.exe' in files:
            PATH.append(os.path.join(root, 'msedgedriver.exe'))
            for the_driver in PATH:
                return the_driver


driver = webdriver.Edge(find_driver())

driver.get("https://cardgenerator.io/mastercard-credit-card-generator/")

while True:
    searchCountry = driver.find_element_by_id("personCountryInput")
    searchCountry.click()

    jumble = random.choice(countries.country_container)
    for country in countries.country_container:
        #print("Countries Intercepted: " + country)
        getCountry = driver.find_element_by_xpath(jumble)
        print(getCountry.text)
        getCountry.click()
        break

    generateCard = driver.find_element_by_xpath(
        '/html/body/div[6]/div[2]/div/div[2]/div[1]/div/div[2]/div[2]/div/div[1]/div/div[1]/button')
    generateCard.click()
    generateCard.click()

    time.sleep(35)
    getCardNumber = driver.find_element_by_xpath(
        '//*[@id="card_number_id"]').text
    getName = driver.find_element_by_xpath('//*[@id="card_name_id"]').text
    getAddress = driver.find_element_by_xpath(
        '//*[@id="card_address_id"]').text
    getCountry = driver.find_element_by_xpath(
        '//*[@id="card_country_id"]').text
    getCVV = driver.find_element_by_xpath('//*[@id="card_cvv_id"]').text
    getEXP = driver.find_element_by_xpath('//*[@id="card_exp_id"]').text

    try:
        if Path('CreditCards.csv').exists():
            print('File Exists, proceeding to data collection.\n\n')
    except FileNotFoundError as ioerr:
        print('File could not be found. ', ioerr)

    print('Card Number: ' + getCardNumber)
    print('Name: ' + getName)
    print('Address: ' + getAddress)
    print('Country: ' + getCountry)
    print('CVV: ' + getCVV)
    print('EXP: ' + getEXP)

    with open('CreditCards.csv', 'a') as f:
        f.write(getCardNumber + ', ' + getName + ', ' + getAddress.replace(",", "") +
                ', ' + getCountry.replace(",", "") + ', ' + getCVV + ', ' + getEXP + '\n\n')

    time.sleep(1)
    print("\nCredit Card Information from " +
          getName + " successfuly stolen.\n")

    f.close()
    insertData()
