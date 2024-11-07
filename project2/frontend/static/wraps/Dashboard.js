import React, { useState } from "react";
import WrapCard from "./WrapCard";  // A component for individual wrap cards

const Dashboard = ({ wraps }) => {
  const [activeWrapIndex, setActiveWrapIndex] = useState(null);

  const openWrap = (index) => {
    setActiveWrapIndex(index);
  };

  const closeWrap = () => {
    setActiveWrapIndex(null);
  };

  const nextWrap = () => {
    setActiveWrapIndex((prev) => (prev < wraps.length - 1 ? prev + 1 : prev));
  };

  const previousWrap = () => {
    setActiveWrapIndex((prev) => (prev > 0 ? prev - 1 : prev));
  };

  return (
    <div className="wraps-container">
      {wraps.map((wrap, index) => (
        <WrapCard
          key={index}
          wrap={wrap}
          isActive={index === activeWrapIndex}
          onOpen={() => openWrap(index)}
          onClose={closeWrap}
          onNext={nextWrap}
          onPrevious={previousWrap}
        />
      ))}
    </div>
  );
};

export default Dashboard;
