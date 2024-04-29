import React from 'react'
import './index.css'

import { GoDotFill } from 'react-icons/go'
import ActionButton from '../ActionButton'
import { MdAccountCircle } from 'react-icons/md'
import { FaRegHeart } from 'react-icons/fa'
import { LuLayoutList } from 'react-icons/lu'
import { LuFlagTriangleRight } from 'react-icons/lu'

function UserProfile(props) {
    const pathPage = '../../pages/Page'
    const temporarFunction = () => {}

    return (
        <div className="user-profile">
            <div className="user-profile-down">
                <img src={props.img} alt="" />

                <div className="user-profile-first-line">
                    <div className="user-profile-name">
                        {props.last_name + ' ' + props.first_name}
                    </div>

                    <div className="user-profile-report">
                        <ActionButton
                            onClick={temporarFunction}
                            Icon={LuFlagTriangleRight}
                        />
                    </div>
                </div>

                <div className="user-profile-description">
                    <a href="#">{props.followers} urmaritori</a>{' '}
                    <div className="user-profile-line">
                        <GoDotFill />
                    </div>
                    <a href="#">{props.following} urmareste</a>
                </div>
                <div className="user-profile-follow-button">
                    <ActionButton onClick={temporarFunction} text="Urmareste" />
                </div>

                <div className="user-profile-buttons">
                    <ActionButton
                        onClick={temporarFunction}
                        text="Descriere"
                        Icon={MdAccountCircle}
                    />

                    <ActionButton
                        onClick={temporarFunction}
                        text="Favorite"
                        Icon={FaRegHeart}
                    />

                    <ActionButton
                        onClick={temporarFunction}
                        text="Postari"
                        Icon={LuLayoutList}
                    />
                </div>
            </div>
        </div>
    )
}

export default UserProfile
