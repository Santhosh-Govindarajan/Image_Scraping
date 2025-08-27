from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# === SETTINGS ===
media_url = "https://www.facebook.com/groups/dataanalystgroup/media" 
save_folder = "Cybersecurity_Media"
scroll_times = 20
pause_between_scrolls = 10
download_delay = 15

# Create folder if not exists
os.makedirs(save_folder, exist_ok=True)

# Chrome setup
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

# Step 1: Manual login
print("🚀 Chrome launched. Please log in manually.")
driver.get("https://facebook.com")
input("🔑 After logging in, press ENTER here to continue...")

# Step 2: Navigate to media page and scroll
print(f"🌐 Navigating to group media: {media_url}")
driver.get(media_url)
wait.until(EC.presence_of_element_located((By.TAG_NAME, "img")))

print(f"🔃 Scrolling {scroll_times} times to load images...")
for _ in range(scroll_times):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(pause_between_scrolls)

# Step 3: Collect links that open full image viewer (anchors around images)
print("🔍 Collecting image viewer links...")
link_elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/photo/")]')
links = list(set(a.get_attribute("href") for a in link_elements if a.get_attribute("href")))
print(f"🖼️ Found {len(links)} full image viewer links.")

# Open new tab for HD images
driver.execute_script("window.open('');")
hd_tab = driver.window_handles[1]

def enhance_to_1080p(url):
    upgrades = [
        ("p180x540", "p1080x1080"), ("p320x320", "p1080x1080"),
        ("s320x320", "s1080x1080"), ("p480x480", "p1080x1080"),
        ("p600x600", "p1080x1080"), ("p720x720", "p1080x1080"),
        ("p960x960", "p1080x1080"), ("s2048x2048", "p1080x1080"),
    ]
    for old, new in upgrades:
        if old in url:
            return url.replace(old, new)
    return url

def download_hd_image(view_url, index):
    driver.switch_to.window(hd_tab)
    driver.get(view_url)
    time.sleep(3)  # wait for page and image to load
    
    # The HD image in Facebook photo viewer is usually the largest <img> inside some div
    try:
        hd_img = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[contains(@style,"background-image")]//img | //img[contains(@src, "scontent")]')
            )
        )
    except Exception as e:
        print(f"❌ Cannot find HD image element for {index}: {e}")
        return

    hd_url = hd_img.get_attribute("src")
    hd_url = enhance_to_1080p(hd_url)

    # Resize browser window to natural image size
    natural_width = driver.execute_script("return arguments[0].naturalWidth;", hd_img)
    natural_height = driver.execute_script("return arguments[0].naturalHeight;", hd_img)
    driver.set_window_size(natural_width + 100, natural_height + 150)
    print(f"🔲 Browser window resized to image natural size: {natural_width}x{natural_height}")

    filename = os.path.join(save_folder, f"image_{index}.jpg")
    if os.path.exists(filename):
        print(f"⏩ Skipped: image_{index}.jpg (already exists)")
        return

    try:
        img_data = requests.get(hd_url).content
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"✅ Downloaded image_{index}.jpg")
    except Exception as e:
        print(f"❌ Failed to download image {index}: {e}")

# Step 4: Download images
for i, link in enumerate(links):
    download_hd_image(link, i)
    time.sleep(download_delay)

driver.quit()
print(f"\n✅ DONE: All images saved in '{os.path.abspath(save_folder)}'")