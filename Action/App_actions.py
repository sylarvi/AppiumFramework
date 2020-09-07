import time
from datetime import datetime
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from Util.yaml_handle import Yaml
from Log.logger_handler import Logger
from Config.project_var import screenshot_path

file = '\Config\device_config.yaml'
kw = 'MIX_2'
data = Yaml().get_yaml(file, kw)
# print(data)
logger = Logger(logger='App_actions').getlog()


class Driver:
    def __init__(self):
        self.desired_caps = {'platformName': data['platformName'],
                             'platformVersion': data['platformVersion'],
                             'deviceName': data['deviceName'],
                             'appPackage': data['appPackage'],
                             'appActivity': data['appActivity'],
                             'unicodeKeyboard': data['unicodeKeyboard'],  # 支持中文输入要添加的代码
                             'resetKeyboard': data['resetKeyboard'],
                             'noReset': data['noReset']  # 初始化设备时不清楚用户数据
                             }
        try:
            self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.desired_caps)
            logger.info('初始化设备成功')
        except Exception as e:
            logger.error('设备连接失败：{}'.format(e))

    def find_element(self, type, keyword):
        if type == 'id':  # 根据元素id定位
            element = self.driver.find_element_by_id(keyword)
        elif type == 'content_desc':  # 根据元素icontent-desc字段定位
            element = self.driver.find_element_by_accessibility_id(keyword)
        elif type == 'css_selector':  # 根据元素css选择器定位
            element = self.driver.find_element_by_css_selector(keyword)
        elif type == 'xpath':  # 根据元素xpath表达式定位
            element = self.driver.find_element_by_xpath(keyword)
        elif type == 'class_name':  # 根据元素classname定位
            element = self.driver.find_element_by_class_name(keyword)
        elif type == 'name':  # 根据元素name属性定位
            element = self.driver.find_element_by_name(keyword)
        elif type == 'source_id':
            # print("new UiSelector().resourceId({})".format(keyword))
            element = self.driver.find_element_by_android_uiautomator('new UiSelector().resourceId("{}")'.format(keyword))
        elif type == 'text':
            element = self.driver.find_element_by_android_uiautomator('new UiSelector().text("%s")' % keyword)
        else:
            element = None
        return element

    def click(self, type, keyword):
        """点击元素"""
        try:
            self.find_element(type, keyword).click()
        except Exception as e:
            logger.error('点击元素({})失败：{}'.format(keyword, e))

    def input(self, type, keyword, text):
        """向文本框元素输入内容"""
        try:
            self.find_element(type, keyword).send_keys(text)
        except Exception as e:
            logger.error('输入内容失败：{}'.format(e))

    def clear(self, type, keyword):
        """清除文本框内的内容"""
        try:
            self.find_element(type, keyword).clear()
        except Exception as e:
            logger.error('清除输入框内容失败：{}'.format(e))

    def assert_string_in_pagesource(self, assertString, *args):
        "断言页面源码是否存在某关键字或关键字符串"
        page_source = self.driver.page_source
        try:
            assert assertString in page_source, "{} not found in page source!".format(assertString)
        except AssertionError as e:
            raise AssertionError(e)
        except Exception as e:
            logger.error('判断页面元素失败：{}'.format(e))

    def get_attributes(self, type, keyword, attr_name):
        try:
            text = self.find_element(type, keyword).get_attribute(attr_name)
            return text
        except Exception as e:
            logger.error(e)

    def screencap(self, *args):
        """截取屏幕图片"""
        currTime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")  # 获取当前时间，精确到毫秒
        # 拼接异常图片保存的绝对路径及名称
        picNameAndPath = screenshot_path + "/" + str(currTime) + ".png"
        try:
            "截取屏幕图片，并保存为本地文件"
            self.driver.get_screenshot_as_file(picNameAndPath)
        except Exception as e:
            logger.error('当前屏幕截图失败：{}'.format(e))

    def get_size(self):
        """获取屏幕尺寸"""
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def scroll_down(self):
        screen = self.driver.get_window_size()
        try:
            action = TouchAction(self.driver)
            action.press(x=screen['width'] / 2, y=screen['height'] / 2)
            action.move_to(x=0, y=screen['height'] / 10)
            action.release()
            action.perform()
        except Exception as e:
            logger.error('向下滑动屏幕失败：{}'.format(e))

    def backgroud(self, time):
        """将应用置于后台指定的时间"""
        self.driver.background_app(time)

    def press_key(self, key):
        """发送一个键码的操作"""
        """4"""
        self.driver.press_keycode(29)

    def lock_screen(self):
        """锁屏"""
        self.driver.lock()

    def hide_keyboards(self):
        """收起键盘操作"""
        self.hide_keyboards()

    def tap(self, params):
        self.tap([(params[0][0], params[0][1]), (params[1][0], params[1][1])])

    def sleep(self, sleepSeconds):
        """强制等待"""
        try:
            time.sleep(int(sleepSeconds))
        except Exception as e:
            raise e

    def close_app(self):
        """关闭app"""
        try:
            self.driver.close_app()
        except Exception as e:
            raise e

    def quite(self):
        """关闭webdriver"""
        try:
            self.driver.quit()
        except Exception as e:
            raise e


if __name__ == "__main__":
    info = Yaml().get_yaml('\Page_case\Home_search.yaml', 'case02')
    device = Driver()
    time.sleep(6)
    a = info
    for i in a:
        if a[i]['operate_type'] == 'click':
            device.click(a[i]['find_type'], a[i]['element_info'])
            device.sleep(a[i]['time'])
        elif a[i]['operate_type'] == 'input':
            device.input(a[i]['find_type'], a[i]['element_info'], a[i]['text'])
            device.sleep(a[i]['time'])
        elif a[i]['operate_type'] == 'get_attributes':
            result = device.get_attributes(a[i]['find_type'], a[i]['element_info'], a[i]['text'])
            print(result)
    device.screencap()

