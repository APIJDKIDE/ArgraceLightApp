import time

import pytest
from appium import webdriver


class Test_case:

    def setup(self):
        desired_caps = {
            "deviceName":"EJL4C17106004977",
            "platformName":"Android",
            "platformVersion":"6",
            "appPackage": "ai.argrace.remotecontrol.sit",
            "appActivity": "ai.argrace.remotecontrol.main.Akeeta_SplashActivity",
            "noReset": True,
            "dontStopAppOnReset": True
            #"UiAutomator":"UiAutomator2"

        }

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub",desired_capabilities = desired_caps)
        self.driver.implicitly_wait(10)


    def test_login_fail(self):

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

        self.driver.find_element("id","ai.argrace.remotecontrol.sit:id/btnLogin").click()  #登录

        time.sleep(10)


    def teardown(self):
        pass


if __name__=="__main__":

    pytest.main()