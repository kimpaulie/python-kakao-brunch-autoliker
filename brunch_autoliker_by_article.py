from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time, random
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
#chrome_options.add_argument("--headless")

## Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
driver = webdriver.Chrome('C:/Users/Paul/Downloads/chromedriver/chromedriver.exe',
                          options=chrome_options)

print("카카오 브런치 게시물 Auto-Like Bot by Paulie")

# driver.set_window_size(1024, 800)
# driver.set_window_size(1632, 990)
# driver.implicitly_wait(3)


## url에 접근
driver.get('https://brunch.co.kr/auth/kakao?url=https%3A%2F%2Fbrunch.co.kr%2F%2Fsignin%2Ffinish%3Fsignin%3Dtrue%26url%3D%252F')
print("로그인 페이지 접속")

# id, pw 입력할 곳을 찾습니다.
driver.find_element_by_id("id_email_2").send_keys("abcd@gmail.com")
driver.find_element_by_id("id_password_3").send_keys("abcd"+Keys.ENTER)

wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_element_located((By.ID, "dkWrap"))
)
print("로그인 완료")

url = "https://brunch.co.kr/keyword/인생"



driver.get(url)
print("키워드 페이지 오픈")


hit = 0
rndSec = random.randint(4, 7)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while hit < 2 :
    hit = hit +1
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(rndSec)
    print("페이지 %d번 로딩" % hit)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

print("-------총 %d번 페이지 로딩 완료-------" % hit)

def parse(texts):
    soup = BeautifulSoup(texts, "html.parser")
    ul_articlelist = soup.find("ul", {"class":"list_article list_common"})
    lis = ul_articlelist.findAll("li") # [<li></li>,]
    print(lis)

    links = []
    for li in lis:
        brunchLink = "https://brunch.co.kr"
        linkAddr = li.find("a")['href']
        # <a href="123" alt="456">hi my name is ~~</a>

        strong = li.find("strong").text # 제목
        links.append(brunchLink + linkAddr)

    return links

time.sleep(3)
texts = driver.page_source
links = parse(texts)

count = 0
totalcount = 0

for i in links:
    count = count + 1
    totalcount = totalcount + 1
    print(count,i)



print("url 로딩 총 %d 건 완료" % totalcount)
print("---------작업 시작---------")

count = 0
success_count=0
fail_count=0

for url in links:
    try:
        count = count + 1
        driver.get(url)
        time.sleep(rndSec)
        driver.find_element_by_css_selector(".ico_likeit_like:nth-child(1)").click()
        time.sleep(rndSec)
        success_count = success_count + 1
        print(count,"/",totalcount, url, "클릭 성공")

    except Exception as e:
        fail_count = fail_count + 1
        print(count,"/",totalcount, url, "클릭 실패")


print("성공 : 총 %d" % success_count,"/ %d 건" % totalcount)
print("실패 : 총 %d" % fail_count,"/ %d 건" % totalcount)

print("---------작업 종료---------")
print("창을 닫습니다.")

driver.close()


