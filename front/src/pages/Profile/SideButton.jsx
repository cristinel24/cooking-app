import { IoIosArrowForward } from 'react-icons/io'
import './index.css'

import { useNavigate, useLocation } from 'react-router-dom'
import { useEffect } from 'react'

export default function SideButton({ link, text, alt, Icon, className }) {
    const navigate = useNavigate()
    const { pathname } = useLocation()
    return (
        <button
            type="button"
            onClick={() => {
                navigate(link)
            }}
            className={`profile-button ${className ? className : ''} ${
                pathname == link || (alt && alt.includes(pathname)) ? 'profile-button-active' : ''
            }`}
        >
            <div className="profile-button-display">
                {Icon && <Icon className="profile-button-icon" />}
                {text && <span className="profile-button-text">{text}</span>}
            </div>
            {text && <IoIosArrowForward className="profile-button-arrow" />}
        </button>
    )
}
