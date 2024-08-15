from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from DrissionPage import ChromiumOptions, ChromiumPage
import pytest
from pytest_bdd import scenario, given, when, then
import time

# Login to firefly
driver = ChromiumPage()
driver.get('https://demo.firefly-iii.org/login')
driver.ele('#remember').check()
driver.ele('.d-grid gap-2').click()

# Navigate to create transactions
driver.ele('#transaction-menu').click()
driver.ele('Expenses').click()
driver.ele('.fa fa-plus fa-fw').click()