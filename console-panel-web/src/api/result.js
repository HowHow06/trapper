import { apiCall } from '../utils/api-call';

export default function Result(api) {
  const getResults = async ({ skip, limit, sortBy, isDescOrder }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/results`,
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
    getResults,
  };
}
