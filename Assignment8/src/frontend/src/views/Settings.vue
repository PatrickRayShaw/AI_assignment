<template>
  <div>
    <el-card>
      <h3>⚙️ n8n 工作流配置</h3>
      <el-table :data="workflows" style="margin-top:16px">
        <el-table-column prop="name" label="工作流名称" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'warning'">{{ row.status === 'active' ? '运行中' : '空闲' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="lastRun" label="上次执行" width="180" />
        <el-table-column label="操作" width="200">
          <template #default>
            <el-button size="small">暂停</el-button>
            <el-button size="small" type="primary">手动触发</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const workflows = ref([
  { name: '新闻采集入库', status: 'active', lastRun: '2026-07-05 19:00' },
  { name: '语义检索', status: 'active', lastRun: '-' },
  { name: '聚类分析', status: 'idle', lastRun: '2026-07-05 12:00' },
  { name: '邮件通知', status: 'active', lastRun: '2026-07-05 18:30' }
])
</script>
