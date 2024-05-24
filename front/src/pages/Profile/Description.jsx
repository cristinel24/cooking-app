import { Outlet, useOutletContext } from 'react-router-dom'

export default function Description() {
    const { profileData } = useOutletContext()
    return (
        <div className="profile-description">
            <h1 className="profile-description-title">{profileData.displayName}</h1>
            <h3 className="profile-description-title">Descriere</h3>
            <div
                className="profile-description-content"
                dangerouslySetInnerHTML={{ __html: profileData.description }}
            />
        </div>
    )
}
