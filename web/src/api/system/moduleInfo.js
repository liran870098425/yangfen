/*
 * @创建文件时间: 2025-11-23 16:07:00
 * @Auther: 码同学
 * @功能: 系统模块信息相关API接口
 */

import { request } from '@/api/service'

/**
 * @description 获取模块列表
 * @param {Object} params 查询参数
 */
export function getModuleList (params) {
  return request({
    url: '/base/moduleInfo/',
    method: 'get',
    params
  })
}

/**
 * @description 创建模块
 * @param {Object} data 模块数据
 */
export function createModule (data) {
  return request({
    url: '/base/moduleInfo/',
    method: 'post',
    data
  })
}

/**
 * @description 更新模块
 * @param {Number} id 模块ID
 * @param {Object} data 模块数据
 */
export function updateModule (id, data) {
  return request({
    url: `/base/moduleInfo/${id}/`,
    method: 'put',
    data
  })
}

/**
 * @description 删除模块
 * @param {Number} id 模块ID
 */
export function deleteModule (id) {
  return request({
    url: `/base/moduleInfo/${id}/`,
    method: 'delete'
  })
}
