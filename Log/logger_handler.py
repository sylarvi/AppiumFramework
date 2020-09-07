import logging
import time
from Config.project_var import log_path


class Logger:
    def __init__(self, logger):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志保存到指定的文件中
        """
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)

        log_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
        file_path = log_path
        file_name = file_path + log_time + '.log'
        f_handler = logging.FileHandler(file_name, encoding='utf-8')
        f_handler.setLevel(logging.INFO)

        # 创建用于输出到控制台handler
        s_handler = logging.StreamHandler()
        s_handler.setLevel(logging.INFO)

        # 定义handler的输出格式
        output_format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(name)s - %(levelname)s - '
                                          '%(message)s')
        f_handler.setFormatter(output_format)
        s_handler.setFormatter(output_format)

        # 给logger添加handler
        self.logger.addHandler(f_handler)
        self.logger.addHandler(s_handler)

    def getlog(self):
        return self.logger


if __name__ == '__main__':
    logger = Logger(logger='test_log').getlog()
    logger.info('log test: this is a info_log 1')
    logger.info('log test: this is a info_log 2')
    logger.info('log test: this is a info_log 3')
    logger.error('log test: this is a error_log 4')
    logger.error('log test: this is a error_log 5')
    print(log_path)
