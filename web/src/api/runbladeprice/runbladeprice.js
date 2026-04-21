import { request } from '@/api/service'

export function getRunBladePriceList(params) {
  return request({
    url: '/api/runbladeprice/',
    method: 'get',
    params
  })
}

export function createRunBladePrice(data) {
  return request({
    url: '/api/runbladeprice/',
    method: 'post',
    data
  })
}

export function updateRunBladePrice(id, data) {
  return request({
    url: '/api/runbladeprice/' + id + '/',
    method: 'put',
    data
  })
}

export function deleteRunBladePrice(id) {
  return request({
    url: '/api/runbladeprice/' + id + '/',
    method: 'delete'
  })
}

export function exportExcel() {
  window.open('/api/runbladeprice/export_excel/')
}

export function importExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/api/runbladeprice/import_excel/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
