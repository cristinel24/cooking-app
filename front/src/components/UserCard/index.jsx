import './index.css'
import Rating from '../Rating'

export default function UserCard({
    displayName,
    username,
    rating,
    link,
    profilePicture,
}) {
    return (
        <a href={link} className="user-card-link">
            <div className="user-card">
                <img src={profilePicture} className="user-card-image"></img>
                <div className="user-card-details">
                    <p className="user-card-details-display-name">
                        {displayName}
                    </p>
                    <p className="user-card-details-user-name">
                        <i className="fa-solid fa-at"></i>
                        {username}
                    </p>
                    <Rating ratingValue={rating} />
                </div>
            </div>
        </a>
    )
}
