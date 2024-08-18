from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from DrissionPage import ChromiumOptions, ChromiumPage
import pytest
from pytest_bdd import scenario, given, when, then
from pytest import fixture
import time
import csv
from dotenv import load_dotenv
import os

#Load ENV
load_dotenv()
APP_LINK = os.getenv('APP_LINK')
ACCOUNT_EMAIL = os.getenv('ACCOUNT_EMAIL')
ACCOUNT_PASSWORD = os.getenv('ACCOUNT_PASSWORD')

# Function to load CSV data
def load_transaction_data(csv_file):
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        transactions = [row for row in csv_reader]
    return transactions

# Login to firefly
@fixture
def driver():
    driver = ChromiumPage()
    yield driver
    driver.ele('.logout-link').click()
    driver.wait(2)
    driver.quit()

def login_firefly(driver):
    driver.get(APP_LINK)
    driver.ele('@name=email').input(ACCOUNT_EMAIL)
    driver.wait(2)
    driver.ele('@name=password').input(ACCOUNT_PASSWORD)
    driver.wait(2)
    remember_checkbox = driver.ele('#remember')
    if remember_checkbox:
        remember_checkbox.check()
    login_button = driver.ele('.d-grid gap-2')
    if login_button:
        login_button.click()
        driver.wait(2)
    driver.ele('#transaction-menu').click()
    driver.ele('Expenses').click()

# Create new transaction
def create_new_transaction(driver, transaction_data):
    # Input the description
    driver.ele('@name=description[]').input(transaction_data['description'])
    driver.wait(2)

    # Input the source account
    driver.ele('@name=source[]').input(transaction_data['source'])
    driver.wait(2)
    suggest_source = driver.ele(transaction_data['source'])
    if suggest_source:
        suggest_source.click()
        driver.wait(2)

    # Input the destination account
    driver.ele('@name=destination[]').input(transaction_data['destination'])
    driver.wait(2)
    
    # Input the date (day, month, year)
    day, month, year = transaction_data['date'].split('/')
    driver.ele('@name=date[]').input(day)
    driver.wait(1)
    driver.ele('@name=date[]').input(month)
    driver.wait(1)
    driver.ele('@name=date[]').input(year)
    driver.wait(2)
    
    # Input the amount
    driver.ele('@name=amount[]').input(transaction_data['amount'])
    driver.wait(2)

    # Submit the form
    driver.ele('#submitButton').click()
    driver.wait(2)

def test_firefly_transactions(driver):
    login_firefly(driver)
    transactions = load_transaction_data('transaction_data.csv')
    results = []
    for transaction_data in transactions:
        try:
            driver.ele('Expenses').click()
            driver.wait(2)
            driver.ele('.fa fa-plus fa-fw').click()
            driver.wait(2)
            create_new_transaction(driver, transaction_data)
            expected_result = transaction_data['expected_result']
            fail_message = driver.ele('.alert alert-danger alert-dismissible')
            if expected_result == 'failure' and fail_message != None:
                results.append(f"PASS: {transaction_data['description']} - Failure message found as expected.")
            elif expected_result == 'success' and fail_message == None :
                results.append(f"PASS: {transaction_data['description']} - No failure message as expected.")
            else:
                results.append(f"FAIL: {transaction_data['description']} - Unexpected result.")
            driver.wait(2)
        except Exception as e:
            results.append(f"FAIL: {transaction_data['description']} - Exception occurred: {str(e)}")
    for result in results:
        print(result)
    assert all("PASS" in result for result in results), "Some test cases failed."