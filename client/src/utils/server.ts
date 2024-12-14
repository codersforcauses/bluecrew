import axios from 'axios'

const server = axios.create({ baseURL: import.meta.env.VITE_BACKEND_URL, timeout: 8000 })
export default server
