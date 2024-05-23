import { IoIosArrowForward } from 'react-icons/io'
import './index.css'

function SideButton({ onClick, text, Icon }) {
    return (
        <button type="button" className="profile-button" onClick={onClick}>
            {Icon && <Icon className="profile-button-icon" />}
            {text && <span className="profile-button-text">{text}</span>}
            {text && <IoIosArrowForward className="profile-button-icon" />}
        </button>
    )
}

export default SideButton
