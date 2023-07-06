import axios from 'axios'

import constants from '../core/constants'
import Auth from './auth'
import ScanRequest from './scanRequest'
import Task from './task'

export const axiosInstance = axios.create({
  baseURL: constants.API_ENDPOINT,
  headers: {},
  withCredentials: true,
})

export const api = {
  ...Task(axiosInstance),
  ...Auth(axiosInstance),
  ...ScanRequest(axiosInstance),
}

export default api
