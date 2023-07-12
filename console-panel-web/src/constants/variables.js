export const DEFAULT = {
  AVATAR: '/assets/avatars/avatar-default-03.jpg',
};

export const TASK_STATUS = {
  WAITING: 1,
  RUNNING: 2,
  DONE: 3,
  KILLED: 4,
  PAUSED: 9,
};
export const TASK_STATUS_NAME = {
  1: 'Created',
  2: 'Running',
  3: 'Completed',
  4: 'Stopping',
  9: 'Paused',
};
export const VULNERABILITY_TYPE = {
  REFLECTED_XSS: 1,
  STORED_XSS: 2,
  DOM_XSS: 3,
};

export const SEVERITY_COLOR_MAP = {
  5: 'info',
  6: 'warning',
  7: 'error',
};

export const SEVERITY_NAME = {
  5: 'Low',
  6: 'Medium',
  7: 'High',
};
