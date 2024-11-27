<template>
  <div class="register-container">
    <h1>User Registration</h1>
    <form @submit.prevent="handleSubmit" class="register-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="formData.username" @blur="validateUsername" />
        <span class="error-message" v-if="errors.username">{{ errors.username }}</span>
      </div>

      <div class="form-group">
        <label for="email">mail:</label>
        <input type="email" id="email" v-model="formData.email" @blur="validateEmail" />
        <span class="error-message" v-if="errors.email">{{ errors.email }}</span>
      </div>

      <div class="form-group">
        <label for="password">password:</label>
        <input type="password" id="password" v-model="formData.password" @blur="validatePassword" />
        <span class="error-message" v-if="errors.password">{{ errors.password }}</span>
      </div>

      <div class="form-group">
        <label for="confirmPassword">confirm password:</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="formData.confirmPassword"
          @blur="validateConfirmPassword"
        />
        <span class="error-message" v-if="errors.confirmPassword">{{
          errors.confirmPassword
        }}</span>
      </div>

      <button type="submit" :disabled="!isFormValid">注册</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      formData: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
      errors: {
        username: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
    }
  },
  computed: {
    isFormValid() {
      return (
        this.formData.username &&
        this.formData.email &&
        this.formData.password &&
        this.formData.confirmPassword &&
        Object.values(this.errors).every((error) => !error)
      )
    },
  },
  methods: {
    validateUsername() {
      if (!this.formData.username) {
        this.errors.username = "Username can't be empty"
      } else if (this.formData.username.length < 3) {
        this.errors.username = 'Username at least 3 characters'
      } else {
        this.errors.username = ''
      }
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!this.formData.email) {
        this.errors.email = "the mail can't be empty"
      } else if (!emailRegex.test(this.formData.email)) {
        this.errors.email = 'Please input valid mail'
      } else {
        this.errors.email = ''
      }
    },
    validatePassword() {
      if (!this.formData.password) {
        this.errors.password = "the password can't be empty"
      } else if (this.formData.password.length < 6) {
        this.errors.password = 'Passwor at least 6 character'
      } else {
        this.errors.password = ''
      }
      if (this.formData.confirmPassword) {
        this.validateConfirmPassword()
      }
    },
    validateConfirmPassword() {
      if (!this.formData.confirmPassword) {
        this.errors.confirmPassword = 'Please confirm password'
      } else if (this.formData.password !== this.formData.confirmPassword) {
        this.errors.confirmPassword = ' Not match'
      } else {
        this.errors.confirmPassword = ''
      }
    },
    async handleSubmit() {
      // 验证所有字段
      this.validateUsername()
      this.validateEmail()
      this.validatePassword()
      this.validateConfirmPassword()

      if (this.isFormValid) {
        try {
          // 这里添加实际的注册逻辑
          console.log('注册表单提交:', this.formData)
          // 例如调用 API:
          // await this.$axios.post('/api/register', this.formData)
          // 注册成功后重定向
          // this.$router.push('/login')
        } catch (error) {
          console.error('registration false:', error)
        }
      }
    },
  },
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-weight: bold;
  color: #555;
}

input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus {
  outline: none;
  border-color: #4caf50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.2);
}

.error-message {
  color: #f44336;
  font-size: 14px;
}

button {
  padding: 12px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>
