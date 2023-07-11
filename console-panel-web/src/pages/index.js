import { Box, Container, Unstable_Grid2 as Grid, Typography } from '@mui/material';
import { groupBy } from 'lodash';
import Head from 'next/head';
import { useEffect, useRef, useState } from 'react';
import api from 'src/api';
import { VULNERABILITY_TYPE } from 'src/constants/variables';
import { DashboardLayout } from 'src/layouts/dashboard/dashboard-layout';
import OverviewRecentTasks from 'src/sections/dashboard/overview-recent-tasks';
import OverviewRequestCount from 'src/sections/dashboard/overview-request-count';
import OverviewTaskCount from 'src/sections/dashboard/overview-task-count';
import OverviewVulnerabilityCount from 'src/sections/dashboard/overview-vulnerability-count';
import OverviewVulnerabilityType from 'src/sections/dashboard/overview-vulnerability-type';
import { isApiSuccess } from 'src/utils/api-call';

const Page = () => {
  const ignore = useRef(false);
  const [isLoading, setIsLoading] = useState(true);
  const [shouldRefresh, setShouldRefresh] = useState(false);
  const [tasks, setTasks] = useState([]);
  const [scanRequests, setScanRequests] = useState([]);
  const [results, setResults] = useState([]);

  useEffect(() => {
    const initialize = async () => {
      const fetchTasks = async () => {
        const response = await api.getTasks({ sortBy: 'created_at', isDescOrder: true });
        if (response && isApiSuccess(response)) {
          const tasks = response.data;
          setTasks(tasks);
        }
      };

      const fetchRequests = async () => {
        const response = await api.getScanRequests({});
        if (response && isApiSuccess(response)) {
          const scanRequests = response.data;
          setScanRequests(scanRequests);
        }
      };

      const fetchResults = async () => {
        const response = await api.getResults({});
        if (response && isApiSuccess(response)) {
          const results = response.data;
          setResults(results);
        }
      };

      if (ignore.current) {
        return;
      }

      ignore.current = true;

      await Promise.all([fetchTasks(), fetchRequests(), fetchResults()]);

      setIsLoading(false);
    };

    initialize();
  }, [shouldRefresh]);

  const resultsGroupByType = groupBy(results, 'vulnerability_id');
  const DOMXSSCount = resultsGroupByType[VULNERABILITY_TYPE.DOM_XSS]?.length || 0;
  const reflectedXSSCount = resultsGroupByType[VULNERABILITY_TYPE.REFLECTED_XSS]?.length || 0;
  const storedXSSCount = resultsGroupByType[VULNERABILITY_TYPE.STORED_XSS]?.length || 0;

  return (
    <>
      <Head>
        <title>Dashboard | Trapper Console</title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 3,
        }}
      >
        <Container maxWidth="xl">
          <Typography
            variant="h4"
            sx={{
              mb: 3,
            }}
          >
            Welcome to Trapper Console!
          </Typography>
          <Grid container spacing={3}>
            <Grid xs={12} lg={4}>
              <OverviewTaskCount value={tasks.length} />
            </Grid>
            <Grid xs={12} sm={6} lg={4}>
              <OverviewRequestCount value={scanRequests.length} />
            </Grid>
            <Grid xs={12} sm={6} lg={4}>
              <OverviewVulnerabilityCount value={results.length} />
            </Grid>
            <Grid xs={12} lg={8}>
              <OverviewRecentTasks tasks={tasks} sx={{ height: '100%' }} isLoading={isLoading} />
            </Grid>

            <Grid xs={12} lg={4}>
              <OverviewVulnerabilityType
                data={[DOMXSSCount, reflectedXSSCount, storedXSSCount]}
                isLoading={isLoading}
              />
            </Grid>
          </Grid>
        </Container>
      </Box>
    </>
  );
};

Page.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Page;
