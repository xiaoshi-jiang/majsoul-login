import sys
import time
from datetime import datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    start_time = time.time()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    success = False
    driver = None
    
    try:
        acccounts = int(len(sys.argv[1:])/2)
        print(f'Config {acccounts} accounts')
        for i in range(acccounts):
            email = sys.argv[1+i]
            passwd = sys.argv[1+i+acccounts]
            print('----------------------------')

            #1.open browser
            options = webdriver.ChromeOptions()
            options.add_argument("--headless=new")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1280,800")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            driver = webdriver.Chrome(options=options)
            driver.get("https://game.maj-soul.net/1/")
            print(f'Account {i+1} loading game...')

            screen = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.TAG_NAME, "canvas"))
            )
            sleep(60)

            #2.input email
            ActionChains(driver)\
                .move_to_element_with_offset(screen, 350, -135)\
                .click()\
                .perform()
            sleep(1)
            ActionChains(driver)\
                .send_keys(email)\
                .perform()
            sleep(1)
            print('Input email successfully')

            #3.input password
            ActionChains(driver)\
                .move_to_element_with_offset(screen, 350, -50)\
                .click()\
                .perform()
            sleep(1)
            ActionChains(driver)\
                .send_keys(passwd)\
                .perform()
            sleep(1)
            print('Input password successfully')

            #4.login
            ActionChains(driver)\
                .move_to_element_with_offset(screen, 350, 60)\
                .click()\
                .perform()
            print(f'Account {i+1} entering game...')
            sleep(40)  # loading...

            #5.click screen to enter lobby / claim reward
            ActionChains(driver)\
                .move_to_element_with_offset(screen, 200, 60)\
                .click()\
                .perform()
            sleep(20)
            print(f'Account {i+1} login success')
            driver.quit()
            driver = None
        
        success = True
        
    except Exception as e:
        print(f'Login failed: {str(e)}')
        if driver is not None:
            driver.quit()
        success = False
    
    finally:
        # 记录执行日志
        end_time = time.time()
        execution_time = end_time - start_time
        
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{current_time}-{'Success' if success else 'Failed'}-{execution_time:.2f}s\n")
        
        print(f"Execution completed. Status: {'Success' if success else 'Failed'}, Time: {execution_time:.2f}s")


if __name__ == "__main__":
    main()
