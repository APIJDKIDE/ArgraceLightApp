import logging
import time

import pytest
import yaml
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

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
        self.driver.implicitly_wait(5)
        self.utils = Utils()
        self.curDate = self.utils.get_curDate()

    @pytest.mark.skip
    def test_login(self):
        try:
            self.driver.find_element_by_class_name("android.widget.ImageButton").click()  #关闭一键登录页
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
            #self.driver.get_screenshot_as_file(self.utils.saveScreenShotFile("test_login"))

            print(ex)
            assert False


    #新建房间
    @pytest.mark.skip
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

    #创建设备卡片 -不同的品类
    # @pytest.mark.parametrize(
    #     'deviceType, deviceName',[
    #         ("冷暖白光灯","CW"),
    #         ("5路彩灯","RGBCW"),
    #         ("5路彩灯(支持音乐律动)","RGBCWRhythm"),
    #         ("4路彩灯(支持音乐律动)","RGBCWRhythm")
    #     ])
    @pytest.mark.parametrize('deviceCategory,deviceType, deviceName', yaml.safe_load(open("./config.yaml","rb")))
    def test_create_devices(self,deviceCategory,deviceType,deviceName):

        #先选择第一个房间
        # 先选择第一个房间
        room_element = self.driver.find_element("xpath",
                                                "//*[@content-desc = '总控']/../androidx.appcompat.app.ActionBar.Tab[2]/android.widget.TextView")
        room_element.click()
        self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/iv_add").click()
        self.driver.find_element("xpath","//*[@text = '{}']".format(deviceCategory)).click()
        title = self.driver.find_element("xpath","//*[@text = '{}']".format(deviceType)).location  #获取设备类型名称的坐标
        x = title["x"]
        y = title["y"]-50   #上移50个像素，才能选中设备icon
        self.driver.tap([(x,y)])

        self.driver.find_element("xpath","//*[@text = '确定']").click()
        self.driver.find_element("xpath","//*[contains(@text,'请输入设备名称')]").send_keys(deviceName+'_{}'.format(self.curDate))

        ''' 估计是识别不到弹框，所以"选择设备所属房间"元素没定位到，先忽略
        belongRoom_locators = "//*[@text = "+"\'所属房间\'"+']'
        self.driver.find_element("xpath", belongRoom_locators).click()
        self.driver.find_element_by_android_uiautomator('new UiSelector().textContains(\"自动化房间\")')
        self.driver.find_element("xpath","//*[@text = '自动化房间20220529']")
        room_locators = "//*[contains(@text , " + "\'自动化房间\')" + ']'
        self.driver.find_element("xpath", room_locators).click()   #还没想明白为什么这里定位不到元素。。。
        '''
        self.driver.find_elements("xpath","//*[@text = '确定']")[1].click()
        self.driver.save_screenshot(self.utils.saveScreenShotFile(deviceName+'_{}'.format(self.curDate)))

        try:
            self.driver.find_element("xpath","//*[contains(@text,'成功')]")
            assert True
        except Exception as ex:
            assert False

    def test_controll_devices(self):
        # 先选择第一个房间
        room_element = self.driver.find_element("xpath",
                                                "//*[@content-desc = '总控']/../androidx.appcompat.app.ActionBar.Tab[2]/android.widget.TextView")
        room_element.click()
        device_elements = self.driver.find_elements_by_class_name("android.view.ViewGroup")

        device_elements = self.driver.find_elements("id","ai.argrace.remotecontrol.sit:id/rv_home_device")

        i = 0
        for device_element in device_elements:
            if i >= 4 :
                break
            device_element.click()
            brightness_ele = self.driver.find_element("xpath","//*[@content-desc = 'ReactColorPicker_Slider']")  #亮度条
            x_end = brightness_ele.location['x']
            y_end = brightness_ele.location['y']
            x_start =x_end + brightness_ele.size["width"]
            y_start =y_end + brightness_ele.size["height"]
            TouchAction(self.driver).press(x = x_start,y = y_start).wait(200).move_to(x = x_end, y = y_end).release().perform()  #滑动亮度条

            for text in ['关','开','配对','解除配对'] :
                self.driver.find_element("xpath",f"//*[@text = '{text}']").click()

            self.driver.find_element("xpath","//*[@content-desc='TopBar_Btn_Back']").click()  #返回房间的设备列表
            i+=1







def teardown(self):
        print("this is the teardown function")
        #self.driver.quit()


if __name__=="__main__":

    pytest.main(['-s','./'])