import { Box, Button, Stack, TextField, Typography } from '@mui/material';
import { useFormik } from 'formik';
import Head from 'next/head';
import { useRouter } from 'next/router'; // It should be `next/router`
import { useEffect } from 'react';
import { passwordSchema } from 'src/constants/yup-schema';
import { useAuth } from 'src/hooks/use-auth';
import { Layout as AuthLayout } from 'src/layouts/auth/layout';
import Swal from 'sweetalert2';
import * as Yup from 'yup';

const ResetPasswordPage = () => {
  const router = useRouter();
  const auth = useAuth();
  const { token } = router.query;

  useEffect(() => {
    if (!router.isReady) {
      return;
    }

    if (!token) {
      Swal.fire({
        icon: 'error',
        title: 'Invalid reset link',
        text: 'The password reset link is invalid or has expired.',
      }).then(() => {
        router.push('/auth/login');
      });
    }
  }, [token, router.isReady]);

  const formik = useFormik({
    initialValues: {
      password: '',
      passwordConfirmation: '',
      submit: null,
    },
    validationSchema: Yup.object({
      password: passwordSchema,
      passwordConfirmation: Yup.string()
        .oneOf([Yup.ref('password'), null], 'Passwords must match')
        .required('Password confirmation is required'),
    }),
    onSubmit: async (values, helpers) => {
      try {
        // assuming you have a function `resetPassword` in your auth hook
        await auth.resetPassword(token, values.password);
        Swal.fire({
          icon: 'success',
          title: 'Password Reset Successful',
          text: 'You can now login with your new password.',
        }).then(() => {
          router.push('/auth/login');
        });
      } catch (err) {
        helpers.setStatus({ success: false });
        helpers.setErrors({ submit: err.message });
        helpers.setSubmitting(false);
      }
    },
  });

  return (
    <AuthLayout>
      <Head>
        <title>Reset Password</title>
      </Head>

      <Box
        sx={{
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
              <Typography variant="h4">Reset Password</Typography>
            </Stack>
            <form onSubmit={formik.handleSubmit}>
              <Stack spacing={3}>
                <TextField
                  error={Boolean(formik.touched.password && formik.errors.password)}
                  fullWidth
                  helperText={formik.touched.password && formik.errors.password}
                  label="New Password"
                  name="password"
                  onBlur={formik.handleBlur}
                  onChange={formik.handleChange}
                  type="password"
                  value={formik.values.password}
                />
                <TextField
                  error={Boolean(
                    formik.touched.passwordConfirmation && formik.errors.passwordConfirmation
                  )}
                  fullWidth
                  helperText={
                    formik.touched.passwordConfirmation && formik.errors.passwordConfirmation
                  }
                  label="Confirm New Password"
                  name="passwordConfirmation"
                  onBlur={formik.handleBlur}
                  onChange={formik.handleChange}
                  type="password"
                  value={formik.values.passwordConfirmation}
                />
                {formik.errors.submit && (
                  <Box my={2}>
                    <Typography variant="body2" color="error">
                      {formik.errors.submit}
                    </Typography>
                  </Box>
                )}
                <Button
                  color="primary"
                  fullWidth
                  size="large"
                  type="submit"
                  variant="contained"
                  disabled={formik.isSubmitting}
                >
                  {formik.isSubmitting ? 'Submitting...' : 'Reset Password'}
                </Button>
              </Stack>
            </form>
          </div>
        </Box>
      </Box>
    </AuthLayout>
  );
};

export default ResetPasswordPage;
