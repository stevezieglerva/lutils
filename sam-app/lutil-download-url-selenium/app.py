from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import glob
import subprocess
import shutil
import time

BIN_DIR = "/tmp/bin"
CURR_BIN_DIR = "/opt/python/bin"


def _init_bin(executable_name):
    start = time.clock()
    if not os.path.exists(BIN_DIR):
        print("Creating bin folder")
        os.makedirs(BIN_DIR)
    currfile = os.path.join(CURR_BIN_DIR, executable_name)
    newfile = os.path.join(BIN_DIR, executable_name)
    if os.path.exists(newfile):
        print(newfile + " already exists")
        return
    print("Copying binaries for " + executable_name + " in /tmp/bin")
    shutil.copy2(currfile, newfile)
    print("Giving new binaries permissions for lambda")
    os.chmod(newfile, 0o775)
    elapsed = time.clock() - start
    print(executable_name + " ready in " + str(elapsed) + "s.")


# driver = webdriver.Chrome(chrome_options=chrome_options)


def lambda_handler(event, context):
    _init_bin("headless-chromium")
    _init_bin("chromedriver")

    for filename in glob.iglob("/tmp/**/*", recursive=True):
        print(filename)

    # TODO implement
    print("Starting ...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1280x1696")
    chrome_options.add_argument("--user-data-dir=/tmp/user-data")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument("--v=99")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--data-path=/tmp/data-path")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--homedir=/tmp")
    chrome_options.add_argument("--disk-cache-dir=/tmp/cache-dir")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )
    chrome_path = "/tmp/bin/headless-chromium"
    chrome_options.binary_location = chrome_path

    driver = webdriver.Chrome(chrome_options=chrome_options)
    page_data = ""
    if "url" in event.keys():
        driver.get(event["url"])
        time.sleep(2)
        page_data = driver.page_source
    driver.close()
    print("Finished.")
    return page_data
