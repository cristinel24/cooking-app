import { useState } from 'react'
import { FaRegStar, FaStar } from 'react-icons/fa6'

const FormStars = ({ value = 0, onChange, label, className, errorCheck, id }) => {
    const handleClick = (newRating) => {
        onChange(newRating)
    }

    return (
        <div className={`form-item ${className ? className : ''}`}>
            {label && (
                <label htmlFor={id} className="form-label">
                    {label}
                </label>
            )}
            <div className="form-stars">
                {[1, 2, 3, 4, 5].map((star, index) =>
                    star <= value ? (
                        <FaStar
                            key={index}
                            onClick={() => {
                                handleClick(star)
                            }}
                        />
                    ) : (
                        <FaRegStar
                            key={index}
                            onClick={() => {
                                handleClick(star)
                            }}
                        />
                    )
                )}
            </div>
            {errorCheck && errorCheck(id)}
        </div>
    )
}

export default FormStars
