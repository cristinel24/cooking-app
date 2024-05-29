import { FaHeart } from 'react-icons/fa6'
import { PiCookingPot } from 'react-icons/pi'
import { BsTextParagraph } from 'react-icons/bs'
import React, { useState, useEffect } from 'react'
import {
    getFollowers as apiGetFollowers,
    getFollowing as apiGetFollowing,
} from '../../services/profile'

import SideButton from './SideButton'
import { Button, GenericModal } from '../../components'
import UserListModal from './UserListModal'
import { getErrorMessage } from '../../utils/api' //TODO: error handling for follow/unfollow requests

export default function Sidebar({ profileData, setProfileData }) {
    const [userModalOpen, setUserModalOpen] = useState({
        followers: false,
        following: false,
    })

    const toggleFollow = () => {
        if (profileData.isFollowing !== undefined) {
            setProfileData((data) => {
                return {
                    ...data,
                    isFollowing: !data.isFollowing,
                    followersCount: profileData.isFollowing
                        ? data.followersCount - 1
                        : data.followersCount + 1,
                }
            })
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
        const response = await apiGetFollowers(profileData.id, start, count)
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
                    total={profileData.followingCount}
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
                        {profileData.followingCount} urmăriți
                    </button>
                </p>
                <Button
                    text={profileData.isFollowing ? 'Nu mai urmări' : 'Urmărește'}
                    onClick={toggleFollow}
                />
            </div>

            <div className="profile-sidebar-buttons">
                {links.map((link, index) => (
                    <SideButton key={index} {...link} className="profile-sidebar-button" />
                ))}
            </div>
        </div>
    )
}
