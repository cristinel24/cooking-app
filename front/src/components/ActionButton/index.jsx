import React from 'react'
import './index.css'

function ActionButton({ onClick, text, Icon }) {
    return (
        <button className="action-button" onClick={onClick}>
            <Icon className="action-button-icon" />
            {text && <span className="action-button-text">{text}</span>}
        </button>
    )
}

export default ActionButton
