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

print("\n☆☆☆카카오 브런치 게시물 Auto-Like Bot_by author upgrade version by Paulie☆☆☆\n")

# driver.set_window_size(1024, 800)
# driver.set_window_size(1632, 990)
# driver.implicitly_wait(3)

#brunchkeyword = input('※ 원하시는 키워드를 입력하세요 :')
#authorloadnum = input('※ 불러올 브런치 작가 수를 입력하세요 :')
#articleloadnum = input('※ 공감을 표시할 각 작가의 글 개수를 입력하세요 :')

brunchkeyword = '소설'
authorloadnum = 3
articleloadnum = 3


print('☞ 키워드 : ' + brunchkeyword + ' / 브런치 작가 수 :',authorloadnum, '/ 각 글 개수 :', articleloadnum)

## Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
driver = webdriver.Chrome('C:/Users/Paul/Downloads/chromedriver/chromedriver.exe',
                          options=chrome_options)

## url에 접근
driver.get('https://brunch.co.kr/auth/kakao?url=https%3A%2F%2Fbrunch.co.kr%2F%2Fsignin%2Ffinish%3Fsignin%3Dtrue%26url%3D%252F')
print("○ 로그인 페이지 접속")

brunch_id = ("abcd@gmail.com")
brunch_pw = ("abcd")


# id, pw 입력할 곳을 찾습니다.
driver.find_element_by_id("id_email_2").send_keys(brunch_id)
driver.find_element_by_id("id_password_3").send_keys(brunch_pw + Keys.ENTER)

wait = WebDriverWait(driver, 10)
wait.until(
    EC.presence_of_element_located((By.ID, "dkWrap"))
)
print("● 로그인 완료")

#url = "https://brunch.co.kr/keyword/건강"
url = "https://brunch.co.kr/keyword/" + brunchkeyword

driver.get(url)
print("\n◎ 키워드 페이지를 오픈하여 작가 url을 로딩합니다.")
rndSec = random.randint(3, 5)
def parse(texts):
    soup = BeautifulSoup(texts, "html.parser")
    ul_articlelist = soup.find("ul", {"class":"list_article list_common"})
    lis = ul_articlelist.findAll("li") # [<li></li>,]

    links = []
    for li in lis:
        brunchLink = "https://brunch.co.kr"
        linkAddr = li.find("a")['href']
        linkAddr = "/"+ linkAddr.split('/')[1]+"#articles"
        # <a href="123" alt="456">hi my name is ~~</a>

        strong = li.find("strong").text # 제목
        links.append(brunchLink + linkAddr)

    return links
time.sleep(3)

count = 0
totalcount = 0

texts = driver.page_source
links = parse(texts)
links_n = len(links)

time.sleep(2)

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
hit = 0

if links_n < authorloadnum :
    print("  ◇ 게시물 수가 부족하여 페이지를 아래로 추가 스크롤 합니다.")

while links_n < authorloadnum :
    hit = hit +1
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(2)


    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

    texts = driver.page_source
    links = parse(texts)
    links_n = len(links)
    perc = (links_n / authorloadnum * 100)
    if perc > 100:
        perc = 100

    print("  ◇ 총 %d 번 스크롤" % hit, "/ 현재 %d%% 완료" % perc)

print("♨ 로딩이 완료되었습니다 ♨\n")
time.sleep(2)

links_limit = links[0:authorloadnum]  # 로딩하는 url 갯수 제한

for i in links_limit:
    count = count + 1
    print(count , i)

print("----------작가 URL 로딩 총 %d 건 완료----------" % count,"\n")


print("■■■■■■■ 개별 작가 로딩 시작 ■■■■■■■■")

author_count = 0
success_count=0
fail_count=0
rndSec = random.randint(4, 7)

tacount = 0
tatotalcount = 0

tsuccess_count=0
tfail_count=0

for url in links_limit:
    author_count = author_count + 1
    print("\n----------- %d 번째 작가 로딩 시작 -----------" % author_count)
    driver.get(url)
    time.sleep(3)
    author_texts = driver.page_source
    author_soup = BeautifulSoup(author_texts, "html.parser")
    author_articlelist = author_soup.find("ul", {"class": "list_article list_post1 #post_list"})
    cond = "list_post1"
    thumbnail_type = str(author_articlelist)[24:34]
    if cond == thumbnail_type:
        print("썸네일 타입 : Small")
    else:
        print("썸네일 타입 : Big")

    author_lis = author_soup.select('.link_post')
    author_links = []

    for author_li in author_lis:
        brunchLink = "https://brunch.co.kr"
        if 'href' in author_li.attrs:
            author_linkAddr = author_li.attrs['href']
            author_links.append(brunchLink + author_linkAddr)

    author_links = author_links[0:articleloadnum]

    acount = 0
    atotalcount = 0

    for i in author_links:
        acount = acount + 1
        atotalcount = atotalcount + 1
        print(acount, i)


    print("★ %d 번째 작가 포스팅 url 로딩" % author_count,"총 %d 건 완료 및 작업 시작 ★" % atotalcount)

    acount = 0



    for url in author_links:
        try:
            acount = acount + 1
            tacount = tacount + 1
            tatotalcount = tatotalcount + 1
            driver.get(url)
            time.sleep(rndSec)
            driver.find_element_by_css_selector(".ico_likeit_like:nth-child(1)").click()
            success_count = success_count + 1
            tsuccess_count = tsuccess_count + 1
            print("(%d) %d/%d %s 클릭 성공" % (tatotalcount,acount,atotalcount,url))
            time.sleep(rndSec)

        except Exception as e:
            fail_count = fail_count + 1
            tfail_count = tfail_count + 1
            print("(%d) %d/%d %s 클릭 실패" % (tatotalcount,acount,atotalcount,url))
            time.sleep(rndSec)

    print("성공 : 총 %d" % success_count + "/%d 건" % atotalcount)
    print("실패 : 총 %d" % fail_count + "/%d 건" % atotalcount)
    success_count = 0
    fail_count = 0

print("---------작업 종료---------")
ttt = tsuccess_count + tfail_count
print("총 성공 : 총 %d" % tsuccess_count, "/ %d 건" % ttt)
print("총 실패 : 총 %d" % tfail_count, "/ %d 건" % ttt)

print("창을 닫습니다.")

driver.close()