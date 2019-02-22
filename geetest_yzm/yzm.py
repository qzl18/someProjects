import math

from selenium.webdriver import ActionChains
from selenium import webdriver
import time
import cv2 as cv
import numpy as np
from selenium.webdriver.common.keys import Keys


def func():

    huakuai = driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')

    driver.save_screenshot('quekou.png')
    #找横线长39~40个像素的坐标点得到
    quekouimg = cv.imread('quekou.png', cv.IMREAD_GRAYSCALE)

    # slider = cv.imread('d://untitled.png', cv.IMREAD_GRAYSCALE)
    canny = cv.Canny(quekouimg, 200, 240)
    # cv.imshow('Canny', canny)
    # cv.imshow('slider', slider)
    # cv.waitKey()

    # p =39,40
    # x = []
    # for i,row in canny.iterrows():
    #     for j in canny.iloc[i]:
    #         if canny[i, j] == 0 and canny[i, j + 1]:
    #             x.append(j)
    #         if (canny[i,j] ==0 and canny[i,j+1]==1 and canny[i,j+1:j+42]==1) and\
    #         (canny[i,j] ==0 and canny[i,j+1]==1 and canny[i,j+1:j+42]==1)
    # for col in canny.
    x= np.where(canny!=0)
    y = x[1]
    x = x[0]
    dic = {}
    for i,j in zip(x,y):
        if i not in dic:
            dic[i] = [j]
        else:
            dic[i].append(j)

    def findxy(dic):
        for i,l in dic.items():
            if 100>len(dic[i])>4:
                if set([x for x in range(l[4],l[4]+39)]).issubset(set(l)) and set([x for x in range(l[0],l[0]+50)]).issubset(set(l))==False:
                    return(dic[i])

    list2 = []
    def distance(list1):
        # if list1:
        l = [list1[0]]
        for i in range(1,len(list1)):
            if list1[i]-1 in l:
                l.append(list1[i])
            else:
                list2.append(l)
                print(l)
                distance(list(list1[i+1:]))





    list1 = findxy(dic)
    try:
        list2 = distance(list1)
    except:
        print(list2)
    list3 = []
    for i in list2:
        if 50>len(i)>30:
            list3.append(i)
    distance_ = list3[1][0]-list3[0][0]
    print(distance_)
    return distance_,huakuai

#
#
# #
def get_track(distance):      # distance为传入的总距离
    # 移动轨迹
    T0=0.4
    T1 = 1.5
    # 计算间隔
    t= np.linspace(0.4,2,17)
    # 初速度

    gt=[math.tanh(1.5*(x-T0)/(T1-T0)) for x in t]

    ft =distance*np.array(gt)/math.tanh(1.5)

    track = [0, 0, 0, 0, 0, 0]
    for i in np.diff(ft):
        track.append(i)

    print(track)
    print(sum(track))
    return track
    # return trackdef get_track(distance):      # distance为传入的总距离
    # # 移动轨迹
    # track=[]
    # # 当前位移
    # current=0
    # # 减速阈值
    # mid=distance*4/5
    # # 计算间隔
    # t=0.2
    # # 初速度
    # v=0
    #
    # while current<distance:
    #     if current<mid:
    #         # 加速度为2
    #         a=2
    #     else:
    #         # 加速度为-2
    #         a=-3
    #     v0=v
    #     # 当前速度
    #     v=v0+a*t
    #     # 移动距离
    #     move=v0*t+1/2*a*t*t
    #     # 当前位移
    #     current+=move
    #     # 加入轨迹
    #     track.append(round(move))
    #
    # print(track)
    # return track
def move_to_gap(slider,tracks):     # slider是要移动的滑块,tracks是要传入的移动轨迹
    ActionChains(driver).click_and_hold(slider).perform()
    for x in tracks:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(2)
    ActionChains(driver).release().perform()

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get("http://nwx.duihuanjifen.com/h5/wxPublic/pages/personalCenter.html?timestamp=")
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="name"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="loginNav"]/div[2]/span').click()

    time.sleep(1)
    ph = driver.find_element_by_xpath('//*[@id="mobile"]')
    ph.send_keys('18634406976')
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="getRandom"]').click()

    time.sleep(3)

    while True:
        try:
            distance_,huakuai = func()

        except:
            driver.find_element_by_xpath('/html/body/div[7]/div[2]/div[6]/div/div[2]/div/a[2]').click()
            time.sleep(3)
            if driver.find_element_by_xpath("//div[@class='geetest_panel_error']").get_attribute('style')=="display: block;":
                print('进入')
                driver.find_element_by_xpath("//div[@class='geetest_panel_error_content']").click()
                time.sleep(3)
            # print(driver.find_element_by_xpath("//div[@class='geetest_panel_error']").get_attribute('style'))
            time.sleep(3)
            continue
        else:
            move_to_gap(huakuai, get_track(distance_))
            break