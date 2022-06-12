from util import *

username = sys.argv[1] # username
password = sys.argv[2] # password
delay_minutes = sys.argv[3] # delay (m)
img_path = os.getcwd() + "/1.png"

def save_img(src):
    img = requests.get(src)
    with open(img_path, "wb") as f:
        f.write(img.content)

def already_checked_in(d):
    status = d.find_elements_by_xpath("//*[@class='icon-calendar-check-o']");
    return True if status != [] and status[0].text.find('已签到') else False
        
@retry(stop_max_attempt_number=5)
def lixianla():
    time.sleep(delay_minutes * 60)
    try:
        driver = get_web_driver()

        # login
        driver.get("https://lixianla.com/user-login.htm")

        driver.find_element_by_xpath("//*[@id='email']").send_keys(username)
        driver.find_element_by_xpath("//*[@id='password']").send_keys(password)

        valid = Ocr_Captcha(driver, "//*[@class='vcode']", img_path)
        driver.find_element_by_xpath("//*[@placeholder='图形验证码']").send_keys(valid)

        driver.find_element_by_xpath("//*[@id='submit']").click()
        time.sleep(5)

        if already_checked_in(driver):
            print('lixianla: already checked in')
        elif driver.find_elements_by_xpath("//*[@class='btn btn-primary ft']") != []:
            print('lixianla: start checking in')

            # click check-in button
            driver.find_element_by_xpath("//*[@class='btn btn-primary ft']").click()
            time.sleep(5)

            valid = Ocr_Captcha(driver, "//*[@class='vcode']", img_path)
            driver.find_element_by_xpath("//*[@placeholder='验证码']").send_keys(valid)

            driver.find_element_by_xpath("//*[@class='btn btn-block btn-primary axbutton']").click()
            time.sleep(5)

            if already_checked_in(driver):
                print('lixianla: checked in successfully')
            else:
                print('lixianla: error checking in')
    except:
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    lixianla()