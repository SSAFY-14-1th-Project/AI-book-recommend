<template>
  <!-- ==================== 기본 정보 입력 폼 ==================== -->
  <div class="card bg-base-100 shadow-lg border border-base-content/10">
    <div class="card-body p-8">
      <h3 class="text-2xl font-bold mb-6">기본 정보를 입력해주세요</h3>

      <div class="space-y-6">
        <!-- 닉네임 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium text-base">
              닉네임
              <span class="text-error ml-1">*</span>
            </span>
            <span class="label-text-alt text-base-content/50">
              {{ nickname.length }}/20
            </span>
          </label>
          <input
            :value="nickname"
            @input="$emit('update:nickname', $event.target.value)"
            type="text"
            placeholder="사용할 닉네임을 입력하세요"
            maxlength="20"
            class="input input-bordered input-lg w-full focus:input-primary"
            required
          />
          <label class="label">
            <span class="label-text-alt text-base-content/60">
              다른 사용자에게 표시될 이름입니다
            </span>
          </label>
        </div>

        <!-- 나이 -->
        <div class="form-control">
          <label class="label">
            <span class="label-text font-medium text-base">
              나이
              <span class="text-error ml-1">*</span>
            </span>
          </label>
          <input
            :value="age"
            @input="$emit('update:age', Number($event.target.value))"
            type="number"
            min="1"
            max="150"
            placeholder="나이를 입력하세요"
            class="input input-bordered input-lg w-full focus:input-primary"
            required
          />
          <label class="label">
            <span class="label-text-alt text-base-content/60">
              맞춤형 도서 추천에 활용됩니다
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
  nickname: {
    type: String,
    required: true,
  },
  age: {
    type: Number,
    required: true,
  },
})

defineEmits(['update:nickname', 'update:age'])
</script>
