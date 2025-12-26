import client from './client'

// 중고거래 목록 조회
export const getTradeList = () => {
  return client.get('/api/trades/')
}

// 중고거래 상세 조회
export const getTradeDetail = (tradeId) => {
  return client.get(`/api/trades/${tradeId}/`)
}

// 중고거래 생성
export const createTrade = (bookPk, tradeData) => {
  return client.post(`/api/trades/create/${bookPk}/`, tradeData)
}

// 중고거래 수정
export const updateTrade = (tradeId, tradeData) => {
  return client.put(`/api/trades/${tradeId}/`, tradeData)
}

// 중고거래 삭제
export const deleteTrade = (tradeId) => {
  return client.delete(`/api/trades/${tradeId}/`)
}

// 중고거래 검색
export const searchTrades = (params) => {
  return client.get('/api/trades/search/', { params })
}

// 중고거래 수정용 조회 (kakao_chat_url 포함)
export const getTradeForEdit = (tradeId) => {
  return client.get(`/api/trades/${tradeId}/edit/`)
}
