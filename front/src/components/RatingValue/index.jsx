import './index.css'
import { FaStar, FaStarHalfAlt, FaRegStar } from 'react-icons/fa'

export default function RatingValue({ value, className, showValue = true }) {
    const getStars = (value) => {
        const fullStars = Math.floor(value)
        const stars = []
        for (let i = 0; i < fullStars; i++) {
            stars.push(<FaStar key={stars.length} />)
        }
        if (value - fullStars >= 0.5) {
            stars.push(<FaStarHalfAlt key={stars.length} />)
        }
        const emptyStars = 5 - stars.length
        for (let i = 0; i < emptyStars; i++) {
            stars.push(<FaRegStar key={stars.length} />)
        }
        return stars
    }

    return (
        <div className={`rating-value-container ${className ? className : ''}`}>
            {getStars(value)}
            {showValue && <div className="rating-value">{value?.toFixed(2)}</div>}
        </div>
    )
}
