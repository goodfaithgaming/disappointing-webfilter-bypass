#import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

parser = argparse.ArgumentParser(
                    prog='Di$appointing WebFilter Bypass',
                    description='Generates /etc/hosts lines, even from networks with DNS filtering.')

parser.add_argument("domain")
parser.add_argument("-d", help="include variant that ends in '.'", action="store_true")
parser.add_argument("-w", help="include variant that starts with 'www.'", action="store_true")
parser.add_argument("-4", help="do IPv4 lookup", action="store_true")
parser.add_argument("-6", help="do IPv6 lookup", action="store_true")
parser.add_argument("-t", help="set timeout in seconds")

arguments = vars(parser.parse_args())
wait_time = 20

#print("# site?")
#site = input("#$>")
site = arguments["domain"]

driver = webdriver.Firefox()

wait = WebDriverWait(driver, 20)
driver.get("https://mxtoolbox.com/DnsLookup.aspx")
elem = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ucToolhandler_txtToolInput")
elem.clear()
elem.send_keys("a:" + site)
elem.send_keys(Keys.RETURN)
#time.sleep(2)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="tool-result-body"]')))
content = driver.find_element(By.XPATH, '//div[@class="tool-result-body"]')
items=content.find_elements(By.XPATH, './/tr/td[@class="table-column-IP_Address"]/a')
dnsarecords = []
for item in items:
    dnsarecords.append(item.text)

driver.get("https://mxtoolbox.com/DnsLookup.aspx")
elem = driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ucToolhandler_txtToolInput")
elem.clear()
elem.send_keys("aaaa:" + site)
elem.send_keys(Keys.RETURN)
#time.sleep(2)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="tool-result-body"]')))
content = driver.find_element(By.XPATH, '//div[@class="tool-result-body"]')
items=content.find_elements(By.XPATH, './/tr/td[@class="table-column-IPv6_Address"]/a')
dnsaaaarecords = []
for item in items:
    dnsaaaarecords.append(item.text)

#www = bool(input("# 'www.*'? "))
#dot = bool(input("# '*.'? "))
www = arguments["w"]
dot = arguments["d"]
domains = [site]
if www:
    domains.append('www.' + site)

if dot:
    domains.append(site + '.')

if www and dot:
    domains.append('www.' + site + '.')

domains = ' '.join(domains)
print("# ipv4:")
for record in dnsarecords:
    print(record + '\t' + domains)

print("# ipv6:")
for record in dnsaaaarecords:
    print(record + '\t' + domains)
