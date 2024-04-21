import React from "react";
// import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
// import { faFlag } from "@fortawesome/free-solid-svg-icons";
// import { faTrademark } from "@fortawesome/free-solid-svg-icons";

import "./index.css";

function Footer() {
  return (
    <div>
      {location.pathname === "/" && (
        <footer className="footer">
          <div className="brand">
            <a href="/">COOKING APP. 2024 ALL RIGHTS ARE RESERVED</a>
            {/* <FontAwesomeIcon icon={faTrademark} className="fa-icon" /> */}
          </div>
          <div className="bug">
            {/* <FontAwesomeIcon icon={faFlag} className="fa-icon" /> */}
            <p>Raporteaza un bug</p>
          </div>
        </footer>
      )}
    </div>
  );
}
export default Footer;
