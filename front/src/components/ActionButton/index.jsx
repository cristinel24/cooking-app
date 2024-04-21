import React from "react";
import "./index.css";

function ActionButton({ onClick, text }) {
  return (
    <button className="button" onClick={onClick}>
      {text}
    </button>
  );
}

export default ActionButton;
