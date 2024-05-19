import React from 'react'
import { RxCross2 } from 'react-icons/rx'
import './index.css'

function Tag({ text, onRemove, className }) {
    return (
        <div className={`tag ${className}`}>
            <span>{text}</span>
            {onRemove && (
                <button className="tag-button" onClick={onRemove}>
                    <RxCross2 />
                </button>
            )}
        </div>
    )
}

export default Tag
