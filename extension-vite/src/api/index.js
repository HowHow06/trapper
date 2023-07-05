import axios from 'axios'

import constants from '../core/constants'
import Task from './task'

export const axiosInstance = axios.create({
  baseURL: constants.API_ENDPOINT,
  headers: {},
  withCredentials: true,
})

export const api = {
  ...Task(axiosInstance),
}

export default api
