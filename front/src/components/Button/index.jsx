import React from 'react'
import './index.css'

function Button({ onClick, text, Icon }) {
    return (
        <button type="button" className="action-button" onClick={onClick}>
            {Icon && <Icon className="action-button-icon" />}
            {text && <span className="action-button-text">{text}</span>}
        </button>
    )
}

export default Button
