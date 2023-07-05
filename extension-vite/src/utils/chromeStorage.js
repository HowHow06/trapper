import constants from '../core/constants'

/**
 * Store to storage
 * @param field
 * @param value
 */
export function saveDataToStorage(field, value) {
  var data = {}
  data[field] = value
  chrome.storage.local.set(data, function () {
    if (chrome.runtime.error) {
      console.log('Runtime error when saving data.', { field, value })
    }
    console.log('Saved data to storage', {
      field,
      value,
    })
  })
}

/**
 * get from storage
 * @param field
 */
export function getDataFromStorage(field) {
  return new Promise((resolve, reject) => {
    chrome.storage.local.get(field, function (items) {
      if (!chrome.runtime.error) {
        resolve(items[field])
      }
    })
  })
}

export function saveTaskToStorage({ urlRule, taskName, id, accessKey, taskStatusId }) {
  saveDataToStorage(constants.LOCAL_STORAGES_KEYS.URL_RULE, urlRule)
  saveDataToStorage(constants.LOCAL_STORAGES_KEYS.TASK_NAME, taskName)
  saveDataToStorage(constants.LOCAL_STORAGES_KEYS.TASK_ID, id)
  saveDataToStorage(constants.LOCAL_STORAGES_KEYS.TASK_ACCESS_KEY, accessKey)
  saveDataToStorage(constants.LOCAL_STORAGES_KEYS.TASK_STATUS, taskStatusId)
}

export async function getTaskFromStorage() {
  const [urlRule, taskName, id, accessKey, taskStatusId] = await Promise.all([
    getDataFromStorage(constants.LOCAL_STORAGES_KEYS.URL_RULE),
    getDataFromStorage(constants.LOCAL_STORAGES_KEYS.TASK_NAME),
    getDataFromStorage(constants.LOCAL_STORAGES_KEYS.TASK_ID),
    getDataFromStorage(constants.LOCAL_STORAGES_KEYS.TASK_ACCESS_KEY),
    getDataFromStorage(constants.LOCAL_STORAGES_KEYS.TASK_STATUS),
  ])

  return {
    urlRule,
    taskName,
    id,
    accessKey,
    taskStatusId,
  }
}

/**
 * Clear all data from storage
 */
export function clearAllStorageData() {
  chrome.storage.local.clear(function () {
    var error = chrome.runtime.lastError
    if (error) {
      console.error(error)
    } else {
      console.log('All data cleared from storage')
    }
  })
}

/**
 * Remove specific data from storage
 * @param key - Key of the data to remove from storage
 */
export function removeStorageData(key) {
  chrome.storage.local.remove(key, function () {
    var error = chrome.runtime.lastError
    if (error) {
      console.error(error)
    } else {
      console.log('Data removed from storage', key)
    }
  })
}
