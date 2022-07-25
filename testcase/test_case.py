import logging
import time

import pytest
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException

from Utils.Utils import Utils

class Test_case:
    def setup(self):
        desired_caps = {
            "deviceName":"CUYDU19703017110",  #EJL4C17106004977
            "platformName":"Android",
            "platformVersion":"10",
            "appPackage": "ai.argrace.remotecontrol.sit",
            "appActivity": "ai.argrace.remotecontrol.main.Akeeta_SplashActivity",
            "noReset": True,
            #"dontStopAppOnReset": True,
            "fullReset":False,
            "unicodeKeyboard":True,
            "resetKeyboard":True,
            #"automationName": "UiAutomator2"
        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",desired_capabilities = desired_caps)
        self.driver.implicitly_wait(10)
        self.utils = Utils()

    #@pytest.mark.skip
    def test_login(self):
        try:
            #self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/tv_common_define").click() #隐私政策与服务协议
            self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/cetUserName").send_keys("18898446160")
            self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/petPassword").send_keys("ld12121212")
            # self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/ctv_service_privacy").click()

            window_rect = self.driver.get_window_rect()
            window_height = window_rect['height']
            window_width = window_rect['width']
            x = int(window_width * 0.40)
            y = int(window_height * 0.65)
            self.driver.tap([(x,y)]) #勾选同意隐私政策与服务协议。不得不通过坐标点击
            self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/btnLogin").click()  #点击登录

            self.driver.find_element("xpath", '//*[@content-desc="总控"]/android.widget.TextView')
            assert True
        except Exception as ex:
            #self.driver.get_screenshot_as_file(self.utils.saveScreenShotFile("test_login"))
            self.driver.get_screenshot_as_file(self.utils.saveScreenShotFile("test_login"))

            print(ex)
            assert False


    #新建房间
    #@pytest.mark.skip
    def test_createRooms(self):
        self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/iv_more_room").click()
        create_Room_Button_element = self.driver.find_element("xpath","//*[@text='创建房间']")
        create_Room_Button_element.click()
        self.driver.find_element("xpath","//*[contains(@text,'请输入房间名称')]").send_keys("自动化房间{}".format(self.utils.get_curDate()) )
        self.driver.find_element("xpath","//*[@text='确定']").click()
        try:
            self.driver.find_element("xpath","//*[contains(@text,'成功')]")
            assert True
        except NoSuchElementException:
            self.driver.get_screenshot_as_file(self.utils.saveScreenShotFile("test_createRooms"))
            assert False

    #删除房间
    @pytest.mark.skip
    def test_deleteRooms(self):
        self.driver.find_element("id", "ai.argrace.remotecontrol.sit:id/iv_more_room").click()
        roomName = "自动化房间{}".format(self.utils.get_curDate())

        self.driver.find_element("xpath","//*[@text = {}]".format(roomName)).click()
        self.driver.find_element("xpath","//*[@text = '删除房间']").click()

        try:
            self.driver.find_element("xpath", "//*[contains(@text,'成功')]")
            assert True
        except NoSuchElementException:
            #self.driver.get_screenshot_as_file(self.utils.saveScreenShotFile("test_deleteRooms"))
            self.driver.get_screenshot_as_file("test_deleteRooms")
            assert False

    #创建设备卡片 -"灯泡"品类
    @pytest.mark.parametrize(
        'deviceType, deviceName',[
            ("冷暖白光灯","CW"),
            ("5路彩灯","RGBCW"),
            ("5路彩灯(支持音乐律动)","RGBCWRhythm"),
            ("4路彩灯(支持音乐律动)","RGBCWRhythm")
        ])
    def test_create_Light_Blub(self,deviceType,deviceName):

        #先选择第一个房间
        room_ele = self.driver.find_element("xpath","//*[@content-desc = '总控']/../androidx.appcompat.app.ActionBar.Tab[2]/android.widget.TextView")

        room_ele.click()
        self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/iv_add").click()
        self.driver.find_element("xpath","//*[@text = '灯泡']").click()
        title = self.driver.find_element("xpath","//*[@text = '{}']".format(deviceType)).location  #获取设备类型名称的坐标
        x = title["x"]
        y = title["y"]-50   #上移50个像素，才能选中设备icon
        self.driver.tap([(x,y)])

        self.driver.find_element("xpath","//*[@text = '确定']").click()
        self.driver.find_element("xpath","//*[contains(@text,'请输入设备名称')]").send_keys(deviceName+'_{}'.format(self.utils.get_curDate()))

        ''' 估计是识别不到弹框，所以"选择设备所属房间"元素没定位到，先忽略
        belongRoom_locators = "//*[@text = "+"\'所属房间\'"+']'
        self.driver.find_element("xpath", belongRoom_locators).click()
        self.driver.find_element_by_android_uiautomator('new UiSelector().textContains(\"自动化房间\")')
        self.driver.find_element("xpath","//*[@text = '自动化房间20220529']")
        room_locators = "//*[contains(@text , " + "\'自动化房间\')" + ']'
        self.driver.find_element("xpath", room_locators).click()   #还没想明白为什么这里定位不到元素。。。
        '''
        self.driver.find_elements("xpath","//*[@text = '确定']")[1].click()

        try:
            self.driver.find_element("xpath","//*[contains(@text,'成功')]")
            assert True
        except Exception as ex:
            print("ex内容："+ex)
            assert False

    @pytest.mark.parametrize(
        'deviceType, deviceName',[
            ("单色风扇灯","Fan"),
            ("双色风扇灯","Fan_CW")
        ])
    def test_create_FanLight(self,deviceType,deviceName):

        #先选择第一个房间
        room_ele = self.driver.find_element("xpath","//*[@content-desc = '总控']/../androidx.appcompat.app.ActionBar.Tab[2]/android.widget.TextView")

        room_ele.click()
        self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/iv_add").click()
        self.driver.find_element("xpath","//*[@text = '风扇灯']").click()
        title = self.driver.find_element("xpath","//*[@text = '{}']".format(deviceType)).location  #获取设备类型名称的坐标
        x = title["x"]
        y = title["y"]-50   #上移50个像素，才能选中设备icon
        self.driver.tap([(x,y)])

        self.driver.find_element("xpath","//*[@text = '确定']").click()
        self.driver.find_element("xpath","//*[contains(@text,'请输入设备名称')]").send_keys(deviceName+'_{}'.format(self.utils.get_curDate()))

        ''' 估计是识别不到弹框，所以"选择设备所属房间"元素没定位到，先忽略
        belongRoom_locators = "//*[@text = "+"\'所属房间\'"+']'
        self.driver.find_element("xpath", belongRoom_locators).click()
        self.driver.find_element_by_android_uiautomator('new UiSelector().textContains(\"自动化房间\")')
        self.driver.find_element("xpath","//*[@text = '自动化房间20220529']")
        room_locators = "//*[contains(@text , " + "\'自动化房间\')" + ']'
        self.driver.find_element("xpath", room_locators).click()   #还没想明白为什么这里定位不到元素。。。
        '''
        self.driver.find_elements("xpath","//*[@text = '确定']")[1].click()

        try:
            self.driver.find_element("xpath","//*[contains(@text,'成功')]")
            assert True
        except Exception as ex:
            print(ex)
            assert False


    def teardown(self):
        print("this is the teardown function")
        #self.driver.quit()


if __name__=="__main__":

    pytest.main(['-s','./'])