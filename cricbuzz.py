import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

url = "http://www.cricbuzz.com/"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html.parser')
#print (soup.find("head").find("title").text)


links  = soup.find_all("a")
#print (links)

#for link in links:
#    print (link.text)

scorinfo = ""


data = soup.find("div", {"class":"cb-col cb-col-25 cb-mtch-blk"})
#print (data)

for item in data:
    #print (item.find_all("div",{"class":"cb-ovr-flo cb-hmscg-tm-nm"}))
    scr_list = item.find_all("div",{"class":"cb-ovr-flo"})
    for info in scr_list:
        scorinfo = scorinfo+info.text+"\n"
        print(scorinfo)


url2 = "http://site23.way2sms.com/content/index.html"
#r = requests.get(url2)
#soup = BeautifulSoup(r.content, 'html.parser')

driver = webdriver.Chrome(executable_path=r"C:\Python34\Scripts\chromedriver.exe")
driver.get(url2)

username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
form = driver.find_element_by_id("lgnFrm")

username.send_keys("7893064752")
password.send_keys("Nishuway")
form.submit()

driver.find_element_by_css_selector(".button.br3").click()

driver.find_element_by_id("sendSMS").click()

frame = driver.find_element_by_id('frame')
driver.switch_to.frame(frame)

mob = driver.find_element_by_id("mobile")

#use click and clear if element does not send keys.
#mob.click()
#mob.clear()
mob.send_keys("8122357897")

message = driver.find_element_by_css_selector("#message")
#message.click()
#message.clear()
message.send_keys(scorinfo)

smsbtn = driver.find_element_by_css_selector(".button.br2up")
smsbtn.click()
