import { apiCall } from '../utils/api-call'

export default function ScanRequest(api) {
  const createScanRequest = async ({ taskId, requestData, accessKey }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${taskId}/scan-request`,
      params: {
        original_request_data: requestData,
        task_access_key: accessKey,
      },
    })
  }

  return {
    createScanRequest,
  }
}
