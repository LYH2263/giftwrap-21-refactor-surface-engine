<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'

const items = ref([])
const err = ref('')

onMounted(async () => {
  try {
    items.value = (await getJSON('/api/runs')).items
  } catch (e) {
    err.value = String(e.message || e)
  }
})
</script>

<template>
  <div class="page">
    <h1>用纸档</h1>
    <p class="lede">算纸页「写入用纸档」后的落库结果，按次保留盒名与面积。详情字段均为接口读回，页面不另算面积。</p>
    <p v-if="err" class="bad">{{ err }}</p>
    <p v-else-if="!items.length" class="empty">还没有写入过。先去算纸试一单。</p>
    <ul v-else class="item-list">
      <li v-for="r in items" :key="r.id">
        <details>
          <summary>
            <span>{{ r.box_name }}</span>
            <span class="meta">{{ r.result?.paper_m2 ?? '—' }} m²</span>
          </summary>
          <dl class="run-detail">
            <div><dt>用纸面积</dt><dd>{{ r.result?.paper_m2 ?? '—' }} m²</dd></div>
            <div><dt>六面面积</dt><dd>{{ r.result?.box_surface ?? '—' }} m²</dd></div>
            <div><dt>折边系数</dt><dd>{{ r.overlap ?? r.result?.overlap ?? '—' }}</dd></div>
            <div><dt>丝带 ({{ r.result?.ribbon?.wrap_style ?? 'cross' }})</dt><dd>{{ r.result?.ribbon?.ribbon_m ?? '—' }} m</dd></div>
            <div><dt>写入时间</dt><dd>{{ r.created_at ?? '—' }}</dd></div>
            <div v-if="r.note"><dt>备注</dt><dd>{{ r.note }}</dd></div>
          </dl>
        </details>
      </li>
    </ul>
  </div>
</template>
