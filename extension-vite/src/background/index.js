import constants from '../core/constants'
import { clearAllStorageData } from '../utils/chromeStorage'
import { MyObject } from './myObject'

console.info('Trapper Client Background Loaded>>')
const { TASK_STATUS, API_ENDPOINT, MESSAGE_ACTION_NAME: ACTION_NAME } = constants
let requests = new MyObject()
let currentTask = {}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  onMessageListenerEvent(request, sender, sendResponse)
  // return true to indicate you want to send a response asynchronously
  return true
})

/**
 * runtime onMessage listener
 */
async function onMessageListenerEvent(request, sender, sendResponse) {
  if (request.actionName == ACTION_NAME.START_TASK && request.task && request.task.id) {
    console.log('Start task action')
    startListeningRequests(request.task)
  } else if (request.actionName == ACTION_NAME.STOP_TASK) {
    console.log('Stop task action')
    currentTask = {}
    removeAllListeners()
  }
  sendResponse('') // not meaningful because our message does not need a response
}

async function startListeningRequests(task) {
  removeAllListeners()
  // const task = await getTaskFromStorage()
  // console.log('Task from storage', task)
  currentTask = task
  addRequestHookListeners()
}

async function HookonBeforeRequest(details) {
  const task = currentTask
  console.log(`Hook on before req: ${details.requestId}, ${task.id}`)
  if (!task.id) {
    return
  }

  if (task.taskStatusId != TASK_STATUS.RUNNING) {
    return
  }

  const urlRuleRegex = task.urlRule.toString().replace(new RegExp('\\*', 'g'), '(.*)') //replace * with (.*)
  const regExp = new RegExp(urlRuleRegex.toString())
  // avoid scanning backend api endpoint
  if (regExp.test(details.url) && details.url.indexOf(`${API_ENDPOINT}`) == -1) {
    console.log('matched req!: ', details.requestId)
    const requestInfo = getAnalysedRequestInformation(details)
    const req = {
      requestid: details.requestId,
      type: details.type,
      url: details.url,
      method: details.method.toLowerCase(),
      data: JSON.stringify(requestInfo.data),
      data_type: requestInfo.dataType,
      parser: 'chrome-plugin',
    }

    if (!requests.hasKey(details.requestId)) {
      requests.put(details.requestId, req)
      // console.log('Request put into requests:', requests.getObject()[details.requestId])
    }
  }
}

async function HookonBeforeSendHeaders(details) {
  const task = currentTask
  console.log(`Hook on before header: ${details.requestId}, ${task.id}`)
  if (!task.id) {
    return
  }

  if (task.taskStatusId != TASK_STATUS.RUNNING) {
    return
  }

  const urlRuleRegex = task.urlRule.toString().replace(new RegExp('\\*', 'g'), '(.*)')
  const regExp = new RegExp(urlRuleRegex.toString())
  // avoid scanning backend api endpoint
  if (regExp.test(details.url) && details.url.indexOf(`${API_ENDPOINT}`) == -1) {
    console.log('matched header!: ', details.requestId)
    const requestid = details.requestId

    const requestData = requests.get(requestid)
    if (requestData) {
      requestData.headers = JSON.stringify(getHeaders(details))
      await createScanRequest({ urlData: requestData, taskId: task.id, accessKey: task.accessKey })
      requests.delete(requestid)
    }
  }
}

/**
 * add listener
 */
function addRequestHookListeners() {
  chrome.webRequest.onBeforeRequest.addListener(HookonBeforeRequest, { urls: ['<all_urls>'] }, [
    'requestBody',
  ])
  chrome.webRequest.onBeforeSendHeaders.addListener(
    HookonBeforeSendHeaders,
    { urls: ['<all_urls>'] },
    ['requestHeaders', 'extraHeaders'],
  )
}

/***
 * remove listener
 */
function removeAllListeners() {
  chrome.webRequest.onBeforeRequest.removeListener(HookonBeforeRequest)
  chrome.webRequest.onBeforeSendHeaders.removeListener(HookonBeforeSendHeaders)
}

/**
 * return http header, Content-Type尽量原格式, 有时候会变成 Content-type
 * @param details
 * @returns {*}
 */
function getHeaders(details) {
  let result = {}
  if (details.requestHeaders != undefined) {
    details.requestHeaders.forEach(function (item, index) {
      if (item.name.toLowerCase() == 'content-type') {
        result['content-type'] = item.value
      } else {
        result[item.name] = item.value
      }
    })
    return result
  }
  return undefined
}

/**
 * return http request information
 * @param details
 * @returns {*}
 */
function getAnalysedRequestInformation(details) {
  let result = {}
  const requestBody = details.requestBody
  if (requestBody != undefined) {
    try {
      data = decodeURIComponent(
        String.fromCharCode.apply(null, new Uint8Array(requestBody.raw[0].bytes)),
      )
      return { data: data, dataType: 'raw' }
    } catch (e) {
      // meaning is a form data
      if (e instanceof TypeError) {
        for (let key in requestBody.formData) {
          requestBody.formData[key].forEach(function (value, index) {
            result[key] = value
          })
        }
      }
      return { data: result, dataType: 'form_data' }
    }
  }
  return { data: undefined, dataType: undefined }
}

/***
 * send the request to backend for scanning, the access key is neccessary, to verify that the task is valid
 */
async function createScanRequest({ urlData, taskId, accessKey }) {
  // using fetch here because axios is not usable in service worker
  console.log('Sending create scan request to fastapi with data: ', urlData)
  const url = `${constants.API_ENDPOINT}/tasks/${taskId}/scan-requests`
  const params = {
    original_request_data: urlData,
    task_access_key: accessKey,
  }

  const options = {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  }

  let response
  try {
    response = await fetch(url, options)
    if (!response.ok) {
      throw new Error('Network response was not ok')
    }
  } catch (error) {
    console.log('Error when creating scan request:', error)
    clearAllStorageData()
    removeAllListeners()
    return
  }

  const data = await response.json()
  console.log('Scan request created: ', data)
}
