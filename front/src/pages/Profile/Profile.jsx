import { Link, Outlet, useLocation, useNavigate, useSearchParams } from 'react-router-dom'
import './index.css'
import React, { useContext, useState, useEffect } from 'react'
import { UserContext } from '../../context'
import { ClipLoader } from 'react-spinners'

import { getProfile } from '../../services/profile'
import Sidebar from './Sidebar'

import { GenericModal } from '../../components'

export default function Profile() {
    const navigate = useNavigate()

    const [loading, setLoading] = useState(true)
    const [profileData, setProfileData] = useState({})

    const profileId = 21

    useEffect(() => {
        const fetch = async () => {
            // temporary; TODO: proper error handling with actual error message
            try {
                const profile = await getProfile(profileId)
                setProfileData(profile)

                setLoading(false)
            } catch (e) {
                navigate('/not-found')
            }
        }

        fetch()
    }, [])

    // const onLogout = () => {
    //     logout()
    //     navigate('/')
    // }

    return (
        <>
            <ClipLoader
                className="loading"
                cssOverride={{
                    borderColor: 'var(--text-color)',
                    color: 'var(--text-color)',
                    alignSelf: 'center',
                }}
                width={'100%'}
                loading={loading}
                aria-label="Se încarcă..."
                data-testid="loader"
            />
            {!loading && (
                <div className="profile">
                    <Sidebar profileData={profileData} setProfileData={setProfileData} />
                    <Outlet context={{ profileData }} />
                </div>
            )}
        </>
    )
}
