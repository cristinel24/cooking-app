import { FaHeart } from 'react-icons/fa6'
import { PiCookingPot } from 'react-icons/pi'
import { BsTextParagraph } from 'react-icons/bs'
import React, { useState, useContext } from 'react'
import {
    getFollowers as apiGetFollowers,
    getFollowing as apiGetFollowing,
    follow as apiFollow,
    unfollow as apiUnfollow,
} from '../../services/profile'

import SideButton from './SideButton'
import { Button, InfoModal } from '../../components'
import UserListModal from './UserListModal'
import { getErrorMessage } from '../../utils/api'
import { UserContext } from '../../context'

export default function Sidebar({ profileData, setProfileData }) {
    const [userModalOpen, setUserModalOpen] = useState({
        followers: false,
        following: false,
    })

    const [isFollowLoading, setIsFollowLoading] = useState(false)
    const [error, setError] = useState('')

    const { token, user, loggedIn } = useContext(UserContext)

    const toggleFollow = async () => {
        if (profileData?.isFollowing !== undefined) {
            try {
                setIsFollowLoading(true)
                if (profileData?.isFollowing) {
                    await apiUnfollow(user?.id, profileData?.id, token)
                    setProfileData((data) => {
                        return {
                            ...data,
                            isFollowing: false,
                            followersCount: data.followersCount - 1,
                        }
                    })
                } else {
                    await apiFollow(user?.id, profileData?.id, token)
                    setProfileData((data) => {
                        return {
                            ...data,
                            isFollowing: true,
                            followersCount: data.followersCount + 1,
                        }
                    })
                }
            } catch (e) {
                setError(getErrorMessage(e))
            } finally {
                setIsFollowLoading(false)
            }
        }
    }

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

    const fetchFollowing = async (start, count) => {
        const response = await apiGetFollowing(profileData.id, start, count)
        return {
            data: response.following,
        }
    }

    const fetchFollowers = async (start, count) => {
        const response = await apiGetFollowers(profileData.id, start, count)
        return {
            data: response.followers,
        }
    }

    return (
        <div className="profile-sidebar" id={`profile-sidebar-${profileData.id}`}>
            <InfoModal
                isOpen={error !== ''}
                onClose={() => {
                    setError('')
                }}
            >
                <p>Eroare: {error}</p>
            </InfoModal>
            {userModalOpen.followers && (
                <UserListModal
                    contentLabel={'Urmăritori'}
                    fetchData={fetchFollowers}
                    total={profileData.followersCount}
                    isOpen={userModalOpen.followers}
                    onClose={() => {
                        setUserModalOpen((data) => ({
                            ...data,
                            followers: !userModalOpen.followers,
                        }))
                    }}
                />
            )}
            {userModalOpen.following && (
                <UserListModal
                    contentLabel={'Urmăriți'}
                    fetchData={fetchFollowing}
                    total={profileData.followsCount}
                    isOpen={userModalOpen.following}
                    onClose={() => {
                        setUserModalOpen((data) => ({
                            ...data,
                            following: !userModalOpen.following,
                        }))
                    }}
                />
            )}
            <div className="profile-sidebar-data">
                <img
                    src={profileData.icon}
                    className="profile-sidebar-data-image"
                    alt="Poza de profil a utilizatorului"
                />
                <p className="profile-sidebar-data-display-name">{profileData.displayName}</p>
                <p>
                    <button
                        className="profile-sidebar-follow-button"
                        type="button"
                        onClick={() => {
                            setUserModalOpen((data) => ({
                                ...data,
                                followers: !userModalOpen.followers,
                            }))
                        }}
                    >
                        {profileData.followersCount} urmăritori
                    </button>
                    <span> • </span>
                    <button
                        className="profile-sidebar-follow-button"
                        type="button"
                        onClick={() => {
                            setUserModalOpen((data) => ({
                                ...data,
                                following: !userModalOpen.following,
                            }))
                        }}
                    >
                        {profileData.followsCount} urmăriți
                    </button>
                </p>
                {loggedIn() && profileData?.id != user?.id && (
                    <Button
                        disabled={isFollowLoading}
                        text={profileData.isFollowing ? 'Nu mai urmări' : 'Urmărește'}
                        onClick={toggleFollow}
                    />
                )}
            </div>

            <div className="profile-sidebar-buttons">
                {links.map((link, index) => (
                    <SideButton key={index} {...link} className="profile-sidebar-button" />
                ))}
            </div>
        </div>
    )
}
