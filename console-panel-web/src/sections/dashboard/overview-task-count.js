import RectangleStackIcon from '@heroicons/react/24/solid/RectangleStackIcon';
import OverviewFigureCard from 'src/components/dashboard/overview-figure-card';
const OverviewTaskCount = (props) => {
  const { value } = props;
  return (
    <OverviewFigureCard
      displayText="Tasks Created"
      value={value}
      Icon={RectangleStackIcon}
      iconColor="warning.main"
    />
  );
};

OverviewTaskCount.propTypes = {};

export default OverviewTaskCount;
