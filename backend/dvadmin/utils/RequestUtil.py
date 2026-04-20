# -*- coding: utf-8 -*-
"""
author:码同学 极光
date:2023-02-11
desc: 
sample: 
"""
import json
import logging
import re
import time

import jsonpath as jsonpath
import requests


import logging

#get post deletd put
from dvadmin.utils.assertUtils import assert_equals


class RequestUtil(requests.Session):
    def __init__(self):
        super().__init__()
        self.var_pool_data = {}  # 定义变量池
        self.result = {}  # 返回结果
        self.retry_num = 0  # 定义初始次数
        # logging.basicConfig(level=logging.INFO)

    def send_request(self, method, url, case_desc=None, verification=None, extract=None,
                     **kwargs):
        self.result = {"code":1}  #默认成功
        before_time = time.time()
        #所有参数 头部参数 body json
        for k, v in kwargs.items():
            #参数化替换规则
            kwargs[k] = self.replace_template_str(v)
            try:
                kwargs[k] = json.loads(v)
            except:
                pass

        url = self.replace_template_str(url)
        logging.info('*** requests front ***'.center(80, "-"))
        logging.info(f"case desc：{case_desc}")
        logging.info(f"数据提取规则： {extract}")
        logging.info(f"Api 断言表达式： {verification}")
        logging.info(f'requests.method : {method}')
        logging.info(f'requests.url : {url}')
        for k, v in kwargs.items():
            logging.info(f'requests.data : {k}：{v}')

        print(f'request :{method} {url}：{kwargs}')
        try:
            response = super().request(method, url, **kwargs)
            response.encoding = 'utf-8'
        except Exception as e:
            self.result['response'] = f'请求失败 失败原因{e}'
            self.result['code'] = 0
            self.result['took_time']=0
            return

            # 中文问题支持
            #response.encoding = 'utf-8'
        print(response)
        after_time = time.time()
        if response.status_code == 200:
            self.result['took_time'] = round((after_time - before_time) * 1000)
            logging.info(f"花费时间: {self.result['took_time']}ms\n")
        else:
            if self.retry_num > 2:
                self.retry_num = 0
                logging.info("接口请求失败，重试完毕！")
                return response
            logging.info(f"接口请求失败，响应code为 {response.status_code}, 进行第 {self.retry_num + 1} 次重试")
            time.sleep(1)
            self.retry_num += 1
            self.send_request(method, url, **kwargs)

        if response.status_code == 500 or response.status_code == 502:
            self.result['response'] = '后台服务器有错误，请联系开发'
            self.result['code']=0
            return
        if response.status_code == 404:
            self.result['response'] = f'请求地址有问题 请检查请求的url:{url}'
            self.result['code'] = 0
            return
        if response.status_code == 405:
            self.result['response'] = '请检查请求信息中参数'
            self.result['code'] = 0
            return

        logging.info('*** response behind ***'.center(80, "-"))
        logging.info(f'response.status_code : {response.status_code}')
        logging.info(f'response.headers : {response.headers}')
        logging.info(f'response.text : {response.text}')
        self.result['response'] = response.text
        #检查点
        if verification:
            if verification.endswith(";"):
                verification = verification.split(";")[0]
            for ver in verification.split(";"):
                expr = ver.split("=")[0]
                # 判断Jsonpath还是正则断言
                if expr.startswith("$."):
                    actual = jsonpath.jsonpath(response.json(), expr)
                    if not actual:
                        logging.error("该jsonpath未匹配到值,请确认接口响应和jsonpath正确性1")
                    actual = actual[0]
                else:
                    actual = re.findall(expr, response.text)[0]
                expect = ver.split("=")[1]
                try:
                    assert_equals(str(actual), expect)
                    self.result['check_result'] = '检查成功'
                except:
                    self.result['check_result'] = '检查失败'
        else:
            self.result['check_result'] = '没有设置检查点'

        #关联 数据提取
        if extract:
            for item in extract.split(";"):
                kvs = item.split("=")
                key = kvs[0]  # 获取关键字
                value = kvs[1]  # 获取正则表达式
                if value.startswith("$."):
                    self.save_variable(response.json(), key, jsonpath_expression=value)  # 进行JSONPATH提取并保存
                else:
                    self.save_variable(response.text, key, regular_expression=value)  # 进行正则提取并保存

        logging.info("*** requests end ***".center(80, "-"))
        return response

    def replace_template_str(self, target):
        target = str(target)
        # 正则匹配所有{{key}}，并做处理
        #${base_url}
        EXPR = r'\$\{(.*?)\}'
        keys = re.findall(EXPR, str(target))
        if keys:
            logging.info("*** processing parameters ***".center(80, "-"))
            logging.info(f"变量池中匹配到需替换的参数: {keys}")
        for key in keys:
            # value = self.variable_pool.get(key)
            value = self.var_pool_data.get(key)
            if not value:
                logging.warning("变量池中未匹配到关联参数！不进行替换操作")
                continue
            target = target.replace('${' + key + '}', str(value))
            logging.info("替换了{" + key + "} 为：" + str(value))

        # 遍历所有函数助手并执行，结束后替换
        FUNC_EXPR = r'__.*?\(.*?\)'
        funcs = re.findall(FUNC_EXPR, str(target))
        for func in funcs:
            fuc = func.split('__')[1]
            fuc_name = fuc.split("(")[0]
            fuc = fuc.replace(fuc_name, fuc_name.lower())
            value = eval(fuc)
            target = target.replace(func, str(value))
        try:
            target = eval(target)
        except:
            target = target
        return target

    def save_variable(self, target, key, jsonpath_expression=None, regular_expression=None):
        """
        存储变量到变量池
        :param target: 目标字符串
        :param key: 关键字
        :param jsonpath_expression: JSONPATH表达式
        :param regular_expression: 正则表达式
        :return:
        """
        # match_values = jsonpath.jsonpath(json.loads(target),
        #                                  jsonpath_expression) if jsonpath_expression else re.findall(
        #     regular_expression, target)
        if jsonpath_expression:
            match_values = jsonpath.jsonpath(target, jsonpath_expression)
        else:
            match_values = re.findall(regular_expression, target)

        if match_values:
            value = match_values[0]
            self.var_pool_data[key] = value
            print(f"add_var_data保存了变量 {key} --> {value} 到 变量池, 当前变量池参数 {self.var_pool_data}")
            return value
        else:
            logging.warning("未匹配到任何参数，不进行保存！")
            return

    def get_variable(self):
        return self.var_pool_data

    def get_result(self):
        return self.result
