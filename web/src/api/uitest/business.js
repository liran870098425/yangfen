import { request } from '@/api/service'

// 获取业务数据列表
export function getBusinessList(params) {
  return request({
    url: '/api/uitest/business/',
    method: 'get',
    params
  })
}

// 新增业务数据
export function createBusiness(data) {
  return request({
    url: '/api/uitest/business/',
    method: 'post',
    data
  })
}

// 更新业务数据
export function updateBusiness(id, data) {
  return request({
    url: `/api/uitest/business/${id}/`,
    method: 'put',
    data
  })
}

// 删除业务数据
export function deleteBusiness(id) {
  return request({
    url: `/api/uitest/business/${id}/`,
    method: 'delete'
  })
}

// 获取统计数据
export function getStats(month) {
  return request({
    url: '/api/uitest/business/stats/',
    method: 'get',
    params: { month }
  }).then(res => {
    console.log('=== getStats raw res ===', JSON.stringify(res))
    return res
  })
}

// 获取按月汇总
export function getMonthlyList() {
  return request({
    url: '/api/uitest/business/monthly_list/',
    method: 'get'
  })
}

// 导出Excel
export function exportExcel() {
  window.open('/api/uitest/business/export_excel/')
}
