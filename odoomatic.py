#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# -*- coding: utf-8 -*-
import sys
import os
import time
import simplejson as json
from bs4 import BeautifulSoup

# Import the Selenium 2 namespace (aka "webdriver")
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

os.environ["PATH"] += ":/home/alexandre/Documentos/Programming/Python/testesOdoo/"


# Google Chrome 
driver = webdriver.Chrome('./chromedriver')

# Firefox 
#WebDriver driver = new FirefoxDriver();

# Driver headless
#driver= webdriver.PhantomJS()
#driver.set_window_size(1120, 550)


wait = WebDriverWait(driver, 30)

def fill_box(box_id,text):
  
  text_box = wait.until(EC.element_to_be_clickable((By.ID,box_id)))
  #text_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID,box_id)))
  text_box.click() #por alguma razao a caixa de texto tem que ser clicada
  text_box.send_keys(Keys.CONTROL+"a")
  text_box.send_keys(text)

def do_form_fill(box_id_list):
  for (box_id,text) in  box_id_list:
    fill_box(box_id,text)
    
def click_link(text):
  link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,text)))
  #link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT,text)))
  link.location_once_scrolled_into_view
  link.click()

def click_button(text):
  xpath=".//button[contains(.,'%s')]"%(text)
  button = wait.until(EC.element_to_be_clickable((By.XPATH,xpath)))
  button.click()

def do_menu_sequence(menu_list):
  for menu_text in menu_list:
    click_link(menu_text)

def do_login(driver,database,user,passwd):
  db_dropdown = wait.until(EC.element_to_be_clickable((By.ID,'db')))
  db_select = Select(db_dropdown)
  db_select.select_by_visible_text(database)

  do_form_fill([('login',user),('password',passwd)])

  click_button('Acessar')

def fill_dropdown(driver,time_gap,box_id,text):
  element=wait.until(EC.element_to_be_clickable((By.ID,box_id)))
  element.clear()
  time.sleep(0.3)
  element.send_keys(text)
  time.sleep(time_gap)
  #time.sleep(time_gap)
  ActionChains(driver).send_keys(Keys.TAB).perform()


sys.stdout.flush()

with open(sys.argv[1]) as json_data_file:
  str_json=json_data_file.read()
  invoice = json.loads(str_json.decode("utf-8"))

hostname=sys.argv[2]
database=sys.argv[3]
username=sys.argv[4]
password=sys.argv[5]

driver.get(hostname)
#wait = WebDriverWait(driver, 10)
do_login(driver,database,username,password)

do_menu_sequence(['Vendas','Pedidos de Venda'])
time.sleep(5)
click_button('Criar')


field_boxes= invoice['head']['metadata']
field_values= invoice['head']['data']
for i in range(len(field_boxes)):
  fill_dropdown(driver,1,field_boxes[i],field_values[i])

click_link("Adicionar um item")
invoice_line=invoice['line']
for produto in invoice_line["data"]:
  print "Preenchendo %s" %(produto[0])
  time.sleep(0.5)
  fill_dropdown(driver,0.8,invoice_line['metadata'][0],produto[0])
  time.sleep(0.2)
  fill_box(invoice_line['metadata'][1],produto[1])
  time.sleep(0.2)
  fill_box(invoice_line['metadata'][2],produto[2])
  time.sleep(0.2)
  fill_box(invoice_line['metadata'][3],produto[3])
  time.sleep(0.2)
  click_button("Salvar & Novo")
time.sleep(1)
click_link("Descartar")

# Close the browser!
#driver.quit()
