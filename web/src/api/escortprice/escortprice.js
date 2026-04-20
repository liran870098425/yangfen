import { request } from '@/api/service'

export function getEscortPriceList(params) {
  return request({
    url: '/api/escortprice/',
    method: 'get',
    params
  })
}

export function createEscortPrice(data) {
  return request({
    url: '/api/escortprice/',
    method: 'post',
    data
  })
}

export function updateEscortPrice(id, data) {
  return request({
    url: '/api/escortprice/' + id + '/',
    method: 'put',
    data
  })
}

export function deleteEscortPrice(id) {
  return request({
    url: '/api/escortprice/' + id + '/',
    method: 'delete'
  })
}

export function exportExcel() {
  window.open('/api/escortprice/export_excel/')
}

export function importExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/api/escortprice/import_excel/',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}
