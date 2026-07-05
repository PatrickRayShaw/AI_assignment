<template>
  <div>
    <el-card>
      <h3>🔍 智能语义检索</h3>
      <div style="display:flex;gap:12px;margin:16px 0">
        <el-input v-model="query" placeholder="输入您的问题，如：最近AI领域有什么新进展？" size="large" @keyup.enter="doSearch" />
        <el-button type="primary" size="large" @click="doSearch" :loading="searching">搜索</el-button>
      </div>
      <div v-if="results.length > 0">
        <div v-for="(item, index) in results" :key="index" class="result-item">
          <div class="result-header">
            <strong>{{ item.title }}</strong>
            <el-tag v-if="item.similarity" size="small" type="info">{{ item.similarity }}% 匹配</el-tag>
          </div>
          <p class="result-content">{{ item.content || item.summary || '无内容' }}</p>
          <div class="result-meta">
            <span>来源：{{ item.source || '本地知识库' }}</span>
            <span v-if="item.tags">
              <el-tag v-for="tag in item.tags" :key="tag" size="small" style="margin-left:4px">{{ tag }}</el-tag>
            </span>
          </div>
        </div>
      </div>
      <el-empty v-else-if="!searching && searched" description="未找到相关结果" />
      <el-empty v-else description="请输入搜索内容" />
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { semanticSearch } from '@/api/search'
import { ElMessage } from 'element-plus'

const query = ref('')
const searching = ref(false)
const searched = ref(false)
const results = ref([])

const doSearch = async () => {
  if (!query.value.trim()) {
    ElMessage.warning('请输入搜索内容')
    return
  }
  searching.value = true
  searched.value = true
  try {
    const res = await semanticSearch(query.value.trim())
    results.value = res.items || []
    if (res.source === 'web') {
      ElMessage.info('本地知识库无匹配结果，已自动联网搜索')
    }
  } catch (e) {
    results.value = []
  } finally {
    searching.value = false
  }
}
</script>

<style scoped>
.result-item {
  border-left: 3px solid #1890ff;
  padding: 12px 16px;
  margin: 12px 0;
  background: #fafafa;
  border-radius: 4px;
}
.result-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.result-content { color: #666; margin: 4px 0; }
.result-meta { font-size: 12px; color: #999; display: flex; align-items: center; gap: 8px; }
</style>
