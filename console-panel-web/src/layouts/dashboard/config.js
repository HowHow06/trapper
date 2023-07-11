import ArrowLeftOnRectangleIcon from '@heroicons/react/24/solid/ArrowLeftOnRectangleIcon';
import ChartBarIcon from '@heroicons/react/24/solid/ChartBarIcon';
import RectangleStackIcon from '@heroicons/react/24/solid/RectangleStackIcon';
import UserIcon from '@heroicons/react/24/solid/UserIcon';
import { SvgIcon } from '@mui/material';

export const items = [
  {
    title: 'Dashboard',
    path: '/',
    icon: (
      <SvgIcon fontSize="small">
        <ChartBarIcon />
      </SvgIcon>
    ),
  },
  {
    title: 'Tasks',
    path: '/tasks',
    icon: (
      <SvgIcon fontSize="small">
        <RectangleStackIcon />
      </SvgIcon>
    ),
  },
  {
    title: 'Account',
    path: '/account',
    icon: (
      <SvgIcon fontSize="small">
        <UserIcon />
      </SvgIcon>
    ),
  },
  {
    title: 'Logout',
    icon: (
      <SvgIcon fontSize="small">
        <ArrowLeftOnRectangleIcon />
      </SvgIcon>
    ),
    action: ({ router, auth }) => {
      auth.signOut();
      router.push('/auth/login');
    },
  },
];
