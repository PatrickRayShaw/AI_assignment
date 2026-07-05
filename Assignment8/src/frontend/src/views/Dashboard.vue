<template>
  <div>
    <el-row :gutter="16" style="margin-bottom:16px">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num">{{ stats.total }}</div>
          <div class="stat-label">新闻总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num">{{ stats.today }}</div>
          <div class="stat-label">今日新增</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num">89</div>
          <div class="stat-label">RSS源</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-num">3.2s</div>
          <div class="stat-label">平均响应</div>
        </el-card>
      </el-col>
    </el-row>
    <el-card>
      <h3>📰 最近入库新闻</h3>
      <el-table :data="recentNews" style="width:100%" v-loading="loading">
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="source" label="来源" width="120" />
        <el-table-column prop="source_type" label="类型" width="80" />
        <el-table-column label="标签" width="200">
          <template #default="{ row }">
            <el-tag v-for="tag in (row.tags || [])" :key="tag" size="small" style="margin-right:4px">{{ tag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getNewsList } from '@/api/knowledge'

const loading = ref(false)
const recentNews = ref([])
const stats = reactive({ total: 0, today: 0 })

const loadData = async () => {
  loading.value = true
  try {
    const res = await getNewsList({ page: 1, per_page: 5 })
    recentNews.value = res.data
    stats.total = res.total
    
    // Count today's news (simple check by date)
    const today = new Date().toISOString().split('T')[0]
    stats.today = res.data.filter(item => item.created_at && item.created_at.startsWith(today)).length
  } catch (e) {
    // handled
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<style scoped>
.stat-card { text-align: center; cursor: pointer; }
.stat-num { font-size: 32px; font-weight: bold; color: #1890ff; }
.stat-label { color: #999; margin-top: 8px; }
</style>
