/*
 * @创建文件时间: 2025-11-23 16:05:00
 * @Auther: 码同学
 * @功能: UI测试相关API接口
 */

import { request } from '@/api/service'

/**
 * @description 获取UI测试用例列表
 * @param {Object} params 查询参数
 */
export function getUiTestCaseList (params) {
  return request({
    url: '/uitest/case/',
    method: 'get',
    params
  })
}

/**
 * @description 创建UI测试用例
 * @param {Object} data 用例数据
 */
export function createUiTestCase (data) {
  return request({
    url: '/uitest/case/',
    method: 'post',
    data
  })
}

/**
 * @description 更新UI测试用例
 * @param {Number} id 用例ID
 * @param {Object} data 用例数据
 */
export function updateUiTestCase (id, data) {
  return request({
    url: `/uitest/case/${id}/`,
    method: 'put',
    data
  })
}

/**
 * @description 删除UI测试用例
 * @param {Number} id 用例ID
 */
export function deleteUiTestCase (id) {
  return request({
    url: `/uitest/case/${id}/`,
    method: 'delete'
  })
}

/**
 * @description 执行UI测试用例
 * @param {Number} id 用例ID
 */
export function executeUiTestCase (id) {
  return request({
    url: `/uitest/case/${id}/execute/`,
    method: 'post'
  })
}

/**
 * @description 获取UI测试报告列表
 * @param {Object} params 查询参数
 */
export function getUiTestReportList (params) {
  return request({
    url: '/uitest/report/',
    method: 'get',
    params
  })
}
