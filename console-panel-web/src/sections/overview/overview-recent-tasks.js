import ArrowRightIcon from '@heroicons/react/24/solid/ArrowRightIcon';
import { Box, Button, Card, CardActions, CardHeader, Divider, SvgIcon } from '@mui/material';
import { useRouter } from 'next/navigation';
import PropTypes from 'prop-types';
import { Scrollbar } from 'src/components/scrollbar';
import CommonTable from '../../components/common/common-table';

const columns = [
  {
    name: 'Task Name',
    accessor: 'task_name',
  },
  {
    name: 'URL Rule',
    accessor: 'url_rule',
  },
  {
    name: 'Status',
    accessor: 'task_status_id',
    type: 'task_status',
  },
  {
    name: 'Created At',
    accessor: 'created_at',
    type: 'datetime',
  },
];

const OverviewRecentTasks = (props) => {
  const { tasks = [], sx, isLoading = false } = props;
  const router = useRouter();

  return (
    <Card sx={sx}>
      <CardHeader title="Recent Tasks" />
      <Scrollbar sx={{ flexGrow: 1 }}>
        <Box sx={{ minWidth: 800 }}>
          <CommonTable
            columns={columns}
            data={tasks.slice(0, 10)}
            itemHref={`/tasks`}
            identity="id"
            noPagination
            isLoading={isLoading}
            noSearch
          />
        </Box>
      </Scrollbar>
      <Divider />
      <CardActions sx={{ justifyContent: 'flex-end' }}>
        <Button
          color="inherit"
          endIcon={
            <SvgIcon fontSize="small">
              <ArrowRightIcon />
            </SvgIcon>
          }
          size="small"
          variant="text"
          // TODO: navigate to tasks
          onClick={() => {
            router.push('/tasks');
          }}
        >
          View all
        </Button>
      </CardActions>
    </Card>
  );
};

OverviewRecentTasks.prototype = {
  orders: PropTypes.array,
  sx: PropTypes.object,
};

export default OverviewRecentTasks;
