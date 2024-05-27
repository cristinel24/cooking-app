import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom'
import './index.css'
import { Button } from '../../components'
import { useContext } from 'react'
import { UserContext } from '../../context'

export default function Settings() {
    const navigate = useNavigate()
    const { logout } = useContext(UserContext)
    const { pathname } = useLocation()

    const links = [
        { link: '/settings/account', display: 'Account', alt: ['/settings'] },
        { link: '/settings/history', display: 'History' },
        { link: '/settings/notifications', display: 'Notifications' },
        { link: '/settings/profile', display: 'Profile' },
    ]

    const onLogout = () => {
        logout()
        navigate("/")
    }

    return (
        <div className="settings">
            <div className="settings-card settings-menu">
                <div className="settings-links">
                    {links.map(({link, display, alt}) => (
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
                <Outlet />
            </div>
        </div>
    )
}
