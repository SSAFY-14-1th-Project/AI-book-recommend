# 중고거래 검색 페이지 구현 가이드

## 📋 목차
1. [개요](#개요)
2. [구현된 기능](#구현된-기능)
3. [컴포넌트 구조](#컴포넌트-구조)
4. [API 파라미터 매핑](#api-파라미터-매핑)
5. [주요 이슈 및 해결방법](#주요-이슈-및-해결방법)
6. [사용 방법](#사용-방법)

---

## 개요

중고거래 검색 페이지를 BookView와 동일한 디자인 패턴으로 구현했습니다.
- **디자인 시스템**: DaisyUI
- **참고 페이지**: `frontend/src/views/book/BookView.vue`
- **API 엔드포인트**: `/api/trades/search/`

---

## 구현된 기능

### ✅ 검색 필터링
- **검색어**: 제목/도서명/내용으로 검색
- **지역 필터**: 17개 시도 다중 선택
- **가격 범위**: 최소/최대 가격 설정
- **거래 타입**: 전체/판매/무료나눔
- **거래 상태**: 전체/판매중/예약중/판매완료

### ✅ UX 기능
- URL 쿼리 파라미터 저장 (새로고침/뒤로가기 지원)
- 활성 필터 뱃지 표시
- 개별/전체 필터 초기화
- 페이지네이션
- 맨 위로 스크롤 버튼
- 스켈레톤 로딩

### ✅ 유효성 검사
- 최소 가격 > 최대 가격 방지
- 무료나눔 선택 시 가격 필터 자동 초기화

---

## 컴포넌트 구조

```
frontend/src/views/trade/
├── TradeView.vue                          # 메인 페이지
└── components/
    ├── TradeSearchFilter.vue              # 검색 필터
    ├── TradeGrid.vue                      # 거래 목록 그리드
    ├── TradeCard.vue                      # 개별 거래 카드
    ├── TradeCardSkeleton.vue              # 로딩 스켈레톤
    └── TradePagination.vue                # 페이지네이션
```

### 1. TradeView.vue
메인 컨테이너 컴포넌트
- 상태 관리 (filters, trades, pagination)
- API 호출 (`searchTrades`)
- URL 쿼리 파라미터 관리
- 라우팅 처리

### 2. TradeSearchFilter.vue
검색 및 필터링 UI
- 검색어 입력
- 지역 다중 선택 (17개 시도)
- 거래 타입/상태 선택
- 가격 범위 입력
- 활성 필터 뱃지 표시

### 3. TradeGrid.vue
거래 목록 그리드 레이아웃
- 반응형 그리드 (5컬럼 → 모바일 1컬럼)
- 로딩/검색결과 상태 처리

### 4. TradeCard.vue
개별 거래 카드
- 이미지, 제목, 가격, 지역, 날짜
- 거래 상태/타입 배지
- 호버 애니메이션

### 5. TradePagination.vue
페이지네이션 컴포넌트
- DaisyUI join 스타일
- 페이지 범위 계산 (생략 표시)

---

## API 파라미터 매핑

### 백엔드 API 스펙
엔드포인트: `GET /api/trades/search/`

| 프론트엔드 | 백엔드 | 타입 | 설명 |
|-----------|--------|------|------|
| `regions` | `region` | Array | 지역 필터 (다중 선택) |
| `saleTypes: "sell"` | `saleType: "sale"` | String | 판매 타입 |
| `saleTypes: "free"` | `saleType: "free"` | String | 무료나눔 타입 |
| `status` | `status` | String | 거래 상태 |
| `search` | `search` | String | 검색어 |
| `searchType` | `searchType` | String | 검색 타입 |
| `minPrice` | `minPrice` | Number | 최소 가격 |
| `maxPrice` | `maxPrice` | Number | 최대 가격 |
| `currentPage` | `page` | Number | 페이지 번호 |
| `pageSize` | `size` | Number | 페이지 크기 |

### 주요 변환 로직

```javascript
// TradeView.vue - fetchTrades()

// 1. 지역 필터: regions → region (배열)
if (filters.value.regions.length > 0) {
  params.region = [...filters.value.regions]
}

// 2. 거래 타입: saleTypes → saleType, "sell" → "sale"
if (filters.value.saleTypes) {
  params.saleType = filters.value.saleTypes === 'sell' ? 'sale' : filters.value.saleTypes
}

// 3. 무료나눔일 때 가격 파라미터 제외
if (filters.value.saleTypes !== 'free') {
  if (filters.value.minPrice) params.minPrice = filters.value.minPrice
  if (filters.value.maxPrice) params.maxPrice = filters.value.maxPrice
}
```

### 백엔드 응답 구조

```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "total_pages": 3,
  "results": [
    {
      "id": 1,
      "title": "책 제목",
      "content": "설명",
      "sale_type": "sale",
      "price": 10000,
      "region": "seoul",
      "status": "available",
      "book_title": "도서명",
      "book_adult": false,
      "seller": "판매자ID",
      "image": "/media/...",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## 주요 이슈 및 해결방법

### 🐛 Issue 1: 파라미터명 불일치
**문제**: 프론트엔드에서 `regions`, `saleTypes`로 보냈으나 백엔드는 `region`, `saleType` 기대

**원인**: Swagger 문서와 실제 백엔드 코드 불일치

**해결**:
```javascript
// Before
params.regions = [...filters.value.regions]
params.saleTypes = filters.value.saleTypes

// After
params.region = [...filters.value.regions]
params.saleType = filters.value.saleTypes === 'sell' ? 'sale' : filters.value.saleTypes
```

### 🐛 Issue 2: 거래 타입 값 불일치
**문제**: UI에서 "판매"를 `sell`로 보냈으나 백엔드는 `sale` 기대

**원인**: 백엔드 모델의 `SALE_TYPE_CHOICES` 확인 필요

**해결**: 값 변환 로직 추가
```javascript
params.saleType = filters.value.saleTypes === 'sell' ? 'sale' : filters.value.saleTypes
```

### 🐛 Issue 3: 거래 상태 필터 버그 (백엔드)
**문제**: `status` 파라미터가 `available`만 처리되고 `reserved`, `sold` 무시됨

**원인**: 백엔드 코드에서 조건문 오류
```python
# Before (버그)
status = request.query_params.get("status")
if status == "available":
    queryset = queryset.filter(status="available")
```

**해결**: 백엔드 코드 수정
```python
# After (수정)
status = request.query_params.get("status")
if status:
    queryset = queryset.filter(status=status)
```

**파일**: `backend/trades/views.py:140-143`

### 🐛 Issue 4: 무료나눔 선택 시 가격 필터 처리
**문제**: 무료나눔 선택 후에도 기존 가격 필터가 유지됨

**해결**:
1. UI에서 가격 입력 필드 숨김
```vue
<div v-if="localFilters.saleTypes !== 'free'" class="flex items-center gap-2">
```

2. 거래 타입 변경 시 가격 초기화
```javascript
const handleSaleTypeChange = () => {
  if (localFilters.value.saleTypes === 'free') {
    localFilters.value.minPrice = null
    localFilters.value.maxPrice = null
  }
  handleFilterChange()
}
```

3. API 호출 시 가격 파라미터 제외
```javascript
if (filters.value.saleTypes !== 'free') {
  if (filters.value.minPrice) params.minPrice = filters.value.minPrice
  if (filters.value.maxPrice) params.maxPrice = filters.value.maxPrice
}
```

### 🐛 Issue 5: 가격 유효성 검사
**문제**: 최소 가격 > 최대 가격 입력 가능

**해결**: 검색 실행 전 유효성 검사
```javascript
const isPriceValid = () => {
  const { minPrice, maxPrice } = localFilters.value
  if (!minPrice && !maxPrice) return true
  if (!minPrice || !maxPrice) return true
  return minPrice <= maxPrice
}

const handleSearch = () => {
  if (!isPriceValid()) {
    alert('최소 가격은 최대 가격보다 작거나 같아야 합니다.')
    return
  }
  handleFilterChange()
  emit('search')
}
```

---

## 사용 방법

### 1. 기본 검색
```
1. 검색어 입력
2. 검색 타입 선택 (제목/도서명/내용)
3. "검색" 버튼 클릭
```

### 2. 지역 필터
```
1. 원하는 지역 버튼 클릭 (다중 선택 가능)
2. "전체" 버튼으로 지역 필터 초기화
```

### 3. 거래 타입 & 상태
```
1. 거래 타입: 전체/판매/무료나눔
2. 상태: 전체/판매중/예약중/판매완료
```

### 4. 가격 범위 (판매만 해당)
```
1. 최소 가격 입력
2. 최대 가격 입력
3. 무료나눔 선택 시 가격 필터 자동 숨김/초기화
```

### 5. 필터 초기화
```
- 개별 초기화: 활성 필터 뱃지의 ✕ 버튼 클릭
- 전체 초기화: "모든 필터 초기화" 버튼 클릭
```

---

## 지역 목록

| 코드 | 이름 |
|------|------|
| `seoul` | 서울 |
| `busan` | 부산 |
| `daegu` | 대구 |
| `incheon` | 인천 |
| `gwangju` | 광주 |
| `daejeon` | 대전 |
| `ulsan` | 울산 |
| `sejong` | 세종 |
| `gyeonggi` | 경기 |
| `gangwon` | 강원 |
| `chungbuk` | 충북 |
| `chungnam` | 충남 |
| `jeonbuk` | 전북 |
| `jeonnam` | 전남 |
| `gyeongbuk` | 경북 |
| `gyeongnam` | 경남 |
| `jeju` | 제주 |

---

## 거래 상태 매핑

| 코드 | 표시 | 배지 색상 |
|------|------|----------|
| `available` | 판매중 | success (녹색) |
| `reserved` | 예약중 | warning (노란색) |
| `sold` | 판매완료 | ghost (회색) |

---

## 파일 구조

```
frontend/src/
├── views/
│   └── trade/
│       ├── TradeView.vue                  # 메인 페이지
│       └── components/
│           ├── TradeSearchFilter.vue      # 검색 필터
│           ├── TradeGrid.vue              # 그리드
│           ├── TradeCard.vue              # 카드
│           ├── TradeCardSkeleton.vue      # 스켈레톤
│           └── TradePagination.vue        # 페이지네이션
└── api/
    └── trades.js                          # API 함수

backend/
└── trades/
    ├── views.py                           # API 뷰 (수정됨)
    ├── models.py                          # 모델 정의
    └── serializers.py                     # 시리얼라이저
```

---

## 디자인 시스템

### DaisyUI 컴포넌트 사용
- `btn`, `btn-primary`, `btn-ghost` - 버튼
- `input`, `input-bordered` - 입력 필드
- `select`, `select-bordered` - 선택 박스
- `card`, `card-body` - 카드
- `badge`, `badge-primary`, `badge-success` - 배지
- `join`, `join-item` - 페이지네이션

### 반응형 브레이크포인트
- `sm`: 640px - 2컬럼
- `md`: 768px - 3컬럼
- `lg`: 1024px - 4컬럼
- `xl`: 1280px - 5컬럼

---

## 추가 개선 가능 사항

1. **정렬 기능**: 최신순, 가격순, 오래된순
2. **무한 스크롤**: 페이지네이션 대신 무한 스크롤
3. **필터 프리셋**: 자주 사용하는 필터 저장
4. **지도 뷰**: 지역별 거래 지도 표시
5. **찜하기**: 관심 거래 북마크

---

---

## 중고거래 상세 페이지 컴포넌트 분리

### 📁 컴포넌트 구조

```
frontend/src/views/trade_detail/
├── TradeDetailView.vue                    # 메인 상세 페이지
└── components/
    ├── TradeDetailHeader.vue              # 헤더 (제목, 가격, 할인율, 상태)
    ├── TradeDetailImage.vue               # 거래 이미지
    ├── TradeDetailInfo.vue                # 도서 정보 & 거래 설명
    └── TradeDetailActions.vue             # 액션 버튼 (채팅/수정/삭제)
```

### 1. TradeDetailHeader.vue
**담당 영역**: 거래 헤더 정보
- 거래 제목, 상태 배지, 무료나눔 배지
- 가격 및 할인율 표시 (정가 대비)
- 판매자 정보 (닉네임)
- 지역, 작성일, 조회수

**주요 기능**:
- 할인율 계산: `book.price_standard` 기준으로 계산
- 할인율 색상 코딩: 50%+ 빨강, 30-50% 주황, 0-30% 초록, 음수 회색
- camelCase/snake_case 양쪽 지원

```javascript
// 할인율 계산
const bookPriceStandard = trade.book?.priceStandard || trade.book?.price_standard
const discountRate = ((bookPriceStandard - price) / bookPriceStandard) * 100
```

### 2. TradeDetailImage.vue
**담당 영역**: 거래 이미지 표시
- 이미지 로딩 및 에러 처리
- 이미지 없을 때 기본 아이콘 표시
- 반응형 이미지 크기 조절

**주요 기능**:
- 상대 경로 → 절대 URL 변환
- 이미지 로드 실패 시 대체 UI 표시

```javascript
const imageUrl = computed(() => {
  if (!props.image || imageError.value) return ''
  if (props.image.startsWith('http')) return props.image
  return `http://localhost:8000${props.image}`
})
```

### 3. TradeDetailInfo.vue
**담당 영역**: 도서 정보 및 거래 설명
- 도서명, 정가, 카테고리 정보 표시
- 거래 상세 설명 (whitespace-pre-wrap으로 줄바꿈 유지)

**UI 패턴**:
- 그리드 레이아웃으로 정보 나열
- 섹션별 구분선 (border-b)
- DaisyUI badge로 카테고리 표시

### 4. TradeDetailActions.vue
**담당 영역**: 액션 버튼 영역
- **본인 게시글이 아닐 때**: 카카오톡 오픈채팅 버튼
- **본인 게시글일 때**: 수정/삭제 버튼
- **공통**: 목록으로 돌아가기 버튼

**Props**:
```javascript
{
  tradeId: Number,           // 거래 ID
  isOwner: Boolean,          // 본인 게시글 여부
  kakaoChatUrl: String,      // 카카오톡 오픈채팅 URL
}
```

**Emits**:
- `delete`: 삭제 버튼 클릭 시 부모 컴포넌트로 이벤트 전달

### 5. TradeDetailView.vue (리팩토링)
**주요 변경사항**:
- 컴포넌트 분리로 코드 가독성 향상
- 로딩/에러/성공 상태별 UI 분리
- `isOwner` computed 속성으로 권한 체크

**컴포넌트 구성**:
```vue
<TradeDetailHeader :trade="trade" />
<TradeDetailImage :image="trade.image" :alt="trade.title" />
<TradeDetailInfo :book="trade.book" :content="trade.content" />
<TradeDetailActions
  :trade-id="trade.id"
  :is-owner="isOwner"
  :kakao-chat-url="trade.kakaoChatUrl || trade.kakao_chat_url"
  @delete="handleDelete"
/>
```

---

## 컴포넌트 분리 설계 원칙

### ✅ 분리 기준
1. **단일 책임 원칙**: 각 컴포넌트는 하나의 명확한 역할만 수행
2. **재사용성**: 다른 페이지에서도 사용 가능한 구조
3. **독립성**: 컴포넌트 간 의존도 최소화
4. **가독성**: 컴포넌트명만으로 역할 파악 가능

### 📦 분리 전후 비교

**Before**: TradeDetailView.vue (단일 파일)
- 모든 로직과 UI가 한 파일에 집중
- 코드 길이 증가로 가독성 저하
- 특정 부분 수정 시 전체 파일 탐색 필요

**After**: TradeDetailView.vue + 4개 컴포넌트
- 각 영역별로 파일 분리
- 수정 필요 시 해당 컴포넌트만 열면 됨
- 테스트 및 유지보수 용이

---

## 디자인 개선 사항

### 🎨 DaisyUI 활용
1. **Badge 컴포넌트**
   - 거래 상태: `badge-success` (판매중), `badge-warning` (예약중), `badge-ghost` (판매완료)
   - 무료나눔: `badge-success`
   - 카테고리: `badge-primary`

2. **Button 컴포넌트**
   - 기본: `btn btn-primary btn-lg`
   - 수정: `btn btn-outline btn-lg`
   - 삭제: `btn btn-error btn-lg`
   - 목록: `btn btn-ghost btn-lg`

3. **레이아웃**
   - `grid grid-cols-1 lg:grid-cols-2`: 반응형 2컬럼 레이아웃
   - `border-b border-base-content/10`: 섹션 구분선
   - `space-y-4`: 일관된 간격

### 📱 반응형 디자인
- **데스크톱** (lg 이상): 이미지와 정보가 좌우 배치
- **모바일**: 세로 스택 레이아웃

---

## 날짜: 2024-12-25
## 작성자: Claude Code
## 문서 버전: 1.1
## 업데이트: 중고거래 상세 페이지 컴포넌트 분리 추가
