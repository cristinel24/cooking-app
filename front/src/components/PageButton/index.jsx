import React from "react";
import { Link } from "react-router-dom";
import "./index.css";

function PageButton({ title, path }) {
  return (
    <Link to={path}>
      <button className="button">{title}</button>
    </Link>
  );
}

export default PageButton;
