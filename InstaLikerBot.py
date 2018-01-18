import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

class InstaLikerBot():
    browser = None
    insta_auth = None

    target_insta_id = None
    target_user_num_posts = None

    def __init__(self, insta_auth, target_insta_id):
        self.insta_auth = insta_auth
        self.target_insta_id = target_insta_id

    def open_browser(self):
        self.browser = webdriver.Chrome()

    def login_and_redirect(self):
        try:
            # login with credentials
            self.browser.get("https://www.instagram.com/accounts/login/")
            WebDriverWait(self.browser, 14).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(self.insta_auth['username'])
            WebDriverWait(self.browser, 14).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(self.insta_auth['password'])
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/span/button'))).click()

            # wait for login successful then redirect to target user profile
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/explore/']")))
            print("logged in successfully!")
            self.browser.get(self.target_insta_id)
        except TimeoutException:
            print("Insta authentication failed!")
            print('quitting browser.')
            self.browser.quit()
            exit()

    def init_num_posts(self):
        post_span = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/header/section/ul/li[1]/span/span')))
        self.num_posts = int(post_span.get_attribute("innerHTML"))

    def like_images_till(self, num):

        print("Starting liking process...")

        # second image
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/div/div[1]/div[1]/div[2]/a/div/div[2]'))).click()

        for i in range(num - 1):
            heart_icon = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/article/div[2]/section[1]/a[1]/span')))
            heart_icon_state = heart_icon.get_attribute("class").split(" ")[1]

            if heart_icon_state == "coreSpriteHeartOpen":
                print("Image " + str(i + 2) + " liked!")
                WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[2]/div/article/div[2]/section[1]/a[1]'))).click()
            else:
                print("Image " + str(i + 2) + " already liked!")

            # next arrow click
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/div[1]/div/div/a[2]'))).click()
            time.sleep(0.9)

    def Run(self):
        print("opening browser...")
        self.open_browser()

        self.login_and_redirect()
        self.init_num_posts()

        print(str(self.num_posts) + " posts found!")

        self.like_images_till(self.num_posts)

        print("All images liked for profile " + self.target_insta_id + " liked.")