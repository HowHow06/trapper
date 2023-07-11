import * as Yup from 'yup';

export const passwordSchema = Yup.string()
  .max(255)
  .min(8, 'Password is too short - should be 8 chars minimum.')
  .matches(/[A-Z]/, 'Password must contain at least one uppercase letter.')
  .matches(/[a-z]/, 'Password must contain at least one lowercase letter.')
  .matches(/[0-9]+/, 'Password must contain at least one number.')
  .matches(/[!@#$%^&*]/, 'Password must contain at least one special character.')
  .required('Password is required');
