#!/usr/bin/python3
#
# Usage: favbet.py 
# https://www.favbet.com/en/bets/#tour=17745&event=4198442

import json
import os
import re
import sys
import glob

from bs4 import BeautifulSoup
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

import util

BOOKIE_NAME = "Lsbet"
BOOKIE_URL = "https://www.lsbet.com/en-GB/sportsbook/eventpaths/multi/[223517]?utf8=%E2%9C%93&filter_options%5B%5D=450%7C209&commit=Refresh"

def main():
  htmls = getHtml(sys.argv) util.getHtml(sys.argv, selenium, BOOKIE_NAME)
  players = []
  for html in htmls:
    players.extend(getPlayers(html))
  util.printPlayers(players)

def selenium():
  with closing(Firefox()) as browser:
    htmls = []
    browser.get(BOOKIE_URL)
    WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='extra-events']")))
    for i in range(5):
      # browser.refresh()
      elements = browser.find_elements_by_xpath("//span[@class='extra-events']")
      # icons other icon-other-gourmands
      e = elements[i]
      e.click()
      WebDriverWait(browser, timeout=10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='event-outcomes']")))
      htmls.append(browser.page_source)
      element = browser.find_element_by_xpath("//span[@class='extra-events selected']")
      element.click()
      WebDriverWait(browser, timeout=10).until(EC.invisibility_of_element_located((By.XPATH, "//div[@class='event-outcomes']")))
    return htmls

def getPlayers(html):
  soup = BeautifulSoup(html, "html.parser")
  pll = soup.findAll("span", "name ellipsis")
  pl = soup.findAll("span", "formatted_price")
  players = []
  for a, b in zip(pll, pl):
    player = util.Player()
    player.a = a.find(text=True)
    player.b = b.find(text=True)
    players.append(player)
  return players

if __name__ == '__main__':
  main()
