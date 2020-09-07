import os

# 工程绝对路径
project_var = os.path.dirname(os.path.dirname(__file__))

# 设备信息配置文件路径
devices_config_path = project_var + "/Config/"

# 日志文件路径
log_path = project_var + "/Log/logs/"

# 截图文件路径
screenshot_path = project_var + '/Screenshots/'

# excel数据文件路径
excel_path = os.path.join(project_var + '/Excel_case/testcase.xlsx')
