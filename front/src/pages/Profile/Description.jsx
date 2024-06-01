import { Outlet, useOutletContext } from 'react-router-dom'
import { RatingValue } from '../../components'

export default function Description() {
    const { profileData } = useOutletContext()
    return (
        <div className="profile-description">
            <div className="profile-description-user-data">
                <h1 className="profile-description-display-name">{profileData.displayName}</h1>
                <div className="profile-description-row">
                    <div className="profile-description-username">@{profileData.username}</div>
                    <RatingValue
                        value={profileData?.ratingAvg}
                        className="profile-description-rating"
                    />
                </div>
            </div>
            <h3 className="profile-description-title">Descriere</h3>
            <div
                className="profile-description-content"
                dangerouslySetInnerHTML={{ __html: profileData.description }}
            />
        </div>
    )
}
