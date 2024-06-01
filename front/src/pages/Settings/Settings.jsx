import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom'
import './index.css'
import { Button } from '../../components'
import { useContext, useEffect, useState } from 'react'
import { UserContext } from '../../context'
import { getFullProfile } from '../../services/profile'
import { ClipLoader } from 'react-spinners'

export default function Settings() {
    const navigate = useNavigate()
    const { user, token, logout } = useContext(UserContext)
    const { pathname } = useLocation()
    const [profile, setProfile] = useState()

    const links = [
        { link: '/settings/account', display: 'Account', alt: ['/settings'] },
        { link: '/settings/history', display: 'History' },
        { link: '/settings/notifications', display: 'Notifications' },
        { link: '/settings/profile', display: 'Profile' },
    ]

    const onLogout = () => {
        logout()
        navigate('/')
    }

    useEffect(() => {
        let ignore = false
        const fetchProfile = async () => {
            try {
                const profile = await getFullProfile(user.id, token)
                if (!ignore) {
                    setProfile(profile)
                }
            } catch (e) {
                navigate('/error')
            }
        }
        fetchProfile()
        return () => (ignore = true)
    }, [])

    if (!profile) {
        return (
            <ClipLoader
                className="loading"
                cssOverride={{
                    alignSelf: 'center',
                }}
                color={'var(--text-color)'}
                loading={true}
                aria-label="Se încarcă..."
                data-testid="loader"
            />
        )
    }

    return (
        <div className="fh settings">
            <div className="settings-card settings-menu">
                <div className="settings-links">
                    {links.map(({ link, display, alt }) => (
                        <Link
                            key={link}
                            to={link}
                            className={`settings-link ${pathname == link || (alt && alt.includes(pathname)) ? 'settings-link-active' : ''}`}
                        >
                            {display}
                        </Link>
                    ))}
                </div>
                <div className="settings-buttons">
                    <Button className="settings-button" text="Deconectare" onClick={onLogout} />
                </div>
            </div>
            <div className="settings-card settings-tab">
                <Outlet context={profile} />
            </div>
        </div>
    )
}
