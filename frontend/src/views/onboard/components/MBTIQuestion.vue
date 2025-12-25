<template>
  <!-- ==================== MBTI 질문 카드 ==================== -->
  <div class="card bg-base-100 shadow-lg border border-base-content/10">
    <div class="card-body p-8">
      <!-- 질문 번호 및 타입 -->
      <div class="flex items-center gap-3 mb-4">
        <div class="badge badge-primary badge-lg">Q{{ questionNumber }}</div>
        <div class="text-sm text-base-content/60">{{ typeLabel }}</div>
      </div>

      <!-- 질문 -->
      <h3 class="text-xl font-bold mb-6 leading-relaxed">
        {{ question }}
      </h3>

      <!-- 선택지 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button
          v-for="option in options"
          :key="option.value"
          type="button"
          @click="$emit('select', option.value)"
          class="btn btn-lg h-auto min-h-[120px] flex-col items-start text-left transition-all"
          :class="
            selected === option.value
              ? 'btn-primary shadow-lg scale-105'
              : 'btn-outline hover:btn-primary hover:scale-105'
          "
        >
          <div class="w-full">
            <div class="flex items-center justify-between mb-2">
              <span class="text-2xl font-bold">{{ option.label }}</span>
              <div
                v-if="selected === option.value"
                class="badge badge-secondary badge-sm"
              >
                선택됨
              </div>
            </div>
            <p class="text-sm opacity-80 whitespace-normal leading-relaxed">
              {{ option.description }}
            </p>
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
// ==================== Props & Emits ====================
defineProps({
  questionNumber: {
    type: Number,
    required: true,
  },
  typeLabel: {
    type: String,
    required: true,
  },
  question: {
    type: String,
    required: true,
  },
  options: {
    type: Array,
    required: true,
  },
  selected: {
    type: String,
    default: null,
  },
})

defineEmits(['select'])
</script>
