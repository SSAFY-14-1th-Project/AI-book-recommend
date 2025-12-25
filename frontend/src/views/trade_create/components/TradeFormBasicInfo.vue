<template>
  <!-- ==================== 기본 정보 입력 ==================== -->
  <div class="card bg-base-100 shadow-sm border border-base-content/5">
    <div class="card-body p-6">
      <h3 class="text-lg font-bold mb-4 flex items-center gap-2">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-primary"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
          />
        </svg>
        게시글 정보
      </h3>

      <div class="space-y-4">
        <!-- 제목 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium">
              제목
              <span class="text-error ml-1">*</span>
            </span>
            <span class="label-text-alt text-base-content/50">{{ title.length }}/50</span>
          </label>
          <input
            :value="title"
            @input="$emit('update:title', $event.target.value)"
            type="text"
            placeholder="예: 자바의 정석 팝니다 (거의 새책)"
            maxlength="50"
            class="input input-bordered w-full focus:input-primary"
            required
          />
        </div>

        <!-- 내용 -->
        <div class="flex flex-col w-full">
          <label class="label">
            <span class="label-text font-medium">
              상세 설명
              <span class="text-error ml-1">*</span>
            </span>
            <span class="label-text-alt text-base-content/50">{{ content.length }}/1000</span>
          </label>
          <textarea
            :value="content"
            @input="$emit('update:content', $event.target.value)"
            placeholder="거래하실 책의 상태, 거래 방법 등을 자세히 작성해주세요.&#10;&#10;예시:&#10;- 책 상태: 깨끗하며 밑줄 및 낙서 없음&#10;- 거래 방법: 직거래 또는 택배 가능&#10;- 기타: 빠른 거래 원합니다"
            maxlength="1000"
            class="textarea textarea-bordered h-40 resize-none focus:textarea-primary w-full"
            required
          ></textarea>
          <label class="label">
            <span class="label-text-alt text-base-content/50">
              책의 상태와 거래 방법을 구체적으로 작성하면 더 빠른 거래가 가능합니다
            </span>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== Props & Emits ====================
defineProps({
  title: {
    type: String,
    required: true,
  },
  content: {
    type: String,
    required: true,
  },
})

defineEmits(['update:title', 'update:content'])
</script>
