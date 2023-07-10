import { Box, Container, Stack, Typography } from '@mui/material';
import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';
import api from 'src/api';
import CommonTable from 'src/components/common/common-table';
import { DashboardLayout } from 'src/layouts/dashboard/dashboard-layout';
import { isApiSuccess } from 'src/utils/api-call';

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
    name: 'Requests',
    accessor: 'scan_request_count',
  },
  {
    name: 'Vulnerabilities',
    accessor: 'result_count',
  },
  {
    name: 'Created At',
    accessor: 'created_at',
    type: 'datetime',
  },
  {
    name: 'Stopped At',
    accessor: 'stopped_at',
    type: 'datetime',
  },
];

const Page = () => {
  const ignore = useRef(false);
  const [isLoading, setIsLoading] = useState(true);
  const [shouldRefresh, setShouldRefresh] = useState(false);
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const initialize = async () => {
      const fetchTasks = async () => {
        const response = await api.getTasks({ sortBy: 'created_at', isDescOrder: true });
        if (response && isApiSuccess(response)) {
          const tasks = response.data;
          setTasks(tasks);
        }
      };

      if (ignore.current) {
        return;
      }
      ignore.current = true;

      await Promise.all([fetchTasks()]);

      setIsLoading(false);
    };

    initialize();
  }, [shouldRefresh]);

  return (
    <>
      <Head>
        <title>Tasks | Trapper Console</title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
        }}
      >
        <Container maxWidth="xl">
          <Stack spacing={3}>
            <Stack direction="row" justifyContent="space-between" spacing={4}>
              <Stack spacing={1}>
                <Typography variant="h4">Tasks</Typography>
              </Stack>
            </Stack>
            {/* <CustomersSearch /> */}
            <CommonTable
              columns={columns}
              data={tasks}
              itemHref={`/tasks`}
              identity="id"
              isLoading={isLoading}
            />
          </Stack>
        </Container>
      </Box>
    </>
  );
};

Page.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Page;
