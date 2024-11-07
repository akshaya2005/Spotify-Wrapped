import React from "react";
import "./WrapCard.css";

const WrapCard = ({ wrap, isActive, onOpen, onClose, onNext, onPrevious }) => {
  return (
    <div>
      {isActive ? (
        <div className="wrap-expanded">
          <h3>{wrap.title}</h3>
          <p>{wrap.content}</p>
          <button onClick={onPrevious}>Back</button>
          <button onClick={onNext}>Next</button>
          <button onClick={onClose}>Close</button>
        </div>
      ) : (
        <div className="wrap-card" onClick={onOpen}>
          <h3>{wrap.title}</h3>
        </div>
      )}
    </div>
  );
};

export default WrapCard;
