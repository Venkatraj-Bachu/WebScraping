from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

website = 'https://www.cricbuzz.com/'
path = 'C:/Users/venka/chromedriver/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

series_button = driver.find_element_by_id('seriesDropDown')
series_button.click()

root = 'https://www.cricbuzz.com/cricket-schedule/series'
website = root
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')


page = soup.find(id='page-wrapper')
box = page.find('div', attrs={"ng-controller":"scheduleFilters"})
series = box.find_all('div', attrs={"ng-if":"((filtered_category == 0 || filtered_category == 9))"})
series_links = []
for series in series:
    series_links.append(series.find('a', href=True)['href'])

for series in series_links:
    try:
        website = 'https://www.cricbuzz.com' + series[:-7] + 'stats'
        driver.get(website)
        series_name = website.split('/')[5].upper()
        # print(series_name)
        file = open(f'{series_name}.csv','w')
        players_list = []
        innings = []
        runs = []
        players = driver.find_elements_by_xpath('//table/tbody/tr')
        for player in players:
            players_list.append(player.find_elements_by_xpath('./td')[1].text)
            innings.append(player.find_elements_by_xpath('./td')[3].text)
            runs.append(player.find_elements_by_xpath('./td')[4].text)
        df = pd.DataFrame({'Player': players_list, 'Innings': innings, 'Runs': runs})
        df.to_csv(f'{series_name}.csv', index=False)
        # print(df)
    except:
        print(f'Link to {website.split("/")[5].upper()} has broken')
driver.quit()
