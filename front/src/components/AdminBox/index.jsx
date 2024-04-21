import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./index.css";
import PageButton from "../PageButton";
import ActionButton from "../ActionButton";
import Page from "../../pages/Page";

function Admin() {
  let userName = "Utilizator";
  let userNumber = "#1";
  let content =
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.";
  let date = "23.07.2023 18:00 AM";
  let viewProfile = "Vizualizare profil";
  let read = "Citit";
  const pathPage = "/";
  const handleClick = () => {};

  return (
    <div className="admin-box">
      <div className="admin-header">
        <div className="admin-header-left">
          <img src="./!.png" alt="Admin Sign" />
          <h3>{userName}</h3>
        </div>
        <div className="admin-header-right">
          <p>{userNumber}</p>
        </div>
      </div>
      <div className="admin-content">
        <p>{content}</p>
      </div>
      <div className="admin-footer">
        <div className="admin-footer-left">
          <p>{date}</p>
        </div>
        <div className="admin-footer-right">
          <Router>
            <div>
              <Routes>
                <Route path={pathPage} element={<Page />} />
              </Routes>
              <div className="customButtons">
                <div>
                  <PageButton
                    title={
                      <>
                        <span>{viewProfile}</span>{" "}
                        <img src="./view.png" alt="View ph" />
                      </>
                    }
                    path={pathPage}
                  />
                </div>
              </div>
            </div>
          </Router>
          <div className="customButtons">
            <div>
              <ActionButton
                onClick={handleClick}
                text={
                  <>
                    <span>{read}</span> <img src="./read.png" alt="Read ph" />
                  </>
                }
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Admin;
