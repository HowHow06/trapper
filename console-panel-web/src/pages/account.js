import { Box, Container, Unstable_Grid2 as Grid, Stack, Typography } from '@mui/material';
import Head from 'next/head';
import { useAuth } from 'src/hooks/use-auth';
import { DashboardLayout } from 'src/layouts/dashboard/dashboard-layout';
import { AccountPassword } from 'src/sections/account/account-password';
import { AccountProfile } from 'src/sections/account/account-profile';

const Page = (props) => {
  const auth = useAuth();

  return (
    <>
      <Head>
        <title>Account | Trapper Console</title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
        }}
      >
        <Container maxWidth="lg">
          <Stack spacing={3}>
            <div>
              <Typography variant="h4">Account</Typography>
            </div>
            <div>
              <Grid container spacing={3}>
                <Grid xs={12} md={6} lg={4}>
                  <AccountProfile user={auth.user} />
                </Grid>
                <Grid xs={12} md={6} lg={8}>
                  <AccountPassword />
                </Grid>
              </Grid>
            </div>
          </Stack>
        </Container>
      </Box>
    </>
  );
};

Page.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Page;
