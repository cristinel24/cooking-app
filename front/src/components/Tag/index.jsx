import React from 'react'
import { RxCross2 } from 'react-icons/rx'
import './index.css'

function Tag(props) {
    console.log(props.text)
    return (
        <div className="tag">
            <span>{props.text}</span>
            {props.onRemove && (
                <button className="tag-button" onClick={props.onRemove}>
                    <RxCross2 />
                </button>
            )}
        </div>
    )
}

export default Tag
