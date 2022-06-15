from util import *

username = sys.argv[1] # username
password = sys.argv[2] # password
delay_minutes = int(sys.argv[3]) # delay (m)
img_path = os.getcwd() + "/1.png"

def save_img(src):
    img = requests.get(src)
    with open(img_path, "wb") as f:
        f.write(img.content)

def already_checked_in(d):
    sg_signed = d.find_element_by_xpath("//*[@id='sg_signed']")
    return True if sg_signed.is_displayed() else False
        
@retry(stop_max_attempt_number=5)
def lixianla():
    try:
        driver = get_web_driver()

        # login
        driver.get("https://lixianla.com/user-login.htm")

        driver.find_element_by_xpath("//*[@id='email']").send_keys(username)
        driver.find_element_by_xpath("//*[@id='password']").send_keys(password)

        valid = Ocr_Captcha(driver, "//*[@class='vcode']", img_path)
        print('lixianla: code: ' + valid)
        driver.find_element_by_xpath("//*[@placeholder='图形验证码']").send_keys(valid)

        driver.find_element_by_xpath("//*[@id='submit']").click()
        time.sleep(10)

        if already_checked_in(driver):
            print('lixianla: already checked in')
        elif driver.find_elements_by_xpath("//*[@class='btn btn-primary ft']") != []:
            print('lixianla: start checking in')

            # click check-in button
            driver.find_element_by_xpath("//*[@class='btn btn-primary ft']").click()
            time.sleep(10)

            valid = Ocr_Captcha(driver, "//*[@class='vcode']", img_path)
            print('lixianla: code: ' + valid)
            driver.find_element_by_xpath("//*[@placeholder='验证码']").send_keys(valid)

            driver.find_element_by_xpath("//*[@class='btn btn-block btn-primary axbutton']").click()
            time.sleep(10)

            if already_checked_in(driver):
                print('lixianla: checked in successfully')
            else:
                print('lixianla: error checking in, ocr failed?')
                return False
        else:
            print('lixianla: error logging in, ocr failed?')
            return False
        
        return True
    except:
        raise
    finally:
        driver.quit()

if __name__ == '__main__':
    print('lixianla: delay ' + str(delay_minutes) + ' minutes')
    time.sleep(delay_minutes * 60)
    for i in range(5):
        if (lixianla()): break