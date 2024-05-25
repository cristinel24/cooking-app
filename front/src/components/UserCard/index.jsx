import './index.css'
import { RatingValue } from '../index.jsx'
import { Link } from 'react-router-dom'

export default function UserCard({ displayName, username, rating, link, profilePicture }) {
    return (
        <Link to={link} className="user-card-link">
            <div className="user-card">
                <img src={profilePicture} className="user-card-image"></img>
                <div className="user-card-details">
                    <p className="user-card-details-display-name">{displayName}</p>
                    <p className="user-card-details-user-name">
                        <i className="fa-solid fa-at"></i>
                        {username}
                    </p>
                    <RatingValue value={rating} />
                </div>
            </div>
        </Link>
    )
}
