import pyderman
import requests
from pathlib import Path
from selenium import webdriver

def init_scraper():
    cdi_path = Path('./chromedriver/')
    cdi_install_path = pyderman.install(file_directory=cdi_path, verbose=True, chmod=True, overwrite=False, version=None)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("--log-level=3")

    return webdriver.Chrome(executable_path=cdi_install_path, options=chrome_options)

def scrape_trackmania_io():
    driver = init_scraper()
    URL = 'https://trackmania.io'

    track_name = ''
    track_author_name = ''
    author_time = ''
    image_url = ''

    driver.implicitly_wait(3)
    driver.get(URL)
    driver.find_element_by_link_text('Leaderboards').click()
    track_info = driver.find_elements_by_class_name('level-left')[1]

    track_name = track_info.find_element_by_tag_name('h1').text
    track_author_name = track_info.find_element_by_tag_name('h2').find_element_by_class_name('game-text').text
    author_time = driver.find_element_by_class_name('medal').text
    medal_thumbnail = driver.find_element_by_class_name('medal').find_element_by_tag_name('img').get_attribute('src')
    image_url = driver.find_element_by_class_name('thumbnail').get_attribute('src')

    driver.close()

    return [track_name, track_author_name, author_time, image_url, medal_thumbnail]

def save_screenshot(url, track_name: str):
    req = requests.get(url)
    with open(Path(f'./screenshots/{track_name}.jpg'), 'wb') as screenshot:
        screenshot.write(req.content)

if __name__ == "__main__":
    print(scrape_trackmania_io())
