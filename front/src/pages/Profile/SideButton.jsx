import { IoIosArrowForward } from 'react-icons/io'
import './index.css'

import { useNavigate, useLocation } from 'react-router-dom'

export default function SideButton({ link, display, alt, Icon }) {
    const { pathname } = useLocation()
    return (
        <button
            type="button"
            onClick={() => {
                navigate(link)
            }}
            className={`profile-button ${
                pathname == link || (alt && alt.includes(pathname)) ? 'profile-button-active' : ''
            }`}
        >
            {Icon && <Icon className="profile-button-icon" />}
            {text && <span className="profile-button-text">{text}</span>}
            {text && <IoIosArrowForward className="profile-button-icon" />}
        </button>
    )
}
