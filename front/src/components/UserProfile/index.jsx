import React, { Component } from "react";
import "./index.css";
import profile_img from "../../../public/ProfileImage.avif";
import {
  FaAngleRight,
  FaUserAlt,
  FaHeart,
  FaAppStoreIos,
} from "react-icons/fa";
import { BsFillGridFill } from "react-icons/bs";
import { GoDotFill } from "react-icons/go";
import { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom"; //necesara pt redirectionarea de la o pag la alta
import PageButton from "../PageButton";
import Page from "../../pages/Page";

function UserProfile() {
  const first_name = "Popescu";
  const last_name = "Ion";
  const followers = 70;
  const following = 12;
  const pathPage = "./Page";

  return (
    <div className="uspr">
      <div className="profile-down">
        <img src={profile_img} alt="" />
        <div className="profile-name">{last_name + " " + first_name}</div>
        <div className="profile-description">
          <a href="#">{followers} urmaritori</a>{" "}
          <div className="liniuta">-</div>
          <a href="#">{following} urmareste</a>
        </div>
        <Router>
          <div>
            <Routes>
              <Route path={pathPage} element={<Page />} />
              <Route path={pathPage} element={<Page />} />
              <Route path={pathPage} element={<Page />} />
            </Routes>
            <div className="button_2">
              <PageButton
                title={
                  <>
                    <icon>
                      <FaUserAlt />
                    </icon>{" "}
                    Descriere{" "}
                    <span className="arrow">
                      <FaAngleRight />
                    </span>
                  </>
                }
                path={pathPage}
              />
              <PageButton
                title={
                  <>
                    <icon>
                      <FaHeart />
                    </icon>{" "}
                    Favorite{" "}
                    <span className="arrow">
                      <FaAngleRight />
                    </span>
                  </>
                }
                path={pathPage}
              />
              <PageButton
                title={
                  <>
                    <icon>
                      <BsFillGridFill />
                    </icon>{" "}
                    Postari{" "}
                    <span className="arrow">
                      <FaAngleRight />
                    </span>
                  </>
                }
                path={pathPage}
              />
            </div>
          </div>
        </Router>
        <div className="report">
          <a href="#"> Raportează </a>
        </div>
      </div>
    </div>
  );
}

export default UserProfile;
