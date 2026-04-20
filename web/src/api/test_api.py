import pytest
from api.request_utils import RequestUtil
from api.data_utils import DataUtil

# 假设测试数据存储在一个Excel文件中，例如 test_data.xlsx
data_util = DataUtil('path_to_your_test_data.xlsx')
test_data = data_util.read_excel()

@pytest.mark.parametrize("data", test_data)
def test_api(data):
    request_util = RequestUtil()
    response = request_util.send_request(method=data['method'], url=data['url'], json=data.get('body'))
    assert response.status_code == 200
    # 可以根据需要添加更多的断言
    assert response.json()['status'] == 'success'