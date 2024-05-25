// StarRating.js
import { useState } from 'react'
import PropTypes from 'prop-types'
import { FaRegStar, FaStar } from 'react-icons/fa6'

const FormStars = ({ value = 0, onChange }) => {
    const [rating, setRating] = useState(value)

    const handleClick = (newRating) => {
        setRating(newRating)
        onChange(newRating)
    }

    return (
        <div className="form-stars">
            {[1, 2, 3, 4, 5].map((star) =>
                star <= rating ? (
                    <FaStar
                        onClick={() => {
                            handleClick(star)
                        }}
                    />
                ) : (
                    <FaRegStar
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
