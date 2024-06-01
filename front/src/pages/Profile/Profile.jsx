import { Outlet, useNavigate, useParams } from 'react-router-dom'
import './index.css'
import React, { useContext, useState, useEffect } from 'react'
import { UserContext } from '../../context'
import { ClipLoader } from 'react-spinners'

import { getProfile } from '../../services/profile'
import Sidebar from './Sidebar'

import { getErrorMessage } from '../../utils/api'

export default function Profile() {
    const navigate = useNavigate()

    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [profileData, setProfileData] = useState({})
    const { user, token } = useContext(UserContext)

    const { profileId } = useParams([])
    const { token } = useContext(UserContext)

    useEffect(() => {
        const fetch = async () => {
            setLoading(true)
            try {
                const profile = await getProfile(profileId, token)
                setProfileData(profile)
            } catch (e) {
                if (e?.response?.status === 404) {
                    navigate('/not-found')
                } else {
                    setError(getErrorMessage(e))
                }
            } finally {
                setLoading(false)
            }
        }

        fetch()
    }, [profileId])

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
                loading={loading && !error}
                aria-label="Se încarcă..."
                data-testid="loader"
            />
            {!error && !loading && (
                <div className="profile">
                    <Sidebar profileData={profileData} setProfileData={setProfileData} />
                    <Outlet context={{ profileData }} />
                </div>
            )}
            {error !== '' && <span style={{ textAlign: 'center' }}>{error}</span>}
        </>
    )
}
