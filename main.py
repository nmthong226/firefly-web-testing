from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from DrissionPage import ChromiumOptions, ChromiumPage
import pytest
from pytest_bdd import scenario, given, when, then
from pytest import fixture
import time

# Login to firefly
@fixture
def driver():
    # Setup: initialize the driver
    driver = ChromiumPage()
    yield driver
    # Teardown: quit the driver
    driver.quit()
    driver.ele('Logout')

def login_firefly(driver):
    driver.get('https://demo.firefly-iii.org/login')
    remember_checkbox = driver.ele('#remember')
    if remember_checkbox:
        remember_checkbox.check()
    login_button = driver.ele('.d-grid gap-2')
    if login_button:
        login_button.click()

# Navigate to create transactions
def navigate_to_transactions(driver):
    driver.ele('#transaction-menu').click()
    driver.ele('Expenses').click()
    driver.ele('.fa fa-plus fa-fw').click()

# Create new transaction
def create_new_transaction(driver):
    driver.ele('@name=description[]').input('Sample transaction')
    driver.wait(3)
    driver.ele('@name=source[]').input('Cash')
    driver.wait(3)
    driver.ele('Cash').click()
    driver.wait(3)
    driver.ele('@name=destination[]').input('Cash account')
    driver.wait(3)
    driver.ele('@name=amount[]').input('100')
    driver.wait(3)
    driver.ele('#submitButton').click()
    driver.wait(3)

def test_firefly_transactions(driver):
    login_firefly(driver)
    navigate_to_transactions(driver)
    create_new_transaction(driver)
    try:
        fail_message = driver.ele('.alert alert-danger alert-dismissible')
        assert fail_message is not None, "Transaction creation failed: Failed message found."
    except Exception as e:
        assert False, f"Transaction creation failed: {str(e)}"