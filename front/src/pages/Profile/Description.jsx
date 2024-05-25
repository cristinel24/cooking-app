import { Outlet, useOutletContext } from 'react-router-dom'

export default function Description() {
    const { profileData } = useOutletContext()
    return (
        <div className="profile-description">
            <div className="profile-description-username">@{profileData.username}</div>
            <h1 className="profile-description-display-name">{profileData.displayName}</h1>
            <h3 className="profile-description-title">Descriere</h3>
            <div
                className="profile-description-content"
                dangerouslySetInnerHTML={{ __html: profileData.description }}
            />
        </div>
    )
}
