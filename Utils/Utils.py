import datetime
import logging
import os
import time


class Utils:

    def get_curDate(self):
        return time.strftime("%Y%m%d", time.localtime())

    def log(self):

        log = logging.getLogger("CAIZQ")          #获取log收集器
        log.setLevel(level= logging.INFO)
        pycharm = logging.StreamHandler()  #输出到控制台
        fmt = "%(asctime)s - [%(funcName)s-->line:%(lineno)d] - %(levelname)s:%(message)s"  #日志打印格式
        pycharm_fmt = logging.Formatter(fmt)  #日志输出对象
        pycharm.setFormatter(pycharm_fmt)
        log.addHandler(pycharm)
        return log

    def saveScreenShotFile(self,fileName):

        filePath = "../log/{}".format(self.get_curDate())

        if not os.path.exists(filePath) :
            os.mkdir(filePath)
        return filePath+"/{}.png".format(fileName)







if __name__=="__main__":
    Utils().get_curDate()