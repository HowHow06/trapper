import { Box, Button, Link, Stack, TextField, Typography } from '@mui/material';
import { useFormik } from 'formik';
import Head from 'next/head';
import NextLink from 'next/link';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { useAuth } from 'src/hooks/use-auth';
import { Layout as AuthLayout } from 'src/layouts/auth/layout';
import { getErrorMessageFromResponse } from 'src/utils/api-call';
import * as Yup from 'yup';

const Page = () => {
  const router = useRouter();
  const auth = useAuth();
  const [method, setMethod] = useState('username');
  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
      submit: null,
    },
    validationSchema: Yup.object({
      username: Yup.string().max(255).required('Username is required'),
      password: Yup.string().max(255).required('Password is required'),
    }),
    onSubmit: async (values, helpers) => {
      try {
        const response = await auth.signIn(values.username, values.password);
        if (!response.success) {
          helpers.setStatus({ success: false });
          helpers.setErrors({ submit: getErrorMessageFromResponse(response) });
          helpers.setSubmitting(false);
          return;
        }
        const continueUrl = router.query.continueUrl || '/';
        const partition = continueUrl.split('[');
        // window.location.href = partition[0];
        router.push(partition[0]);
      } catch (err) {
        helpers.setStatus({ success: false });
        helpers.setErrors({ submit: err.message });
        helpers.setSubmitting(false);
      }
    },
  });

  const authCheck = () => {
    const { isAuthenticated } = auth;
    if (isAuthenticated) {
      const continueUrl = router.query.continueUrl || '/';
      const partition = continueUrl.split('[');
      router.push(partition[0]);
    }
  };

  useEffect(() => {
    authCheck();
  }, []);

  return (
    <>
      <Head>
        <title>Login | Devias Kit</title>
      </Head>
      <Box
        sx={{
          backgroundColor: 'background.paper',
          flex: '1 1 auto',
          alignItems: 'center',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <Box
          sx={{
            maxWidth: 550,
            px: 3,
            py: '100px',
            width: '100%',
          }}
        >
          <div>
            <Stack spacing={1} sx={{ mb: 3 }}>
              <Typography variant="h4">Login</Typography>
              <Typography color="text.secondary" variant="body2">
                Don&apos;t have an account? &nbsp;
                <Link
                  component={NextLink}
                  href="/auth/register"
                  underline="hover"
                  variant="subtitle2"
                >
                  Register
                </Link>
              </Typography>
            </Stack>
            {/* <Tabs onChange={handleMethodChange} sx={{ mb: 3 }} value={method}>
              <Tab label="Username" value="username" />
              <Tab label="Phone Number" value="phoneNumber" />
            </Tabs> */}
            {method === 'username' && (
              <form noValidate onSubmit={formik.handleSubmit}>
                <Stack spacing={3}>
                  <TextField
                    error={!!(formik.touched.username && formik.errors.username)}
                    fullWidth
                    helperText={formik.touched.username && formik.errors.username}
                    label="Username Address"
                    name="username"
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    type="username"
                    value={formik.values.username}
                  />
                  <TextField
                    error={!!(formik.touched.password && formik.errors.password)}
                    fullWidth
                    helperText={formik.touched.password && formik.errors.password}
                    label="Password"
                    name="password"
                    onBlur={formik.handleBlur}
                    onChange={formik.handleChange}
                    type="password"
                    value={formik.values.password}
                  />
                </Stack>
                {/* <FormHelperText sx={{ mt: 1 }}>Optionally you can skip.</FormHelperText> */}
                {formik.errors.submit && (
                  <Typography color="error" sx={{ mt: 3 }} variant="body2">
                    {formik.errors.submit}
                  </Typography>
                )}
                <Button fullWidth size="large" sx={{ mt: 3 }} type="submit" variant="contained">
                  Continue
                </Button>
                {/* <Button fullWidth size="large" sx={{ mt: 3 }} onClick={handleSkip}>
                  Skip authentication
                </Button> */}
              </form>
            )}
          </div>
        </Box>
      </Box>
    </>
  );
};

Page.getLayout = (page) => <AuthLayout>{page}</AuthLayout>;

export default Page;
