import {
  Button,
  Card,
  CardActions,
  CardContent,
  CardHeader,
  Divider,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { useFormik } from 'formik';
import api from 'src/api';
import { passwordSchema } from 'src/constants/yup-schema';
import { getErrorMessageFromResponse, isApiSuccess } from 'src/utils/api-call';
import Swal from 'sweetalert2';
import * as Yup from 'yup';

export const AccountPassword = () => {
  const formik = useFormik({
    initialValues: {
      originalPassword: '',
      password: '',
      confirm: '',
    },
    validationSchema: Yup.object({
      originalPassword: Yup.string().required('Original Password is required'),
      password: passwordSchema,
      confirm: Yup.string()
        .oneOf([Yup.ref('password'), null], 'Passwords must match')
        .required('Confirm Password is required'),
    }),
    onSubmit: async (values, helpers) => {
      try {
        const response = await api.editPassword({
          oldPassword: values.originalPassword,
          newPassword: values.password,
        });

        if (!isApiSuccess(response)) {
          helpers.setStatus({ success: false });
          helpers.setErrors({ submit: getErrorMessageFromResponse(response) });
          helpers.setSubmitting(false);
          return;
        }
        Swal.fire({
          icon: 'success',
          title: 'Password edited successfully!',
          confirmButtonText: 'OK',
          timer: 1500,
        }).then(() => {
          formik.resetForm();
        });
      } catch (err) {
        helpers.setStatus({ success: false });
        helpers.setErrors({ submit: err.message });
        helpers.setSubmitting(false);
      }
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <Card>
        <CardHeader subheader="Update password" title="Password" />
        <Divider />
        <CardContent>
          <Stack spacing={3} sx={{ maxWidth: 400 }}>
            <TextField
              error={!!(formik.touched.originalPassword && formik.errors.originalPassword)}
              fullWidth
              helperText={formik.touched.originalPassword && formik.errors.originalPassword}
              label="Original Password"
              name="originalPassword"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              type="password"
              value={formik.values.originalPassword}
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
            <TextField
              error={!!(formik.touched.confirm && formik.errors.confirm)}
              fullWidth
              helperText={formik.touched.confirm && formik.errors.confirm}
              label="Password (Confirm)"
              name="confirm"
              onBlur={formik.handleBlur}
              onChange={formik.handleChange}
              type="password"
              value={formik.values.confirm}
            />
            {formik.errors.submit && (
              <Typography color="error" sx={{ mt: 3 }} variant="body2">
                {formik.errors.submit}
              </Typography>
            )}
          </Stack>
        </CardContent>
        <Divider />

        <CardActions sx={{ justifyContent: 'flex-end' }}>
          <Button variant="contained" type="submit" disabled={formik.isSubmitting}>
            Update
          </Button>
        </CardActions>
      </Card>
    </form>
  );
};
