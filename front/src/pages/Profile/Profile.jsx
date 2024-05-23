import { Link, Outlet, useLocation, useNavigate, useSearchParams } from 'react-router-dom'
import './index.css'
import React, { useContext, useState, useEffect } from 'react'
import { UserContext } from '../../context'
import { ClipLoader } from 'react-spinners'

export default function Profile() {
    const navigate = useNavigate()
    const { pathname } = useLocation()

    const [loading, setLoading] = useState(false)

    const [profileData, setProfileData] = useState({})
    const profileId = 21

    useEffect(() => {}, [])

    const links = [
        {
            link: `/profile/${profileId}/description`,
            display: 'Descriere',
            alt: [`/profile/${profileId}`],
        },
        { link: `/profile/${profileId}/favorites`, display: 'Favorite' },
        { link: `/profile/${profileId}/recipes`, display: 'Rețete' },
    ]

    // const onLogout = () => {
    //     logout()
    //     navigate('/')
    // }

    return (
        <>
            <ClipLoader
                // color={'blue'}
                className="loading"
                cssOverride={{
                    borderColor: 'var(--color-white)',
                    color: 'var(--color-white)',
                    alignSelf: 'center',
                }}
                width={'100%'}
                loading={loading}
                aria-label="Se încarcă..."
                data-testid="loader"
            />
            {!loading && (
                <div className="profile">
                    <div className="profile-sidebar"></div>
                    <Outlet />
                </div>
            )}
        </>
    )
}
