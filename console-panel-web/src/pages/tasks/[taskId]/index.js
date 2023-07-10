import { Box, Container, Stack, Typography } from '@mui/material';
import { groupBy, isEmpty } from 'lodash';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useEffect, useRef, useState } from 'react';
import api from 'src/api';
import CommonTable from 'src/components/common/common-table';
import InfoList from 'src/components/common/info-list';
import { DashboardLayout } from 'src/layouts/dashboard/dashboard-layout';
import { isApiSuccess } from 'src/utils/api-call';

const taskInfoColumns = [
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
  const [task, setTask] = useState({});
  const [results, setResults] = useState([]);
  const [vulnerabilites, setVulnerabilites] = useState({});
  const router = useRouter();
  const [isInvalidId, setIsInvalidId] = useState(false);
  const { taskId } = router.query;

  useEffect(() => {
    const initialize = async () => {
      const fetchTask = async () => {
        const response = await api.getTask({ taskId: taskId });
        if (response && isApiSuccess(response)) {
          const task = response.data;
          setTask(task);
          return;
        }
        setIsInvalidId(true);
        return;
      };

      const fetchResults = async () => {
        const response = await api.getResultsByTask({ taskId: taskId });
        if (response && isApiSuccess(response)) {
          const results = response.data;
          setResults(results);
          return;
        }
        return;
      };
      const fetchVulnerabilities = async () => {
        const response = await api.getVulnerabilities({});
        if (response && isApiSuccess(response)) {
          let vulnerabilites = response.data;
          vulnerabilites = groupBy(vulnerabilites, 'id');
          setVulnerabilites(vulnerabilites);
          return;
        }
        return;
      };

      if (ignore.current) {
        return;
      }
      ignore.current = true;

      await Promise.all([fetchTask(), fetchResults(), fetchVulnerabilities()]);

      setIsLoading(false);
    };

    initialize();
  }, [shouldRefresh]);

  const resultsColumns = [
    {
      name: 'Request Endpoint',
      accessor: 'scan_request.request_endpoint',
    },
    {
      name: 'Payload',
      accessor: (data) => {
        const payload = data.payload;
        return payload.replace(/\033\[\d+m/g, ''); // remove color code for terminal
      },
    },
    {
      name: 'Vulnerability Type',
      accessor: (data) => {
        if (isEmpty(vulnerabilites)) {
          return '-';
        }
        const vulnerability_id = data.vulnerability_id;
        return vulnerabilites[vulnerability_id]?.[0]?.name || '-';
      },
    },
    // {
    //   name: 'Patch Suggestion',
    //   accessor: (data) => {
    //     if (isEmpty(vulnerabilites)) {
    //       return '-';
    //     }
    //     const vulnerability_id = data.vulnerability_id;
    //     return vulnerabilites[vulnerability_id]?.[0]?.patch_suggestion || '-';
    //   },
    // },
  ];

  if (isInvalidId) {
    router.push('/404');
  }

  return (
    <>
      <Head>
        <title>View Task | Trapper Console</title>
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
                <Typography variant="h4">Tasks: {taskId}</Typography>
              </Stack>
            </Stack>
            <Box sx={{ mt: 3 }}>
              <InfoList data={task} columns={taskInfoColumns} />
            </Box>

            {/* Groups Section */}
            <Box sx={{ mt: 3 }}>
              <Stack spacing={1}>
                <Typography variant="h5">Vulnerabilities Detected: </Typography>
              </Stack>
              <Box sx={{ mt: 3 }}>
                <CommonTable
                  columns={resultsColumns}
                  data={results}
                  // itemHref={`/communities/${communityId}/groups`}
                  identity="id"
                />
              </Box>
            </Box>
          </Stack>
        </Container>
      </Box>
    </>
  );
};

Page.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Page;
