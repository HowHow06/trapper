const TASK_STATUS = {
  WAITING: 1,
  RUNNING: 2,
  DONE: 3,
  KILLED: 4,
}
const TASK_STATUS_NAME = {
  1: 'Created',
  2: 'Running',
  3: 'Completed',
  4: 'Completed',
}
const TIME_OUT_IN_MS = 10 * 1000
const API_ENDPOINT = import.meta.env.VITE_API_URL
const CONSOLE_APP_HOST_NAME = import.meta.env.VITE_CONSOLE_PANEL_URL

// Key in local storage
const LOCAL_STORAGES_KEYS = {
  TASK_STATUS: 'STATUS',
  TASK_ID: 'TASK_ID',
  TASK_ACCESS_KEY: 'TASK_ACCESS_KEY',
  URL_RULE: 'FILTER_SITE',
  // RECEIVER_EMAIL: 'RECEIVER_EMAIL',
  TASK_NAME: 'TASK_NAME',
}

export default {
  TASK_STATUS,
  API_ENDPOINT,
  TIME_OUT_IN_MS,
  CONSOLE_APP_HOST_NAME,
  LOCAL_STORAGES_KEYS,
  TASK_STATUS_NAME,
}
