# 페이지 캐싱 및 검색 상태 유지 가이드

## 📌 개요

도서 검색 페이지에서 상세 페이지로 이동 후 뒤로가기 시 검색 필터와 결과를 유지하는 방법에 대한 가이드입니다.

### 구현된 기능
- 검색 필터 상태 유지 (검색어, 카테고리, 페이지 등)
- 스크롤 위치 유지
- 브라우저 뒤로가기/앞으로가기 지원
- URL 공유 및 북마크 지원

## 🎯 구현 방법: Query Parameters + keep-alive

두 가지 기술을 조합하여 최적의 사용자 경험을 제공합니다.

### 1. keep-alive (컴포넌트 캐싱)

**파일:** `frontend/src/layout/Layout.vue`

```vue
<template>
  <main class="max-w-300 min-h-screen w-full mx-auto">
    <Navbar />
    <!-- keep-alive로 BookView 캐싱하여 뒤로가기 시 상태 유지 -->
    <RouterView v-slot="{ Component, route }">
      <keep-alive :include="['BookView']">
        <component :is="Component" :key="route.fullPath" />
      </keep-alive>
    </RouterView>
  </main>
</template>
```

**효과:**
- 컴포넌트가 DOM에서 제거되지 않고 메모리에 캐시됨
- 스크롤 위치 자동 유지
- 렌더링 성능 향상 (재렌더링 불필요)

### 2. Query Parameters (URL 기반 상태 관리)

**파일:** `frontend/src/views/book/BookView.vue`

#### 2-1. 컴포넌트 이름 설정

```javascript
// keep-alive 캐싱을 위한 컴포넌트 이름 설정
defineOptions({
  name: 'BookView',
})
```

#### 2-2. URL에서 상태 읽기

```javascript
// URL에서 상태 읽기
const loadStateFromQuery = () => {
  const query = route.query

  // 검색어
  if (query.search) {
    filters.value.search = query.search
  }

  // 검색 타입
  if (query.searchType) {
    filters.value.searchType = query.searchType
  }

  // 카테고리 (쉼표로 구분된 문자열 -> 숫자 배열)
  if (query.categories) {
    const categoriesStr = query.categories
    filters.value.categories = categoriesStr
      .split(',')
      .map(Number)
      .filter((n) => !isNaN(n))
  }

  // 성인 도서
  if (query.adult !== undefined) {
    filters.value.adult = query.adult === 'true'
  }

  // 페이지 번호
  if (query.page) {
    currentPage.value = Number(query.page) || 1
  }

  // 페이지당 개수
  if (query.size) {
    pageSize.value = Number(query.size) || 20
  }

  // 검색 수행 여부
  if (query.searched === 'true') {
    searchPerformed.value = true
  }
}
```

#### 2-3. 상태를 URL에 저장

```javascript
// 상태를 URL에 저장
const saveStateToQuery = () => {
  const query = {}

  // 검색어가 있을 때만 저장
  if (filters.value.search) {
    query.search = filters.value.search
    query.searchType = filters.value.searchType
  }

  // 카테고리가 있을 때만 저장 (배열 -> 쉼표로 구분된 문자열)
  if (filters.value.categories.length > 0) {
    query.categories = filters.value.categories.join(',')
  }

  // 성인 도서 필터가 true일 때만 저장
  if (filters.value.adult) {
    query.adult = 'true'
  }

  // 페이지 번호 (1이 아닐 때만)
  if (currentPage.value !== 1) {
    query.page = currentPage.value
  }

  // 페이지당 개수 (20이 아닐 때만)
  if (pageSize.value !== 20) {
    query.size = pageSize.value
  }

  // 검색을 수행했다는 플래그
  if (searchPerformed.value) {
    query.searched = 'true'
  }

  // URL 업데이트 (페이지 리로드 없이)
  router.replace({ query })
}
```

#### 2-4. 라이프사이클 훅

```javascript
// ==================== Lifecycle ====================
onMounted(() => {
  // URL에서 상태 복원
  loadStateFromQuery()

  // URL에 검색 파라미터가 있으면 자동으로 검색 실행
  if (route.query.searched === 'true') {
    fetchBooks()
  }

  // 스크롤 이벤트 리스너 등록
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  // 스크롤 이벤트 리스너 제거
  window.removeEventListener('scroll', handleScroll)
})
```

#### 2-5. 브라우저 네비게이션 감지

```javascript
// ==================== Watch ====================
// 브라우저 뒤로가기/앞으로가기 감지
watch(
  () => route.query,
  () => {
    loadStateFromQuery()
    if (route.query.searched === 'true') {
      fetchBooks()
    }
  }
)
```

## 🔄 작동 방식

### 검색 시
1. 사용자가 검색 실행
2. API 호출
3. 결과 표시
4. **URL에 모든 검색 조건 저장** (`saveStateToQuery`)
   - 예: `/books?search=해리포터&categories=1,3&page=2&searched=true`

### 뒤로가기 시
1. `keep-alive`로 인해 컴포넌트 상태 유지됨
2. URL 쿼리 파라미터 감지 (`watch`)
3. URL에서 검색 조건 복원 (`loadStateFromQuery`)
4. 필요시 검색 재실행
5. **스크롤 위치도 자동 유지**

### 브라우저 뒤로/앞으로 버튼
- Vue Router의 `watch`가 URL 변경 감지
- 즉시 상태 복원
- 자연스러운 네비게이션 경험

## 🎁 장점

### 1. URL 공유 가능
```
검색 결과 URL 복사 → 공유
받는 사람도 동일한 검색 결과 확인 가능
```

### 2. 새로고침 시에도 유지
```
F5 새로고침해도 검색 상태 유지
```

### 3. 브라우저 히스토리 완벽 지원
```
뒤로가기/앞으로가기 모두 작동
Ctrl+Shift+T (닫은 탭 복원)도 작동
```

### 4. 사용자별 격리
```
URL 기반이므로 다른 사용자와 간섭 없음
로그아웃/로그인해도 문제없음
```

### 5. 성능 최적화
```
keep-alive로 불필요한 재렌더링 방지
API 중복 호출 없음
```

## 📊 다른 방법들과의 비교

| 방법 | 장점 | 단점 | 추천도 |
|------|------|------|--------|
| **Query Parameters + keep-alive** | URL 공유 가능, SEO 친화적, 브라우저 히스토리 활용 | URL이 길어질 수 있음 | ⭐⭐⭐⭐⭐ |
| Pinia Store | 간단한 구현, 전역 상태 관리 | 새로고침 시 초기화, 탭 간 공유 안됨 | ⭐⭐⭐⭐ |
| SessionStorage | 탭별로 격리, 새로고침 유지 | 탭 닫으면 삭제, 공유 불가 | ⭐⭐⭐ |
| LocalStorage | 영구 보존 | 다른 사용자 간섭 가능성 | ⭐⭐ |

## 🧪 테스트 시나리오

### 1. 기본 흐름
```
검색 → 결과 확인 → 도서 클릭 → 상세 페이지
→ 뒤로가기 ✅ 검색 결과 유지됨
```

### 2. 페이지네이션
```
검색 → 2페이지로 이동 → 도서 클릭
→ 뒤로가기 ✅ 2페이지 상태 유지됨
```

### 3. 복잡한 필터
```
검색어 입력 + 카테고리 2개 선택 + 성인 도서 포함
→ 도서 클릭 → 뒤로가기 ✅ 모든 필터 유지됨
```

### 4. URL 공유
```
검색 후 URL 복사 → 새 탭에서 열기
✅ 동일한 검색 결과 표시됨
```

### 5. 브라우저 버튼
```
검색 → 홈 이동 → 뒤로가기
✅ 검색 상태 유지됨
```

## 🌐 프레임워크별 비교

### Vue (현재 사용)
```vue
<!-- keep-alive 내장 지원 -->
<keep-alive>
  <component :is="Component" />
</keep-alive>
```
✅ 가장 간단한 구현
✅ 컴포넌트 전체 상태 보존 (DOM, 스크롤, 타이머 등)

### React
```jsx
// keep-alive 기능 없음
// 직접 구현하거나 라이브러리 사용 필요
- react-activation
- react-keep-alive
- React Query (데이터 캐싱)
```
⚠️ 추가 라이브러리 필요
⚠️ 데이터만 캐싱 (컴포넌트는 재렌더링)

### Next.js
```jsx
// 서버 컴포넌트 캐싱은 자동
// 클라이언트 컴포넌트는 별도 처리
```
✅ 서버 캐싱 자동
⚠️ 클라이언트 상태는 수동 관리

### Angular
```typescript
// RouteReuseStrategy 직접 구현
export class CustomReuseStrategy implements RouteReuseStrategy {
  // 커스텀 구현 필요
}
```
⚠️ 복잡한 구현

## 💡 핵심 포인트

### 1. 개념은 동일
```
모든 방법의 공통점: "상태를 어딘가에 저장했다가 복원"
```

### 2. 차이는 "저장 위치"
```
- URL: 브라우저 주소창
- Pinia: JavaScript 메모리
- Storage: 브라우저 저장소
```

### 3. URL 방식의 핵심 장점
```
브라우저의 네이티브 히스토리 기능 활용
→ 뒤로가기/앞으로가기 자동 처리
→ 북마크, 공유, 새로고침 모두 지원
```

### 4. keep-alive의 역할
```
컴포넌트 자체를 메모리에 보관
→ 렌더링조차 안 함 (최고 성능)
→ Vue만의 강력한 기능
```

## 📝 URL 쿼리 파라미터 스키마

현재 구현된 URL 파라미터:

```
/books?
  search=검색어           // 검색어
  &searchType=title      // 검색 타입 (title | author)
  &categories=1,3,5      // 카테고리 ID (쉼표 구분)
  &adult=true            // 성인 도서 포함
  &page=2                // 현재 페이지
  &size=20               // 페이지당 개수
  &searched=true         // 검색 수행 플래그
```

### 최적화 규칙
```javascript
// 기본값은 URL에 저장하지 않음 (URL 간결화)
- page=1 → 생략
- size=20 → 생략
- searchType=title → 생략
- adult=false → 생략
```

## 🔧 실무 팁

### 1. URL 길이 제한
```
브라우저마다 URL 길이 제한 있음 (보통 2000자)
→ 너무 많은 데이터는 Storage 사용 고려
```

### 2. 민감한 정보
```
URL은 브라우저 히스토리에 남음
→ 민감한 정보는 URL에 저장하지 말 것
```

### 3. SEO 고려
```
검색엔진이 URL 파라미터 인덱싱 가능
→ 공개되어도 되는 정보만 URL에 저장
```

### 4. keep-alive 메모리 관리
```vue
<!-- 특정 컴포넌트만 캐싱 -->
<keep-alive :include="['BookView']">
  <!-- 필요한 것만 캐싱하여 메모리 절약 -->
</keep-alive>
```

## 🎯 결론

**Query Parameters + keep-alive 조합**은 Vue.js에서 페이지 상태를 유지하는 가장 효율적이고 사용자 친화적인 방법입니다.

### 주요 이점
1. ✅ 구현이 간단 (Vue 내장 기능 활용)
2. ✅ 완벽한 브라우저 통합
3. ✅ URL 공유 및 북마크 지원
4. ✅ 최고의 성능 (불필요한 재렌더링 없음)
5. ✅ 사용자별 완벽 격리

### 적용 페이지
- 검색 페이지
- 필터가 있는 목록 페이지
- 페이지네이션이 있는 페이지
- 사용자가 돌아올 가능성이 높은 페이지

---

**작성일:** 2025-12-25
**프로젝트:** AI Book Recommendation
**작성자:** jiwon
