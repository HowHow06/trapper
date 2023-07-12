import { apiCall } from '../utils/api-call';

export default function Task(api) {
  const createTask = async ({ taskName, urlRule }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks`,
      params: {
        task_name: taskName,
        url_rule: urlRule,
      },
    });
  };

  const updateTask = async ({ id, taskName, urlRule }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${id}`,
      method: `put`,
      params: {
        task_name: taskName,
        url_rule: urlRule,
      },
    });
  };

  const getTasks = async ({ skip, limit, sortBy, isDescOrder }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks`,
      method: `get`,
      params: {
        skip,
        limit,
        sort_by: sortBy,
        desc_order: isDescOrder,
      },
    });
  };

  const getTask = async ({ taskId }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${taskId}`,
      method: `get`,
    });
  };

  const getCurrentTask = async () => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/current`,
      method: `get`,
    });
  };

  const startTask = async ({ id }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${id}/start-task`,
    });
  };

  const stopTask = async ({ id }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${id}/stop-task`,
    });
  };

  const pauseTask = async ({ id }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${id}/pause-task`,
    });
  };

  const getResultsByTask = async ({ taskId }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${taskId}/results`,
      method: 'get',
    });
  };

  return {
    createTask,
    updateTask,
    getTasks,
    getTask,
    getCurrentTask,
    startTask,
    stopTask,
    pauseTask,
    getResultsByTask,
  };
}
