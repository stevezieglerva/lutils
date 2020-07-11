from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import glob
import subprocess
import shutil
import time
import json
import re
from urllib.parse import urlparse
from datetime import datetime
from S3TextFromLambdaEvent import *


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
    print(f"Started at {datetime.now()}")

    _init_bin("headless-chromium")
    _init_bin("chromedriver")

    for filename in glob.iglob("/tmp/**/*", recursive=True):
        print(filename)

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

    try:

        bucket = os.environ["s3_bucket"]
        for records in event["Records"]:
            message = json.loads(records["Sns"]["Message"])
            print(message)
            url = message["line"]
            res = download_page(url, chrome_options)
            status_code = 200
            print(str(status_code) + "-" + url)
            result = {
                "processing_type": "async download urls",
                "url": url,
                "status_code": status_code,
                "length": len(res),
            }
            print(f"processed url: {result}")
            url_parts = urlparse(url)
            domain = re.sub(r"[^a-zA-Z0-9-_.]", "_", url_parts.netloc)
            filename = re.sub(r"[^a-zA-Z0-9-_.]", "_", url)
            s3_key = f"lutil-download-url/latest/{domain}/{filename}"
            create_s3_text_file(
                bucket, s3_key, res,
            )
            print(f"File saved to: {s3_key}")
            timestamp = datetime.now().isoformat()
            s3_key = f"lutil-download-url/{domain}/{filename}.{timestamp}"
            create_s3_text_file(
                bucket, s3_key, res,
            )
            print(f"File saved to: {s3_key}")
            print(f"Finished at {datetime.now()}")

    except Exception as e:
        print("Exception: " + str(e))
        raise (e)
        return {"msg": "Exception"}

    print(f"Finished at {datetime.now()}")

    return {"msg": "Success"}


def download_page(url, chrome_options):
    driver = webdriver.Chrome(chrome_options=chrome_options)
    page_data = ""
    driver.get(url)
    time.sleep(2)
    page_data = driver.page_source
    driver.close()
    return page_data

