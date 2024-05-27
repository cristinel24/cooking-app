import React from 'react'
import { Link } from 'react-router-dom'
import './index.css'

function PageButton({ children, path, className }) {
    return (
        <Link className={`link ${className ? className : ''}`} to={path}>
            {children}
        </Link>
    )
}

export default PageButton
