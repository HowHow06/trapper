export const apiCall = async ({
  axiosInstance,
  url,
  method = 'post',
  params = null,
  options = {},
}) => {
  try {
    let response

    switch (method.toLowerCase()) {
      case 'post':
        response = await axiosInstance.post(url, params, options)
        break
      case 'put':
        response = await axiosInstance.put(url, params, options)
        break
      case 'delete':
        response = await axiosInstance.delete(url, options)
        break
      case 'get':
      default:
        response = await axiosInstance.get(url, { ...options, params })
    }

    return { success: true, ...response }
  } catch (error) {
    return { success: false, error: error }
  }
}

export const isApiSuccess = (response) => {
  return response.status >= 200 && response.status < 300 && response.success
}

export const getErrorMessageFromResponse = (response) => {
  const errorObject = response.error
  return errorObject.response?.data?.detail ?? errorObject.message
}
