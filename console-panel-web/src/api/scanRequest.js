import { apiCall } from '../utils/api-call';

export default function ScanRequest(api) {
  const createScanRequest = async ({ taskId, requestData, accessKey }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${taskId}/scan-requests`,
      params: {
        original_request_data: requestData,
        task_access_key: accessKey,
      },
    });
  };

  const getScanRequests = async ({ skip, limit, sortBy, isDescOrder }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/scan-requests`,
      method: `get`,
      params: {
        skip,
        limit,
        sort_by: sortBy,
        desc_order: isDescOrder,
      },
    });
  };

  return {
    createScanRequest,
    getScanRequests,
  };
}
