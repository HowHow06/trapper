import { apiCall } from '../utils/api-call'

export default function Task(api) {
  const createTask = async ({ taskName, urlRule }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks`,
      params: {
        task_name: taskName,
        url_rule: urlRule,
      },
    })
  }

  const updateTask = async ({ id, taskName, urlRule }) => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/${id}`,
      method: `put`,
      params: {
        task_name: taskName,
        url_rule: urlRule,
      },
    })
  }

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
    })
  }

  const getCurrentTask = async () => {
    return await apiCall({
      axiosInstance: api,
      url: `/tasks/current`,
      method: `get`,
    })
  }

  return {
    createTask,
    updateTask,
    getTasks,
    getCurrentTask,
  }
}
