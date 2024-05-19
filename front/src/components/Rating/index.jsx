import './index.css'
import { FaStar, FaStarHalfAlt, FaRegStar } from 'react-icons/fa'

export default function Rating({ ratingValue, className }) {
    const getStars = (ratingValue) => {
        const fullStars = Math.floor(ratingValue)
        const stars = []
        for (let i = 0; i < fullStars; i++) {
            stars.push(<FaStar key={stars.length} />)
        }
        if (ratingValue - fullStars >= 0.5) {
            stars.push(<FaStarHalfAlt key={stars.length} />)
        }
        const emptyStars = 5 - stars.length
        for (let i = 0; i < emptyStars; i++) {
            stars.push(<FaRegStar key={stars.length} />)
        }
        return stars
    }

    return (
        <div className={`rating-container ${className}`}>
            {getStars(ratingValue)}
            <div className="rating-value">{ratingValue}</div>
        </div>
    )
}
