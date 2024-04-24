import React from "react";
import "./index.css";
import { FaAngleRight, FaUserAlt, FaHeart } from "react-icons/fa";
import { BsFillGridFill } from "react-icons/bs";
import { GoDotFill } from "react-icons/go";
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"; //necesara pt redirectionarea de la o pag la alta
import PageButton from "../PageButton";
import Page from "../../pages/Page";

function UserProfile(props) {
  const first_name = props.first_name;
  const last_name = props.last_name;
  const followers = props.followers;
  const following = props.following;
  const profile_img = props.img;
  const pathPage = "../../pages/Page";

  return (
    <div className="user-profile">
      <div className="user-profile-down">
        <img src={profile_img} alt="" />
        <div className="user-profile-name">{last_name + " " + first_name}</div>
        <div className="user-profile-description">
          <a href="#">{followers} urmaritori</a>{" "}
          <div className="user-profile-line">
            <GoDotFill />
          </div>
          <a href="#">{following} urmareste</a>
        </div>
        <Router>
          <div>
            <Routes>
              <Route path={pathPage} element={<Page />} />
              <Route path={pathPage} element={<Page />} />
              <Route path={pathPage} element={<Page />} />
            </Routes>
            <div className="user-profile-button">
              <PageButton
                title={
                  <>
                    <FaUserAlt /> Descriere{" "}
                    <span className="user-profile-button-arrow">
                      <FaAngleRight />
                    </span>
                  </>
                }
                path={pathPage}
              />
              <PageButton
                title={
                  <>
                    <FaHeart /> Favorite{" "}
                    <span className="user-profile-button-arrow">
                      <FaAngleRight />
                    </span>
                  </>
                }
                path={pathPage}
              />
              <PageButton
                title={
                  <>
                    <BsFillGridFill /> Postari{" "}
                    <span className="user-profile-button-arrow">
                      <FaAngleRight />
                    </span>
                  </>
                }
                path={pathPage}
              />
            </div>
          </div>
        </Router>
        <div className="user-profile-report">
          <a href="#"> Raportează </a>
        </div>
      </div>
    </div>
  );
}

export default UserProfile;
