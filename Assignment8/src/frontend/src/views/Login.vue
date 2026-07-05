<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 style="text-align:center;margin-bottom:24px">⚡ XU-News-AI-RAG 登录</h2>
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width:100%" @click="handleLogin" :loading="loading">登 录</el-button>
        </el-form-item>
      </el-form>
      <div style="text-align:center">
        <el-button link type="primary" @click="showRegister = true">没有账号？立即注册</el-button>
      </div>
    </el-card>

    <el-dialog v-model="showRegister" title="用户注册" width="400px">
      <el-form :model="regForm" :rules="regRules" ref="regFormRef">
        <el-form-item prop="username">
          <el-input v-model="regForm.username" placeholder="用户名" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="regForm.password" type="password" placeholder="密码" show-password />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="regForm.email" placeholder="邮箱（选填）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width:100%" @click="handleRegister" :loading="regLoading">注 册</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const showRegister = ref(false)
const formRef = ref(null)
const regFormRef = ref(null)

const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const regForm = reactive({ username: '', password: '', email: '' })
const regRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, min: 6, message: '密码至少6位', trigger: 'blur' }]
}
const regLoading = ref(false)

const handleLogin = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await userStore.login({ username: form.username, password: form.password })
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (e) {
    // error handled by interceptor
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  const valid = await regFormRef.value.validate().catch(() => false)
  if (!valid) return
  regLoading.value = true
  try {
    await userStore.register({ username: regForm.username, password: regForm.password, email: regForm.email })
    ElMessage.success('注册成功，请登录')
    showRegister.value = false
  } catch (e) {
    // handled
  } finally {
    regLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 400px;
  padding: 20px;
}
</style>
