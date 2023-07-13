import { Card, CardHeader, Divider, Stack, Typography } from '@mui/material';
import _get from 'lodash/get';
import moment from 'moment';
import PropTypes from 'prop-types';
import { SEVERITY_COLOR_MAP, TASK_STATUS_NAME } from 'src/constants/variables';
import { TimeUtils } from 'src/utils/time-utils';

const InfoList = ({ title, subtitle, data, columns, ...rest }) => {
  const renderDateTimeFromUTC = (data, column) => {
    const value = _get(data, column.accessor);
    const dateString = value
      ? moment(TimeUtils.getDateFromUTCString(value)).format('YYYY-MM-DD HH:mm')
      : '-';
    return (
      <Typography variant="body2" component="p">
        {dateString}
      </Typography>
    );
  };

  const renderBoolean = (data, column) => {
    return (
      <Typography variant="body2" component="p">
        {_get(data, column.accessor) ? 'Yes' : 'No'}
      </Typography>
    );
  };

  const renderValue = (column) => {
    if (column.type === 'boolean') {
      return renderBoolean(data, column);
    }

    if (column.type === 'datetime') {
      return renderDateTimeFromUTC(data, column);
    }

    if (column.type === 'task_status') {
      const value = _get(data, column.accessor);
      return (
        <Typography variant="body2" component="p">
          {value ? TASK_STATUS_NAME[value] : '-'}
        </Typography>
      );
    }

    if (column.type === 'vulnerability_severity') {
      const value = _get(data, column.accessor);
      return value ? (
        <SeverityPill color={SEVERITY_COLOR_MAP['delivered']}>
          {TASK_STATUS_NAME[value]}
        </SeverityPill>
      ) : (
        '-'
      );
    }

    if (typeof column.accessor === 'function') {
      return (
        <Typography variant="body2" component="p">
          {column.accessor(data)}
        </Typography>
      );
    }

    return (
      <Typography variant="body2" component="p">
        {_get(data, column.accessor) || '-'}
      </Typography>
    );
  };

  return (
    <Card {...rest}>
      {title && (
        <>
          <CardHeader subheader={subtitle} title={title} />
          <Divider />
        </>
      )}

      <Stack
        direction="column"
        justifyContent="space-evenly"
        spacing={1}
        divider={<Divider orientation="horizontal" />}
        sx={{
          m: 0,
          py: 1,
          height: '100%',
        }}
      >
        {columns.map((column, index) => {
          return (
            <Stack
              direction="row"
              alignItems="center"
              key={`${index}-${column.accessor}`}
              sx={{
                px: 2,
                py: 1,
              }}
            >
              <Typography
                variant="subtitle2"
                component="h6"
                sx={{
                  textTransform: 'capitalize',
                  minWidth: '180px',
                }}
              >
                {column.name}
              </Typography>
              {renderValue(column)}
            </Stack>
          );
        })}
      </Stack>
    </Card>
  );
};

InfoList.propTypes = {
  title: PropTypes.string,
  subtitle: PropTypes.string,
  data: PropTypes.object.isRequired,
  columns: PropTypes.array.isRequired,
};

export default InfoList;
