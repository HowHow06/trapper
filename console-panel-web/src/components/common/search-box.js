import XMarkIcon from '@heroicons/react/24/outline/XMarkIcon';
import MagnifyingGlassIcon from '@heroicons/react/24/solid/MagnifyingGlassIcon';
import { Card, IconButton, InputAdornment, OutlinedInput, SvgIcon } from '@mui/material';
import { useState } from 'react';

const SearchBox = (props) => {
  const { onSubmitSearch, placeholder = 'Search here' } = props;
  const [searchKey, setSearchKey] = useState('');

  const handleSearchKeyChange = (event) => {
    event.preventDefault();
    const searchKey = event.target.value;
    setSearchKey(searchKey);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      onSubmitSearch(searchKey);
    }
  };

  const handleClearClick = () => {
    setSearchKey('');
    onSubmitSearch('');
  };

  return (
    <Card sx={{ p: 2 }}>
      <OutlinedInput
        value={searchKey}
        fullWidth
        placeholder={placeholder}
        startAdornment={
          <InputAdornment position="start">
            <SvgIcon color="action" fontSize="small">
              <MagnifyingGlassIcon />
            </SvgIcon>
          </InputAdornment>
        }
        endAdornment={
          <InputAdornment position="end">
            <IconButton
              fontSize="small"
              sx={{ visibility: searchKey ? 'visible' : 'hidden' }}
              onClick={handleClearClick}
            >
              <XMarkIcon height="1.25rem" />
            </IconButton>
          </InputAdornment>
        }
        sx={{ maxWidth: 500 }}
        onChange={handleSearchKeyChange}
        onKeyDown={handleKeyDown}
      />
    </Card>
  );
};

export default SearchBox;
