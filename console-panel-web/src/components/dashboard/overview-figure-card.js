import ArrowDownIcon from '@heroicons/react/24/solid/ArrowDownIcon';
import ArrowUpIcon from '@heroicons/react/24/solid/ArrowUpIcon';
import CurrencyDollarIcon from '@heroicons/react/24/solid/CurrencyDollarIcon';
import { Avatar, Card, CardContent, Stack, SvgIcon, Typography } from '@mui/material';
import PropTypes from 'prop-types';

const OverviewFigureCard = (props) => {
  const {
    differenceSinceLastMonth,
    positive = false,
    sx,
    value,
    iconColor = 'error.main',
    displayText,
    Icon = CurrencyDollarIcon,
  } = props;

  return (
    <Card sx={sx}>
      <CardContent>
        <Stack alignItems="flex-start" direction="row" justifyContent="space-between" spacing={3}>
          <Stack spacing={1}>
            <Typography color="text.secondary" variant="overline">
              {displayText}
            </Typography>
            <Typography variant="h4">{value}</Typography>
          </Stack>
          <Avatar
            sx={{
              backgroundColor: iconColor,
              height: 56,
              width: 56,
            }}
          >
            <SvgIcon>
              <Icon />
            </SvgIcon>
          </Avatar>
        </Stack>
        {differenceSinceLastMonth && (
          <Stack alignItems="center" direction="row" spacing={2} sx={{ mt: 2 }}>
            <Stack alignItems="center" direction="row" spacing={0.5}>
              <SvgIcon color={positive ? 'success' : 'error'} fontSize="small">
                {positive ? <ArrowUpIcon /> : <ArrowDownIcon />}
              </SvgIcon>
              <Typography color={positive ? 'success.main' : 'error.main'} variant="body2">
                {differenceSinceLastMonth}%
              </Typography>
            </Stack>
            <Typography color="text.secondary" variant="caption">
              Since last month
            </Typography>
          </Stack>
        )}
      </CardContent>
    </Card>
  );
};

OverviewFigureCard.prototypes = {
  differenceSinceLastMonth: PropTypes.number,
  positive: PropTypes.bool,
  sx: PropTypes.object,
  value: PropTypes.string.isRequired,
  displayText: PropTypes.string.isRequired,
  Icon: PropTypes.element,
  iconColor: PropTypes.string,
};

export default OverviewFigureCard;
