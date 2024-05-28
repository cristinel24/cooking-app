import { useState } from 'react'
import { FaRegStar, FaStar } from 'react-icons/fa6'

const FormStars = ({ value = 0, onChange }) => {
    const handleClick = (newRating) => {
        onChange(newRating)
    }

    return (
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
    )
}

export default FormStars
