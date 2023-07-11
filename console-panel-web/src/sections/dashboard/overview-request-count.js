import ListBulletIcon from '@heroicons/react/24/solid/ListBulletIcon';
import OverviewFigureCard from 'src/components/dashboard/overview-figure-card';
const OverviewRequestCount = (props) => {
  const { value } = props;
  return (
    <OverviewFigureCard
      displayText="Requests Processed"
      value={value}
      Icon={ListBulletIcon}
      iconColor="success.main"
    />
  );
};

OverviewRequestCount.propTypes = {};

export default OverviewRequestCount;
