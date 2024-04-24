import React from 'react'
import './index.css'
import { FaAngleRight, FaUserAlt, FaHeart } from 'react-icons/fa'
import { BsFillGridFill } from 'react-icons/bs'
import { GoDotFill } from 'react-icons/go'
import PageButton from '../PageButton'

function UserProfile(props) {
    const pathPage = '../../pages/Page'

    return (
        <div className="user-profile">
            <div className="user-profile-down">
                <img src={props.img} alt="" />
                <div className="user-profile-name">
                    {props.last_name + ' ' + props.first_name}
                </div>
                <div className="user-profile-description">
                    <a href="#">{props.followers} urmaritori</a>{' '}
                    <div className="user-profile-line">
                        <GoDotFill />
                    </div>
                    <a href="#">{props.following} urmareste</a>
                </div>
                <div className="user-profile-button">
                    <PageButton
                        children={
                            <>
                                <FaUserAlt /> Descriere{' '}
                                <span className="user-profile-button-arrow">
                                    <FaAngleRight />
                                </span>
                            </>
                        }
                        path={pathPage}
                        className="user-profile-button"
                    />
                    <PageButton
                        children={
                            <>
                                <FaHeart /> Favorite{' '}
                                <span className="user-profile-button-arrow">
                                    <FaAngleRight />
                                </span>
                            </>
                        }
                        path={pathPage}
                        className="user-profile-button"
                    />
                    <PageButton
                        children={
                            <>
                                <BsFillGridFill /> Postari{' '}
                                <span className="user-profile-button-arrow">
                                    <FaAngleRight />
                                </span>
                            </>
                        }
                        path={pathPage}
                        className="user-profile-button"
                    />
                </div>
                <div className="user-profile-report">
                    <a href="#"> Raportează </a>
                </div>
            </div>
        </div>
    )
}

export default UserProfile
