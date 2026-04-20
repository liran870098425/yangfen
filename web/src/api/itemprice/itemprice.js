import { request } from '@/api/service'

export function getItemPriceList(params) {
  return request({
    url: '/api/itemprice/',
    method: 'get',
    params
  })
}

export function getItemPriceDetail(id) {
  return request({
    url: `/api/itemprice/${id}/`,
    method: 'get'
  })
}

export function createItemPrice(data) {
  return request({
    url: '/api/itemprice/',
    method: 'post',
    data
  })
}

export function updateItemPrice(id, data) {
  return request({
    url: `/api/itemprice/${id}/`,
    method: 'put',
    data
  })
}

export function deleteItemPrice(id) {
  return request({
    url: `/api/itemprice/${id}/`,
    method: 'delete'
  })
}

export function exportExcel() {
  window.open('/api/itemprice/export_excel/')
}

export function importExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/api/itemprice/import_excel/',
    method: 'post',
    data: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export function batchUpdatePrice(data) {
  return request({
    url: '/api/itemprice/batch_update_price/',
    method: 'post',
    data
  })
}
