"""
UI自动化执行引擎
支持多种UI自动化框架：Selenium、Playwright等
"""
import json
import os
import subprocess
import tempfile
import time
from datetime import datetime

from django.conf import settings
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from uitest.models import UITestReport


class SeleniumExecutor:
    """Selenium执行器"""
    
    def __init__(self):
        self.driver = None
    
    def setup_driver(self):
        """初始化WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        return self.driver
    
    def execute_yaml_case(self, yaml_file_path):
        """执行YAML格式的测试用例"""
        import yaml
        
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            test_data = yaml.safe_load(f)
        
        driver = self.setup_driver()
        results = []
        
        try:
            for step in test_data.get('steps', []):
                action = step.get('action')
                locator = step.get('locator')
                value = step.get('value', '')
                timeout = step.get('timeout', 10)
                
                if action == 'open':
                    driver.get(value)
                elif action == 'fill':
                    element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, locator))
                    )
                    element.clear()
                    element.send_keys(value)
                elif action == 'click':
                    element = WebDriverWait(driver, timeout).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, locator))
                    )
                    element.click()
                elif action == 'wait':
                    time.sleep(value if isinstance(value, (int, float)) else 1)
                elif action == 'wait_for_element':
                    WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, locator))
                    )
                elif action == 'assert_title_contains':
                    if value not in driver.title:
                        raise AssertionError(f"标题 '{driver.title}' 不包含 '{value}'")
                elif action == 'screenshot':
                    screenshot_path = os.path.join(settings.MEDIA_ROOT, 'screenshots', f"{int(time.time())}_{value}.png")
                    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                    driver.save_screenshot(screenshot_path)
            
            # 测试成功
            results.append({'success': True, 'message': 'Test completed successfully'})
        except Exception as e:
            # 测试失败
            results.append({'success': False, 'message': str(e)})
        finally:
            if self.driver:
                self.driver.quit()
        
        return results


class PlaywrightExecutor:
    """Playwright执行器"""
    
    def __init__(self):
        self.browser = None
        self.page = None
    
    def setup_browser(self):
        """初始化浏览器"""
        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        return self.page
    
    def execute_yaml_case(self, yaml_file_path):
        """执行YAML格式的测试用例"""
        import yaml
        
        # 检查YAML文件是否存在
        if not os.path.exists(yaml_file_path):
            return [{'success': False, 'message': f'YAML file not found: {yaml_file_path}'}]
        
        try:
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                test_data = yaml.safe_load(f)
        except Exception as e:
            return [{'success': False, 'message': f'Failed to read YAML file: {str(e)}'}]
        
        # 检查是否有steps
        if not test_data or 'steps' not in test_data:
            return [{'success': False, 'message': 'Invalid YAML format: missing steps'}]
        
        page = self.setup_browser()
        results = []
        
        try:
            for step in test_data.get('steps', []):
                action = step.get('action')
                locator = step.get('locator')
                value = step.get('value', '')
                
                if action == 'open':
                    page.goto(value)
                elif action == 'fill':
                    page.fill(locator, value)
                elif action == 'click':
                    page.click(locator)
                elif action == 'wait_for_selector':
                    page.wait_for_selector(locator)
                elif action == 'assert_title':
                    assert value in page.title()
                elif action == 'screenshot':
                    screenshot_path = os.path.join(settings.MEDIA_ROOT, 'screenshots', f"{int(time.time())}_{value}.png")
                    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                    page.screenshot(path=screenshot_path)
                
                # 记录步骤执行成功
                results.append({'success': True, 'message': f'Step {action} completed', 'step': step})
            
            # 测试成功
            results.append({'success': True, 'message': 'Test completed successfully'})
        except Exception as e:
            # 测试失败
            results.append({'success': False, 'message': str(e)})
        finally:
            if self.browser:
                self.browser.close()
        
        return results


def execute_ui_test(test_case):
    """
    执行UI测试用例的主函数
    :param test_case: UITestCase实例
    :return: 执行结果
    """
    if not test_case.yaml_file:
        return {'success': False, 'message': 'No YAML file provided'}
    
    # 处理不同类型的yaml_file字段
    if hasattr(test_case.yaml_file, 'path'):
        # FileField类型
        yaml_file_path = test_case.yaml_file.path
    elif isinstance(test_case.yaml_file, str):
        # TextField类型（我们刚刚修改后的）
        yaml_file_path = test_case.yaml_file
        # 如果是相对路径，需要拼接完整路径
        if not os.path.isabs(yaml_file_path):
            yaml_file_path = os.path.join(settings.MEDIA_ROOT, yaml_file_path)
    else:
        return {'success': False, 'message': 'Invalid YAML file format'}
    
    # 检查文件是否存在
    if not os.path.exists(yaml_file_path):
        return {'success': False, 'message': f'YAML file not found: {yaml_file_path}'}
    
    # 根据用例类型选择执行器
    if test_case.case_type == 0:  # web
        executor = SeleniumExecutor()
    elif test_case.case_type == 1:  # android
        return {'success': False, 'message': 'Android UI automation not supported yet'}
    elif test_case.case_type == 2:  # ios
        return {'success': False, 'message': 'iOS UI automation not supported yet'}
    else:
        return {'success': False, 'message': f'UI automation for type {test_case.case_type} not supported yet'}
    
    results = executor.execute_yaml_case(yaml_file_path)
    
    # 保存测试报告
    last_result = results[-1]
    report = UITestReport.objects.create(
        case_belong=test_case,
        case_type=test_case.case_type,
        result=1 if last_result['success'] else 0,  # 1表示成功，0表示失败
        project_belong=test_case.project_belong,
        module_belong=test_case.module_belong,
        report_path=f"reports/ui_{test_case.id}_{int(time.time())}.html",
        report_file=last_result['message']
    )
    
    return {
        'success': last_result['success'],
        'message': last_result['message'],
        'report_id': report.id
    }