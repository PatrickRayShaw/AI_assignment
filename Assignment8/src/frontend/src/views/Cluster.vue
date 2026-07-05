<template>
  <div>
    <el-card>
      <h3>📈 知识库聚类分析报告 — Top10 关键词分布</h3>
      <div v-if="report.keywords && report.keywords.length">
        <el-table :data="report.keywords" style="margin:16px 0">
          <el-table-column prop="rank" label="排名" width="60" />
          <el-table-column prop="keyword" label="关键词" width="150" />
          <el-table-column label="权重/次数" width="120">
            <template #default="{ row }">
              <el-progress :percentage="row.percentage" :stroke-width="12" />
            </template>
          </el-table-column>
          <el-table-column prop="percentage" label="占比(%)" width="100" />
        </el-table>
      </div>
      <div v-else style="text-align:center;padding:40px;color:#999">
        <p v-if="!report.total_news">暂无数据</p>
        <p v-else>点击下方按钮生成分析报告</p>
      </div>
      <div style="text-align:right;margin-top:12px">
        <el-button type="primary" @click="generateReport" :loading="loading">🔄 生成报告</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getClusterReport, analyzeCluster } from '@/api/cluster'
import { ElMessage } from 'element-plus'

const report = ref({ keywords: [], total_news: 0 })
const loading = ref(false)

const loadReport = async () => {
  try {
    const res = await getClusterReport()
    if (!res.error) report.value = res
  } catch (e) {
    // no report yet
  }
}

const generateReport = async () => {
  loading.value = true
  try {
    const res = await analyzeCluster()
    report.value = res
    ElMessage.success('分析报告生成成功')
  } catch (e) {
    // handled
  } finally {
    loading.value = false
  }
}

onMounted(loadReport)
</script>
