# -*- coding: utf-8 -*-
"""
author:码同学 极光
date:2023-02-12
desc: 
sample: 
"""

#http://121.11.97.201:9088/pinter
#支持接口的  检查点
from dvadmin.utils.RequestUtil import RequestUtil

def test_check():
    api = RequestUtil()
    #jsonpath 类型检查点
    api.send_request("get", "http://121.11.97.201:9088/pinter/com/getSku?id=1",
                     verification='$..message=success', case_desc='json检查点测试', )
    # print(f"当前接口测试结果{api.get_result()}")
    #支持正则检查点
    api.send_request("get", "http://www.baidu.com",
                     verification='<title>(.+?)</title>=百度一下，你就知道', case_desc='正则检查点测试', )

    print(f"当前接口测试结果{api.get_result()}")


#两个接口 关联  提取 替换 正则
def test_correlation():
    api = RequestUtil()
    api.send_request("get", "http://121.11.97.201:9088/pinter/com/getSku?id=1",
                     verification='$.code=0', case_desc="json提取",
                     extract="skuId=$.data.skuId;msg=$.message")
    print(f"当前接口测试结果{api.get_result()},  全局变量{api.get_variable()}")

    api.send_request("get", "http://www.baidu.com",
                     case_desc="html数据提取",
                     extract="title=<title>(.+?)</title>")
    print(f"全局变量{api.get_variable()}")
    #
    data = {"param": '{"skuId":${skuId}, "num": 10, "desc":${title}'}
    headers={"id":'${skuId}'}
    api.send_request("post", "http://121.11.97.201:9088/pinter/com/login",
                     verification='$.code=1',
                     data=data,case_desc="参数替换",headers=headers)
    print(f"当前接口测试结果{api.get_result()},  全局变量{api.get_variable()}")


def testurl():
    url = "http://${host}:${port}/pinter/com/getSku?id=1"
    api = RequestUtil()
    api.var_pool_data={"host":'127.0.0.1','port':"9088"}
    api.send_request('get',url)


if __name__ == '__main__':
    #检查点测试
    #test_check()
    #关联测试
    #test_correlation()
    testurl()
