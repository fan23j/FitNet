import io
import os
import time
import hashlib
import requests
from PIL import Image
from selenium import webdriver


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            # return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")
        return False

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
        return True
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
        return False


def search_and_download(search_term:str,driver_path:str,target_path='.',number_images=5, sleep_between_interactions=1):
    target_folder = os.path.join(target_path,'_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=sleep_between_interactions)
    
    urls = []
    for elem in res:
        result = persist_image(target_folder,elem)
        if result:
            urls.append(f"{elem}\n")
    with open(f"{target_folder}/urls.txt", 'w') as f:
        f.writelines(urls)
        print(f"SUCCESS - saved URL list in {target_folder}")
    print(f"Done..! {len(urls)} images were downloaded..")
    

def main(driver_path, search_terms, save_folder, no_of_images):
    
    images_per_class = no_of_images // len(search_terms)

    for search_term in search_terms:
        print(f'[INFO] Starting the category {search_term}')
        search_and_download(search_term=search_term,driver_path=driver_path,target_path=save_folder ,number_images=images_per_class, sleep_between_interactions=sleep_between_interactions)

if __name__ == '__main__':
    DRIVER_PATH = "./chromedriver" # Path to the Chrome driver. Downloaded according to your chrome version from https://chromedriver.chromium.org/downloads
    no_of_images = 10000 # Total number of images you need
    search_terms = ["exercise", "yoga", "workout", "calisthenics", "gym workout", "weight lifting", "treadmill exercise", "lunges", "pushups",
                    "squats", "dumbbell exercises","Standing overhead dumbbell presses", "Dumbbell rows",
                    "Single-leg deadlifts", "Burpees", "Side planks", "Planks", "Glute bridge",
                    "jump rope workout", "Alternate foot jump", "streatching", "fitness", "knee pushups", "Straight-leg donkey kick", "bird dog exercise",
                    "Side-lying hip abduction", "Bicycle crunch", "superman exercise",
                    "Dead bug exercise", "Hollow hold to jackknife", "ball exercises",
                    "aerobic exercises", "Anaerobic Exercise", "warmup exercises",
                    "Foam Rolling", "HIIT", "Isometrics", "Plyometrics", "reps exercise",
                    "Strength Training", "Tabata", "power lifting"] # The terms to be searched on the internet. Add or remove list items as you wish.
    save_folder = 'Downloaded' # Target folder to save the downloaded images
    sleep_between_interactions = 1 # Time in seconds between two adjacent image clicks (Give a enough time to fully load the image. Otherwise a low quality image will be downloaded.) Decide a value having done a test run.
    
    main(DRIVER_PATH, search_terms, save_folder, no_of_images)