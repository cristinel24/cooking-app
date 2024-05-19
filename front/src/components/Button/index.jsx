import React from 'react'
import './index.css'

function Button({ className, onClick, text, Icon }) {
    return (
        <button
            type="button"
            className={`button ${className}`}
            onClick={onClick}
        >
            {Icon && <Icon className="button-icon" />}
            {text && <span className="button-text">{text}</span>}
        </button>
    )
}

export default Button
