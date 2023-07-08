import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import requests
import os
import time
import base64
from PIL import Image
from io import BytesIO

def download_image(query, download_path):
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    driver = uc.Chrome(options=options)

    try:
        time.sleep(2)
        driver.get(f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=99&q=site:wikipedia.org+{query.replace(' ', '+')}")

        tos = driver.find_elements(By.CLASS_NAME, "VfPpkd-vQzf8d")
        for to in tos:
            if to.text.lower() == "tout refuser":
                to.click()
                break
        time.sleep(1)
        f = 0
        while f < 10:
            try:
                driver.get(f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=99&q=site:wikipedia.org+{query.replace(' ', '+')}")

                image = driver.find_element(By.CLASS_NAME, "rg_i").click()
                
                break
            except:
                f += 1
            finally:
                time.sleep(1)
        if f == 10:
                raise Exception("No image found")
        time.sleep(5)
        while True:
            try:
                image = driver.find_element(By.CLASS_NAME, "iPVvYb").get_attribute("src") or driver.find_element(By.CLASS_NAME, "pT0Scc").get_attribute("src") or driver.find_element(By.CLASS_NAME, "r48jcc").get_attribute("src") or ""
                if image != "":
                    break
            except Exception as a:
                print(a)
                pass
            finally:
                time.sleep(1)            
        image_content = None

        if image.startswith("data:"):
            image_content = base64.b64decode(image.split(",")[1])
        else:
            #define a common user agent for all requests
            headers = {'User-Agent': 'FABLE/1.2 (Website coming soon; me@paillat.dev)'}

            response = requests.get(image, stream=True, headers=headers)
            response.raise_for_status()
            image_content = response.content

        # Convert all images to PNG format using PIL, if they aren't already
        img = Image.open(BytesIO(image_content))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.save(download_path)  # download_path already contains the output filename

        print('Image downloaded successfully at ', download_path)
        
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()

if __name__ == "__main__":
    #test
    download_image("test", os.path.join(os.getcwd(), "test.png"))
