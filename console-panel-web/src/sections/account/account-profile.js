import { Avatar, Box, Card, CardContent, Typography } from '@mui/material';
import { DEFAULT } from 'src/constants/variables';

export const AccountProfile = (props) => {
  const { user, sx = {} } = props;
  return (
    <Card sx={sx}>
      <CardContent>
        <Box
          sx={{
            alignItems: 'center',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Avatar
            src={user?.avatar || DEFAULT.AVATAR}
            sx={{
              height: 80,
              mb: 2,
              width: 80,
            }}
          />
          <Typography gutterBottom variant="h5">
            {user?.username || ''}
          </Typography>
          <Typography color="text.secondary" variant="body2">
            {user?.email || ''}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};
