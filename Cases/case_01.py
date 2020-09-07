import ddt
import unittest
from datetime import datetime
from Util.data_organize import test_data
from Log.logger_handler import Logger
from Util.yaml_handle import Yaml
from Action.App_actions import Driver
from Util.Excel_parse import HandleExcel

logger = Logger(logger='case_01').getlog()
data = test_data()
# print(data)
currTime = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


# yaml_data = Yaml().get_yaml('\Page_case\Home_search.yaml', data[0][0])
# print(yaml_data)
# @ddt.ddt
# class PageTest(unittest.TestCase):
#     @ddt.data(*data)
#     def test_case01(self, data1):
#         print(data1)


@ddt.ddt
class TestPage(unittest.TestCase):
    def setUp(self):
        print('start')

    @ddt.data(*data)
    def test_case01(self, data1):
        driver = Driver()
        driver.sleep(7)
        logger.info('开始执行测试用例:{}'.format(data1[0]))
        HandleExcel().write_data(HandleExcel().get_case_number(data1[0]), 5, currTime)
        params = Yaml().get_yaml('\Page_case\Home_search.yaml', data1[0])
        for item in params:
            logger.info('执行{}_步骤:{}'.format(data1[0], item))
            if params[item]['operate_type'] == 'click':
                driver.click(params[item]['find_type'], params[item]['element_info'])
                driver.sleep(params[item]['time'])
            elif params[item]['operate_type'] == 'input':
                driver.input(params[item]['find_type'], params[item]['element_info'], params[item]['text'])
                driver.sleep(params[item]['time'])
            elif params[item]['operate_type'] == 'get_attributes':
                text = driver.get_attributes(params[item]['find_type'], params[item]['element_info'],
                                             params[item]['text'])
                HandleExcel().write_data(HandleExcel().get_case_number(data1[0]), 8, str(text))
                try:
                    self.assertEqual(data1[2], text)
                    HandleExcel().write_data(HandleExcel().get_case_number(data1[0]), 7, 'Pass')
                except Exception as e:
                    HandleExcel().write_data(HandleExcel().get_case_number(data1[0]), 7, 'Failed')
                    logger.error(e)
                self.assertEqual(data1[2], text)
        driver.screencap()
        driver.close_app()
        driver.quite()

    def tearDown(self) -> None:
        print('end')


if __name__ == '__main__':
    unittest.main()
