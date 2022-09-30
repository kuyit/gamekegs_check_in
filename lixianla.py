from util import *
from selenium.webdriver.common.by import By

username = sys.argv[1] # username
password = sys.argv[2] # password
https_proxy = sys.argv[3] if len(sys.argv) > 3 else ""
img_path = os.getcwd() + "/1.png"

def save_img(src):
    img = requests.get(src)
    with open(img_path, "wb") as f:
        f.write(img.content)

def already_checked_in(d, id):
    sg_signed = d.find_element(By.XPATH, "//*[@id='" + id + "']")
    return True if sg_signed.is_displayed() else False

def lixianla():
    try:
        driver = get_web_driver(proxy = {'https': https_proxy} if https_proxy else {})

        # login
        driver.get("https://lixianla.com/user-login.htm")

        driver.find_element(By.XPATH, "//*[@id='email']").send_keys(username)
        driver.find_element(By.XPATH, "//*[@id='password']").send_keys(password)

        valid = Ocr_Captcha(driver, "//*[@class='vcode']", img_path)
        print('lixianla: code: ' + valid)
        driver.find_element(By.XPATH, "//*[@placeholder='图形验证码']").send_keys(valid)

        driver.find_element(By.XPATH, "//*[@id='submit']").click()
        time.sleep(10)

        if already_checked_in(driver, "sg_signed"):
            print('lixianla: already checked in')
        elif driver.find_elements(By.XPATH, "//*[@class='btn btn-primary ft']") != []:
            print('lixianla: start checking in')

            # click check-in button
            driver.find_element(By.XPATH, "//*[@class='btn btn-primary ft']").click()
            time.sleep(10)

            valid = Ocr_Captcha(driver, "//*[@class='vcode']", img_path)
            print('lixianla: code: ' + valid)
            driver.find_element(By.XPATH, "//*[@placeholder='验证码']").send_keys(valid)

            driver.find_element(By.XPATH, "//*[@class='btn btn-block btn-primary axbutton']").click()
            time.sleep(10)

            if already_checked_in(driver, "sign"):
                print('lixianla: checked in successfully')
            else:
                print('lixianla: error checking in, ocr failed?')
                return False
        else:
            print('lixianla: error logging in, ocr failed?')
            return False

        return True
    except:
        return False
    finally:
        driver.quit()

if __name__ == '__main__':
    for i in range(10):
        if (lixianla()): break