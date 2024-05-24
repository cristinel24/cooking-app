import { Link } from 'react-router-dom'

import { FaHeart } from 'react-icons/fa6'
import { PiCookingPot } from 'react-icons/pi'
import SideButton from './SideButton'
import { useNavigate } from 'react-router-dom'
import { BsTextParagraph } from 'react-icons/bs'

export default function Sidebar({ profileData }) {
    // also add profile pic etc etc

    const links = [
        {
            link: `/profile/${profileData.id}/description`,
            text: 'Descriere',
            alt: [`/profile/${profileData.id}`],
            Icon: BsTextParagraph,
        },
        { link: `/profile/${profileData.id}/favorites`, text: 'Favorite', Icon: FaHeart },
        { link: `/profile/${profileData.id}/recipes`, text: 'Rețete', Icon: PiCookingPot },
    ]
    return (
        <div className="profile-sidebar">
            <div className="profile-sidebar-data">
                <img
                    src={profileData.icon}
                    className="profile-sidebar-data-image"
                    alt="Poza de profil a utilizatorului"
                />
                <span>{profileData.displayName}</span>
                <span>{profileData.followingCount} following</span>
                <span>{profileData.followersCount} followers</span>
            </div>
            <div className="profile-sidebar-buttons">
                {links.map((link, index) => (
                    <SideButton key={index} {...link} className="profile-sidebar-button" />
                ))}
            </div>
        </div>
    )
}
