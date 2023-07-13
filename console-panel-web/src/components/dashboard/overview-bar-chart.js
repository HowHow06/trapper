import { Box, Card, CardContent, CardHeader, Stack, Typography, useTheme } from '@mui/material';
import PropTypes from 'prop-types';
import { Chart } from 'src/components/chart';

const useChartOptions = (categories) => {
  const theme = useTheme();

  return {
    chart: {
      background: 'transparent',
      type: 'bar',
    },
    colors: [theme.palette.primary.main, theme.palette.success.main, theme.palette.warning.main],
    plotOptions: {
      bar: {
        horizontal: true,
      },
    },
    dataLabels: {
      enabled: false,
    },
    xaxis: {
      categories: categories,
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
    theme: {
      mode: theme.palette.mode,
    },
    tooltip: {
      fillSeriesColor: false,
    },
  };
};

export const OverviewBarChart = (props) => {
  const { chartSeries, categories, sx, title, isLoading = false, noLabel = false } = props;
  const chartOptions = useChartOptions(categories);

  return (
    <Card sx={sx}>
      {title && <CardHeader title={title} />}
      <CardContent>
        {isLoading ? (
          <>Loading...</>
        ) : (
          <Chart height={300} options={chartOptions} series={chartSeries} type="bar" width="100%" />
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
              const label = categories[index];
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
                    {item.data[0]}
                  </Typography>
                </Box>
              );
            })}
        </Stack>
      </CardContent>
    </Card>
  );
};

OverviewBarChart.propTypes = {
  chartSeries: PropTypes.array.isRequired,
  categories: PropTypes.array.isRequired,
  sx: PropTypes.object,
};
