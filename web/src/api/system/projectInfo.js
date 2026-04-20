/*
 * @创建文件时间: 2025-11-23 16:07:00
 * @Auther: 码同学
 * @功能: 系统项目信息相关API接口
 */

import { request } from '@/api/service'

/**
 * @description 获取项目列表
 * @param {Object} params 查询参数
 */
export function getProjectList (params) {
  return request({
    url: '/base/projectInfo/',
    method: 'get',
    params
  })
}

/**
 * @description 创建项目
 * @param {Object} data 项目数据
 */
export function createProject (data) {
  return request({
    url: '/base/projectInfo/',
    method: 'post',
    data
  })
}

/**
 * @description 更新项目
 * @param {Number} id 项目ID
 * @param {Object} data 项目数据
 */
export function updateProject (id, data) {
  return request({
    url: `/base/projectInfo/${id}/`,
    method: 'put',
    data
  })
}

/**
 * @description 删除项目
 * @param {Number} id 项目ID
 */
export function deleteProject (id) {
  return request({
    url: `/base/projectInfo/${id}/`,
    method: 'delete'
  })
}
