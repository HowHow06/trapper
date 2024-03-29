import { Box, Card, CardContent, CardHeader, Stack, Typography, useTheme } from '@mui/material';
import PropTypes from 'prop-types';
import { Chart } from 'src/components/chart';

const useChartOptions = (labels) => {
  const theme = useTheme();

  return {
    chart: {
      background: 'transparent',
    },
    colors: [theme.palette.primary.main, theme.palette.success.main, theme.palette.warning.main],
    dataLabels: {
      enabled: false,
    },
    labels,
    legend: {
      show: false,
    },
    plotOptions: {
      pie: {
        expandOnClick: false,
      },
    },
    states: {
      active: {
        filter: {
          type: 'none',
        },
      },
      hover: {
        filter: {
          type: 'none',
        },
      },
    },
    stroke: {
      width: 0,
    },
    theme: {
      mode: theme.palette.mode,
    },
    tooltip: {
      fillSeriesColor: false,
    },
  };
};

export const OverviewPieChart = (props) => {
  const { chartSeries, labels, sx, title, isLoading = false, noLabel = false } = props;
  const chartOptions = useChartOptions(labels);

  return (
    <Card sx={sx}>
      {title && <CardHeader title={title} />}
      <CardContent>
        {isLoading ? (
          <>Loading...</>
        ) : (
          <Chart
            height={300}
            options={chartOptions}
            series={chartSeries}
            type="donut"
            width="100%"
          />
        )}
        <Stack
          alignItems="center"
          direction="row"
          justifyContent="center"
          spacing={2}
          sx={{ mt: 2 }}
        >
          {!noLabel &&
            chartSeries.map((item, index) => {
              const label = labels[index];
              return (
                <Box
                  key={label}
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                  }}
                >
                  <Typography sx={{ my: 1 }} variant="h6">
                    {label}
                  </Typography>
                  <Typography color="text.secondary" variant="subtitle2">
                    {item}
                  </Typography>
                </Box>
              );
            })}
        </Stack>
      </CardContent>
    </Card>
  );
};

OverviewPieChart.propTypes = {
  chartSeries: PropTypes.array.isRequired,
  labels: PropTypes.array.isRequired,
  sx: PropTypes.object,
};
