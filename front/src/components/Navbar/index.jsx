import { useContext, useEffect, useState } from 'react'
import { FaRegHeart, FaRegUser, FaRegMoon, FaBars } from 'react-icons/fa6'
import { IoSettingsOutline, IoSearch, IoLogOutOutline } from 'react-icons/io5'
import { AiOutlineUserAdd } from 'react-icons/ai'
import { FaTimes } from 'react-icons/fa'
import { Link, useLocation, useNavigate, useSearchParams } from 'react-router-dom'

import './index.css'
import { ThemeContext, UserContext } from '../../context'
import { LuLogIn } from 'react-icons/lu'

const Navbar = () => {
    const location = useLocation()
    const [params, setParams] = useSearchParams()
    const navigate = useNavigate()

    const { logout, loggedIn } = useContext(UserContext)
    const { toggleTheme } = useContext(ThemeContext)

    const [inputValue, setInputValue] = useState('')
    const [activeDropdown, setActiveDropdown] = useState('nav-dropdown')

    useEffect(() => {
        ;(() => {
            const query = params.get('query')

            if (query) {
                setInputValue(query)
            }
        })()
    }, [params, navigate])

    const search = () => {
        if (location.pathname == '/search') {
            const filters = params.get('filters')
            navigate(`/search?query=${inputValue}&${filters ? `filters=${filters}` : ''}`)
        } else {
            navigate(`/search?query=${inputValue}`)
        }
    }

    const handleKeyUp = (event) => {
        if (event.keyCode === 13) {
            // enter was pressed
            search()
        }
    }

    const onLogout = () => {
        logout()
        navigate('/')
    }

    const toggleDropdown = () => {
        activeDropdown === 'nav-dropdown'
            ? setActiveDropdown('nav-dropdown nav-active')
            : setActiveDropdown('nav-dropdown')
    }

    return (
        <nav className="nav" id="nav">
            <a href="/" className="nav-brand">
                <span className="nav-brand-span">Cooking</span>
                <span className="nav-brand-span">App</span>
                <img className="nav-brand-img" src="/logo.png" alt="brand" />
            </a>

            <div className="nav-search" id="search">
                <IoSearch className="nav-search-icon" onClick={search} />
                <input
                    className="nav-search-input"
                    placeholder="Search"
                    type="text"
                    id="searchInput"
                    onKeyUp={handleKeyUp}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                />
            </div>

            <div className="nav-buttons">
                <button type="button" className="nav-button" onClick={toggleTheme}>
                    <FaRegMoon />
                </button>
                {loggedIn() ? (
                    <>
                        <Link to="/settings" className="nav-button">
                            <IoSettingsOutline />
                        </Link>
                        <Link to="/profile" className="nav-button">
                            <FaRegUser />
                        </Link>
                        <Link to="/profile/favorite" className="nav-button">
                            <FaRegHeart />
                        </Link>
                        <button type="button" className="nav-button" onClick={onLogout}>
                            <IoLogOutOutline />
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-button">
                            <LuLogIn />
                        </Link>
                        <Link to="/register" className="nav-button">
                            <AiOutlineUserAdd />
                        </Link>
                    </>
                )}
            </div>

            {/* hamburger menu */}
            <div className="nav-buttons nav-buttons-hamburger-menu">
                <button type="button" className="nav-button nav-button-theme" onClick={toggleTheme}>
                    <FaRegMoon />
                </button>

                <button
                    type="button"
                    className="nav-button nav-button-dropdown"
                    onClick={toggleDropdown}
                >
                    {activeDropdown === 'nav-dropdown' ? <FaBars /> : <FaTimes />}
                </button>
            </div>

            <div className={activeDropdown}>
                {loggedIn() ? (
                    <>
                        <Link to="/settings" className="nav-button">
                            <IoSettingsOutline />
                            <p>Setări</p>
                        </Link>
                        <Link to="/profile" className="nav-button">
                            <FaRegUser />
                            <p>Profilul tău</p>
                        </Link>
                        <Link to="/profile/favorite" className="nav-button">
                            <FaRegHeart />
                            <p>Favorite</p>
                        </Link>
                        <button type="button" className="nav-button" onClick={onLogout}>
                            <IoLogOutOutline />
                            <p>Deconectează-te</p>
                        </button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-button">
                            <LuLogIn />
                            <p>Conectează-te</p>
                        </Link>
                        <Link to="/register" className="nav-button">
                            <AiOutlineUserAdd />
                            <p>Înregistrează-te</p>
                        </Link>
                    </>
                )}
            </div>
        </nav>
    )
}

export default Navbar
