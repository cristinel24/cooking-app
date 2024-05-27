import { Link } from 'react-router-dom'

import './index.css'

import { RatingValue } from '..'

export default function UserCard({ user }) {
    return (
        <Link to={`/profile/${user.id}`} className="user-card-link">
            <div className="user-card">
                <img src={user.icon} className="user-card-image"></img>
                <div className="user-card-details">
                    <p className="user-card-details-display-name">{user.displayName}</p>
                    <p className="user-card-details-user-name">
                        <i className="fa-solid fa-at"></i>
                        {user.username}
                    </p>
                    <RatingValue value={user.ratingAvg} />
                </div>
            </div>
        </Link>
    )
}
