import React from 'react'
import './index.css'

function ActionButton({ onClick, text, Icon }) {
    return (
        <button className="actionbutton" onClick={onClick}>
            {Icon && <Icon className="actionbutton_icon" />}
            {text && <span className="actionbutton_text">{text}</span>}
        </button>
    )
}

export default ActionButton
