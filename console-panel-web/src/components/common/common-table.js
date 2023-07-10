import {
  Box,
  Button,
  Card,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TablePagination,
  TableRow,
  TableSortLabel,
} from '@mui/material';
import { visuallyHidden } from '@mui/utils';
import _get from 'lodash/get';
import moment from 'moment';
import NextLink from 'next/link';
import { useRouter } from 'next/router';
import PropTypes from 'prop-types';
import { useState } from 'react';
import { STATUS_COLOR_MAP, TASK_STATUS_NAME } from 'src/constants/variables';
import { TimeUtils } from 'src/utils/time-utils';
import { Scrollbar } from '../scrollbar';

const descendingComparator = (a, b, orderByAccessor) => {
  if (_get(b, orderByAccessor) < _get(a, orderByAccessor)) {
    return -1;
  }
  if (_get(b, orderByAccessor) > _get(a, orderByAccessor)) {
    return 1;
  }
  return 0;
};

const getComparator = (order, orderByAccessor) => {
  return order === 'desc'
    ? (a, b) => descendingComparator(a, b, orderByAccessor)
    : (a, b) => -descendingComparator(a, b, orderByAccessor);
};

const CommonTable = ({
  columns,
  data,
  itemHref,
  identity,
  actions,
  noPagination = false,
  isLoading,
  ...rest
}) => {
  const router = useRouter();
  const [limit, setLimit] = useState(100);
  const [page, setPage] = useState(0);
  const [query, setQuery] = useState('');
  const [order, setOrder] = useState('');
  const [orderBy, setOrderBy] = useState('');

  const handleLimitChange = (event) => {
    setLimit(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === 'asc';
    setOrder(isAsc ? 'desc' : 'asc');
    setOrderBy(property);
  };

  const renderTableHeader = ({ orderBy, order }) => {
    return columns.map((columnItem) => {
      return (
        <TableCell key={columnItem.accessor}>
          <TableSortLabel
            active={orderBy === columnItem.accessor}
            direction={orderBy === columnItem.accessor ? order : 'asc'}
            onClick={(event) => handleRequestSort(event, columnItem.accessor)}
          >
            {columnItem.name}
            {orderBy === columnItem.accessor ? (
              <Box component="span" sx={visuallyHidden}>
                {order === 'desc' ? 'sorted descending' : 'sorted ascending'}
              </Box>
            ) : null}
          </TableSortLabel>
        </TableCell>
      );
    });
  };

  const renderBoolean = (data, column) => {
    return _get(data, column.accessor) ? 'Yes' : 'No';
  };

  const renderTableColumn = (dataItem, columnItem) => {
    if (columnItem.image) {
      const fileName = _get(dataItem, columnItem.accessor);
      if (!fileName) {
        return '-';
      }
      return <img src={fileName} loading="lazy" alt={fileName} height="50" />;
    }

    if (columnItem.type === 'boolean') {
      return renderBoolean(data, columnItem);
    }

    if (columnItem.type === 'datetime') {
      const value = _get(dataItem, columnItem.accessor);
      return value ? moment(TimeUtils.getDateFromUTCString(value)).format('YYYY-MM-DD HH:mm') : '-';
    }

    if (columnItem.type === 'task_status') {
      const value = _get(dataItem, columnItem.accessor);
      return value ? TASK_STATUS_NAME[value] : '-';
    }

    if (columnItem.type === 'vulnerability_severity') {
      const value = _get(dataItem, columnItem.accessor);
      return value ? (
        <SeverityPill color={STATUS_COLOR_MAP['delivered']}>{TASK_STATUS_NAME[value]}</SeverityPill>
      ) : (
        '-'
      );
    }

    if (typeof columnItem.accessor === 'function') {
      return columnItem.accessor(dataItem);
    }

    return _get(dataItem, columnItem.accessor);
  };

  const renderTableRows = (dataItem) => {
    return columns.map((columnItem, index) => {
      return (
        <TableCell
          key={`${index}-${dataItem.id}-${columnItem.accessor}`}
          sx={{ cursor: 'pointer' }}
        >
          {itemHref ? (
            <NextLink
              href={`${itemHref}/${dataItem[identity]}`}
              style={{
                textDecoration: 'none',
              }}
            >
              <Box
                className="MuiTableCell-root"
                sx={{
                  color: 'text.primary',
                }}
              >
                {renderTableColumn(dataItem, columnItem)}
              </Box>
            </NextLink>
          ) : (
            renderTableColumn(dataItem, columnItem)
          )}
        </TableCell>
      );
    });
  };

  const renderActions = (dataItem, dataIndex) => {
    if (!actions || actions.length === 0) {
      return null;
    }

    return (
      <TableCell padding="checkbox">
        <Stack
          direction="row"
          justifyContent="flex-end"
          alignItems="center"
          spacing={0.5}
          sx={{ pr: 2 }}
        >
          {actions.map((action) => {
            return (
              <Button
                key={`${action.label.toLowerCase()}-${dataItem.uuid}`}
                variant="contained"
                onClick={() => action.onClick(dataItem, dataIndex)}
              >
                {action.label}
              </Button>
            );
          })}
        </Stack>
      </TableCell>
    );
  };

  const getFilteredData = ({ data, columns, query }) => {
    return data.filter((dataItem) => {
      for (const columnItem of columns) {
        const value = _get(dataItem, columnItem.accessor);
        if (value && value.toString().toUpperCase().indexOf(query.toUpperCase()) !== -1) {
          return true;
        }
      }
      return false;
    });
  };

  const filteredData = query ? getFilteredData({ data, columns, query }) : data;

  return (
    <>
      {/* {noSearch ? (
        ''
      ) : (
        <Box
          sx={{
            minWidth: '20rem',
            maxWidth: '30%',
            mb: '1rem',
          }}
        >
          <SearchBox
            onSubmitSearch={(searchKey) => {
              setQuery(searchKey);
            }}
          />
        </Box>
      )} */}

      <Card {...rest}>
        <Scrollbar>
          <Box sx={{ minWidth: 500 }}>
            <Table>
              <TableHead>
                <TableRow>
                  {renderTableHeader({ order, orderBy })}
                  {actions && actions.length > 0 && <TableCell key="actions">Actions</TableCell>}
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredData.length === 0 && !isLoading && (
                  <TableRow>
                    <TableCell colSpan={columns.length + 1}>No data available</TableCell>
                  </TableRow>
                )}
                {isLoading && (
                  <TableRow>
                    <TableCell colSpan={columns.length + 1}>Loading...</TableCell>
                  </TableRow>
                )}
                {(limit > 0 ? filteredData.slice(page * limit, page * limit + limit) : filteredData)
                  .sort(getComparator(order, orderBy))
                  .map((dataItem, dataIndex) => (
                    <TableRow hover key={`row-${dataItem[identity]}`}>
                      {renderTableRows(dataItem)}
                      {renderActions(dataItem, dataIndex)}
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </Box>
          {!noPagination && (
            <TablePagination
              component="div"
              count={filteredData.length}
              rowsPerPage={limit}
              page={page}
              onPageChange={handlePageChange}
              onRowsPerPageChange={handleLimitChange}
              rowsPerPageOptions={[25, 50, 100, { label: 'All', value: -1 }]}
            />
          )}
        </Scrollbar>
      </Card>
    </>
  );
};

CommonTable.propTypes = {
  columns: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string.isRequired,
      accessor: PropTypes.oneOfType([PropTypes.string, PropTypes.func]).isRequired,
    })
  ).isRequired,
  data: PropTypes.array.isRequired,
  itemHref: PropTypes.string,
  identity: PropTypes.string.isRequired,
  actions: PropTypes.array,
};

CommonTable.defaultProps = {
  actions: [],
};

export default CommonTable;
