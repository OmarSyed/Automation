import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException


def parse_date(input):
    string = ""
    if len(str(input)) < 5:
        return string
    for i in range(5, 10):
        if str(input)[i] == '-':
            string += '/'
        else:
            string += str(input)[i]
    return string

def wait_xpath_presence(url):
    WebDriverWait(squareup, 30).until(EC.presence_of_all_elements_located(
        (By.XPATH, url)))  # wait for element to appear
    return
def wait_xpath_clickable(url):
    WebDriverWait(squareup, 10).until(
        EC.element_to_be_clickable((By.XPATH, url)))
    return
def wait_xpath_visibility(url):
    WebDriverWait(squareup, 10).until(expect.visibility_of_element_located((By.XPATH, url)))
    return
def wait_class_clickable(url):
    WebDriverWait(squareup, 10).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, url)))
    return
def wait_class_presence(url):
    WebDriverWait(squareup, 10).until(EC.presence_of_all_elements_located((By.XPATH, url)))
    return
def wait_css_presence(url):
    WebDriverWait(squareup, 10).until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, url)))  # wait for element to appear
    return
def css_finder(url):
    return squareup.find_element(By.CSS_SELECTOR, url)
def xpath_finder(url):
    return squareup.find_element_by_xpath(url)
def id_finder(url):
    return squareup.find_element_by_id(url)
def link_text_finder(url):
    return squareup.find_element_by_link_text(url)
def class_finder(url):
    return squareup.find_element(By.CLASS_NAME, url)
def retryingClassFindClick(url):
    num_occurrances = 0
    while num_occurrances < 10:
        try:
            class_finder(url).click()
        except StaleElementReferenceException:
            num_occurrances += 1
            continue
        except NoSuchElementException:
            num_occurrances += 1
            continue
    print("Failed to find page element.")

def clickInvoices():
    wait_css_presence("#sq-app-container > div.page-layout > "
                      "div.filter-bar.filter-bar--mobile-fullbleed.l-invoices-list-header > "
                      "div.filter-bar__actions > button")
    css_finder("#sq-app-container > div.page-layout > "
               "div.filter-bar.filter-bar--mobile-fullbleed.l-invoices-list-header > "
               "div.filter-bar__actions > button").click()  # click create invoice tab

def createInvoice(row_start, data):
    try:
        while row_start < row_count:
            clickInvoices()
            j = 0
            for i in range(len(column_headers)):
                if "Location" in column_headers[i]:
                    wait_xpath_visibility("//input[@placeholder='Full Name']")
                    xpath_finder("//input[@placeholder='Full Name']").send_keys(data.iloc[row_start, i], Keys.ENTER)
                elif "Timestamp" in column_headers[i]:
                    wait_xpath_visibility("//input[@placeholder='Optional']")
                    xpath_finder("//input[@placeholder='Optional']").send_keys(parse_date(data.iloc[row_start, i]))
                elif "Email" in column_headers[i]:
                    if xpath_finder("//input[@placeholder='Email Address']").is_displayed():
                        xpath_finder("//input[@placeholder='Email Address']").send_keys(data.iloc[row_start, i])
                elif "Column" in column_headers[i] or "Price" in column_headers[i]:
                    if str(data.iloc[row_start, i - 1]) != 'nan' and str(data.iloc[row_start, i - 1]) != '0':
                        if j != 0:
                            xpath_finder("(//input[@placeholder='Add Item'])[" + str(j + 1) + "]").send_keys(
                                column_headers[i - 1])  # Add new item
                        else:
                            xpath_finder("(//input[@placeholder='Add Item'])").send_keys(
                                column_headers[i - 1])  # add first item
                        wait_class_clickable("l-invoices-edit-new-item-search__detail-additive")  # add custom item
                        # WebDriverWait(squareup, 10).until(EC.staleness_of((By.CLASS_NAME, "l-invoices-edit-new-item-search__detail-additive")))
                        # retryingClassFindClick("l-invoices-edit-new-item-search__detail-additive") #try looking for stale element
                        class_finder("l-invoices-edit-new-item-search__detail-additive").click()
                        if j != 0:
                            wait_xpath_clickable("(//input[@placeholder='0'])[" + str(j + 1) + "]")  # add quantity
                            xpath_finder("(//input[@placeholder='0'])[" + str(j + 1) + "]").clear()
                            xpath_finder("(//input[@placeholder='0'])[" + str(j + 1) + "]").send_keys(
                                str(int(data.iloc[row_start, i - 1])))
                        else:
                            wait_xpath_clickable("(//input[@placeholder='0'])")  # add initial item quantity
                            xpath_finder("(//input[@placeholder='0'])").clear()
                            xpath_finder("(//input[@placeholder='0'])").send_keys(str(int(data.iloc[row_start, i - 1])))
                        if data.iloc[row_start, i] != 'nan':
                            if j != 0:
                                wait_xpath_clickable("(//input[@placeholder='$0.00'])[" + str(j + 1) + "]")  # add price
                                xpath_finder("(//input[@placeholder='$0.00'])[" + str(j + 1) + "]").clear()
                                xpath_finder("(//input[@placeholder='$0.00'])[" + str(j + 1) + "]").send_keys(
                                    str(float(data.iloc[row_start, i])), Keys.TAB)
                                j += 1
                            else:
                                wait_xpath_clickable("(//input[@placeholder='$0.00'])")  # add initial item price
                                xpath_finder("(//input[@placeholder='$0.00'])").clear()
                                xpath_finder("(//input[@placeholder='$0.00'])").send_keys(str(float(data.iloc[row_start, i])), Keys.TAB)
                                j += 1
        xpath_finder("//button[@class='button--secondary button button button--loading ember-view']").click()  # find save as draft
        row_start += 1
    except:
        squareup.find_element_by_class_name('sheet-layout__headerbar-close').click() # click close
        createInvoice(row_start, data) #restart


############ Getting excel file ########################################
user = input("Enter your Squareup username: ")
password = input("Enter your Squareup password: ")
file = input("Enter file pathname: ")
data = pd.read_excel(file, 0, 0) #get excel file
data = data.dropna(0, subset=['Location'])#include only rows without nan values under location header
data = data.dropna(1, how='all') #drop empty columns
column_headers = data.columns.values.tolist() #list of column headers
row_count = len(data.index) # number of rows

############ Opening up webpage #########################################
squareup = webdriver.Chrome()
squareup.get("https://www.squareup.com")

############ Signing in #################################################
xpath_finder("//*[@id='header']/nav[1]/div/div[3]/a[1]/div[2]").click() #Click on sign in
xpath_finder("//*[@id='email']").send_keys(user) #entering username
xpath_finder("//*[@id='password']").send_keys(password) #enter password
xpath_finder("//*[@id='sign-in-button']").click()

############ Invoice automation ##########################################
wait_xpath_presence("//*[@id='dashboard-navigation__container']/div[2]/div[2]/div/div/div[3]/div[3]/a") #wait for the invoice tab
xpath_finder("//*[@id='dashboard-navigation__container']/div[2]/div[2]/div/div/div[3]/div[3]/a").click()  # click invoice tab
recovery = 0
createInvoice(1, data)
#    wait_xpath_clickable("//button[@class='button']") #wait for done
#    xpath_finder("//button[@class='button']").click() #click done

     #   print("Webpage took too long to load or an element you were looking for was not found.")
