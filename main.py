from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
import threading

def create_options(path):
    options = webdriver.ChromeOptions()
    options.binary_location = "C:\Program Files\BraveSoftware\Brave-Browser\Application\\brave.exe"
    options.add_argument('ignore-certificate-errors')
    options.add_argument("--headless=new")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": path,  ### Set the path accordingly
             "download.prompt_for_download": False,  ## change the downpath accordingly
             "download.directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    return options


def driver_setup(path):
    brave_driver_path = "./chromedriver.exe"

    service = Service(brave_driver_path)

    options = create_options(path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver
def baixar_anime(anime):
    download_path = "Z:\Media\\" + anime["directory"]

    driver = driver_setup(download_path)

    driver.get(anime["url"])

    rows = driver.find_elements(by=By.CSS_SELECTOR, value="table.downloadpag_episodios tr td:nth-child({}) p a".format(anime["quality"]))

    links = []

    for row in rows:
        link = row.get_property('href')
        links.append(link)

    for link in links:
        driver.get(link)
        form = driver.find_element(by=By.CSS_SELECTOR, value="form button")
        form.click()
        botoes = driver.find_element(by=By.CSS_SELECTOR, value="div.botoes a")

        sleep(3)

        url = botoes.get_property('href')
        driver.execute_script("window.open(arguments[0], '_blank');", url)
        sleep(5)

qualities = {
    "sd": "1",
    "hd": "2",
    "full_hd": "3"
}

animes = [
    {
        "directory": "Sword Art Online",
        "url": "https://www.anitube.vip/download/animes-dublado/sword-art-online-dublado",
        "quality": qualities["hd"],
        "done": True
    },
    {
        "directory": "Dragon Ball Super HD",
        "url": "https://www.anitube.vip/download/animes-dublado/2586473a7c35262f225d7674bb73f2e253114534",
        "quality": qualities["hd"],
        "done": True
    },
    {
        "directory": "Fairy Tail HD",
        "url": "https://www.anitube.vip/download/animes-dublado/9138ff934dca1bdadde9af35b446e1613e31ec67",
        "quality": qualities["hd"],
        "done": True
    },
    {
        "directory": "Fairy Tail (2014) HD",
        "url": "https://www.anitube.vip/download/anime/7bfb1033655079c1d44ea97e3e56aaa9388d8291",
        "quality": qualities["hd"],
        "done": True
    },
    {
        "directory": "Naruto HD",
        "url": "https://www.anitube.vip/download/animes-dublado/60ef0f9f31d4b36acf9d6ce10394c80e0c8b2bb2",
        "quality": qualities["hd"],
        "done": True
    },
    {
        "directory": "Naruto Shippuden HD",
        "url": "https://www.anitube.vip/download/animes-dublado/7b6ac82e47029991251eefdf6ba0cb93d079083c",
        "quality": qualities["hd"],
        "done": True
    }
]
# for anime in animes:
#     baixar_anime(anime)
#     sleep(60)
threads = []
for anime in animes:
    if anime["done"]:
        continue
    thread = threading.Thread(target=baixar_anime, args=(anime,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()