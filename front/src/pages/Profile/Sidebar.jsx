import { FaHeart } from 'react-icons/fa6'
import { PiCookingPot } from 'react-icons/pi'
import { BsTextParagraph } from 'react-icons/bs'
import React, { useState } from 'react'

import SideButton from './SideButton'
import { Button, GenericModal } from '../../components'
import InfiniteScroll from 'react-infinite-scroll-component'

export default function Sidebar({ profileData, setProfileData }) {
    const [followers, setFollowers] = useState({ hasMore: true, data: [] })
    const [following, setFollowing] = useState({ hasMore: true, data: [] })

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
    return (
        <>
            <GenericModal>
                {/* followers*/}

                <InfiniteScroll
                    className="user-list-container"
                    dataLength={following.data.length}
                    next={() =>
                        setFollowing((following) =>
                            following.data.concat(
                                [...Array(10).keys()].map((id) => {
                                    return {}
                                })
                            )
                        )
                    }
                    hasMore={true}
                    loader={<h4>Loading...</h4>}
                    endMessage={
                        <p style={{ textAlign: 'center' }}>
                            <b>No more users for you</b>
                        </p>
                    }
                >
                    {/* {recipes.map((recipe) => (
                        <RecipeCard
                            key={recipe.id}
                            recipe={recipe}
                            owned={recipe.author.id === user.id}
                            onFavorite={onFavorite}
                            onRemove={onRemove}
                        />
                    ))} */}
                </InfiniteScroll>
            </GenericModal>
            <div className="profile-sidebar">
                <div className="profile-sidebar-data">
                    <img
                        src={profileData.icon}
                        className="profile-sidebar-data-image"
                        alt="Poza de profil a utilizatorului"
                    />
                    <p className="profile-sidebar-data-display-name">{profileData.displayName}</p>
                    <p>
                        <span>{profileData.followingCount} following</span>
                        <span> • </span>
                        <span>{profileData.followersCount} followers</span>
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
        </>
    )
}
