import React from 'react'
import './index.css'

function Button({ className, onClick, text, Icon }) {
    return (
        <button type="button" className={`action-button ${className}`} onClick={onClick}>
            {Icon && <Icon className="action-button-icon" />}
            {text && <span className="action-button-text">{text}</span>}
        </button>
    )
}

export default Button
