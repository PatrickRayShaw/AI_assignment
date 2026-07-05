<template>
  <div>
    <el-card>
      <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px;align-items:center">
        <el-input v-model="filters.keyword" placeholder="搜索标题..." style="width:200px" clearable />
        <el-select v-model="filters.source_type" placeholder="全部类型" style="width:120px" clearable>
          <el-option label="RSS" value="rss" />
          <el-option label="网页" value="web" />
          <el-option label="手动上传" value="manual" />
        </el-select>
        <el-select v-model="filters.time" placeholder="全部时间" style="width:120px" clearable>
          <el-option label="今天" value="today" />
          <el-option label="本周" value="week" />
          <el-option label="本月" value="month" />
        </el-select>
        <el-button type="primary" @click="search">🔍 筛选</el-button>
        <el-button @click="dialogVisible = true">📤 上传数据</el-button>
        <el-button type="danger" :disabled="selectedIds.length===0" @click="batchDelete">🗑 批量删除</el-button>
      </div>
      <el-table :data="newsList" @selection-change="handleSelectionChange" v-loading="loading">
        <el-table-column type="selection" width="40" />
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="source_type" label="类型" width="80" />
        <el-table-column prop="source" label="来源" width="120" />
        <el-table-column label="标签" width="200">
          <template #default="{ row }">
            <el-tag v-for="tag in (row.tags || [])" :key="tag" size="small" style="margin-right:4px">{{ tag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160" />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="editNews(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteOne(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        style="margin-top:16px;justify-content:flex-end"
        v-model:current-page="pagination.page"
        :page-size="pagination.per_page"
        :total="pagination.total"
        layout="total, prev, pager, next"
        @current-change="loadData"
      />
    </el-card>

    <el-dialog v-model="dialogVisible" title="上传数据" width="500px">
      <el-form :model="form">
        <el-form-item label="标题">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="form.content" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="form.source" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.source_type">
            <el-option label="手动上传" value="manual" />
            <el-option label="网页" value="web" />
            <el-option label="RSS" value="rss" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签（逗号分隔）">
          <el-input v-model="form.tagsStr" placeholder="AI, 科技" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUpload">上传并入库</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="editVisible" title="编辑新闻" width="500px">
      <el-form :model="editForm">
        <el-form-item label="标题">
          <el-input v-model="editForm.title" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="editForm.content" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="editForm.source" />
        </el-form-item>
        <el-form-item label="标签（逗号分隔）">
          <el-input v-model="editForm.tagsStr" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" @click="saveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getNewsList, deleteNews, batchDeleteNews, createNews, updateNews } from '@/api/knowledge'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const newsList = ref([])
const selectedIds = ref([])
const dialogVisible = ref(false)
const editVisible = ref(false)
const filters = reactive({ keyword: '', source_type: '', time: '' })
const pagination = reactive({ page: 1, per_page: 20, total: 0 })
const form = reactive({ title: '', content: '', source: 'manual', source_type: 'manual', tagsStr: '' })
const editForm = reactive({ id: null, title: '', content: '', source: '', tagsStr: '' })

const loadData = async () => {
  loading.value = true
  try {
    const res = await getNewsList({ page: pagination.page, per_page: pagination.per_page, keyword: filters.keyword, source_type: filters.source_type })
    newsList.value = res.data
    pagination.total = res.total
  } finally {
    loading.value = false
  }
}

const search = () => {
  pagination.page = 1
  loadData()
}

const handleSelectionChange = (val) => {
  selectedIds.value = val.map(v => v.id)
}

const deleteOne = async (id) => {
  await ElMessageBox.confirm('确定删除该新闻？', '提示', { type: 'warning' })
  await deleteNews(id)
  ElMessage.success('删除成功')
  loadData()
}

const batchDelete = async () => {
  await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条新闻？`, '批量删除', { type: 'warning' })
  await batchDeleteNews(selectedIds.value)
  ElMessage.success('批量删除成功')
  loadData()
}

const submitUpload = async () => {
  if (!form.title) {
    ElMessage.warning('标题不能为空')
    return
  }
  const tags = form.tagsStr.split(',').map(t => t.trim()).filter(Boolean)
  await createNews({ title: form.title, content: form.content, source: form.source, source_type: form.source_type, tags })
  ElMessage.success('上传成功')
  dialogVisible.value = false
  Object.assign(form, { title: '', content: '', source: 'manual', source_type: 'manual', tagsStr: '' })
  loadData()
}

const editNews = (row) => {
  editForm.id = row.id
  editForm.title = row.title
  editForm.content = row.content || ''
  editForm.source = row.source || ''
  editForm.tagsStr = (row.tags || []).join(', ')
  editVisible.value = true
}

const saveEdit = async () => {
  const tags = editForm.tagsStr.split(',').map(t => t.trim()).filter(Boolean)
  await updateNews(editForm.id, { title: editForm.title, content: editForm.content, source: editForm.source, tags })
  ElMessage.success('更新成功')
  editVisible.value = false
  loadData()
}

onMounted(loadData)
</script>
