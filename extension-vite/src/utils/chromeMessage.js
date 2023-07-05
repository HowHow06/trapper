/**
 * will trigger the onMessage
 * @param message
 * @param callback
 */
export function sendCurrentTabMessagePromise(message) {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const tabId = tabs[0].id
      chrome.tabs.sendMessage(tabId, message, (response) => {
        if (response.complete) {
          resolve()
        } else {
          reject('Something wrong')
        }
      })
    })
  })
}

/**
 *  发送消息给background
 * @param message
 * @param callback
 */
export function sendRuntimeMessagePromise(message) {
  return new Promise((resolve, reject) => {
    chrome.runtime.sendMessage(message, function (response) {
      if (response.complete) {
        resolve()
      } else {
        reject('Something wrong')
      }
    })
  })
}
