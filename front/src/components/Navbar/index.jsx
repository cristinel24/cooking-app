import { ThemeContext, themes } from '../../context'
import React, { useContext, useEffect, useState } from 'react'
import './index.css'
import { FaRegHeart, FaRegUser, FaRegMoon, FaBars } from 'react-icons/fa6'
import { IoSettingsOutline, IoSearch } from 'react-icons/io5'
import { FaTimes } from 'react-icons/fa'

const Navbar = () => {
    const { toggleTheme } = useContext(ThemeContext)

    const heart = () => {
        console.log('Pressed heart!')
    }

    const profile = () => {
        console.log('Pressed profile!')
    }

    const settings = () => {
        console.log('Pressed settings!')
    }

    const search = () => {
        const searchInput = Array.from(
            document.getElementsByClassName('nav-search')
        )
            .filter(
                (element) => window.getComputedStyle(element).display != 'none'
            )[0]
            .querySelector('.nav-search-input')

        console.log(searchInput.value)
    }

    const handleKeyDown = (event) => {
        if (event.keyCode === 13) {
            //enter was pressed
            search()
        }
    }

    const [activeDropdown, setActiveDropdown] = useState('nav-dropdown')

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
                <img className="nav-brand-img" src="./logo.png"></img>
            </a>

            <div className="nav-search" id="search">
                <IoSearch className="nav-search-icon" onClick={search} />
                <input
                    className="nav-search-input"
                    placeholder="Search"
                    type="text"
                    id="searchInput"
                    onKeyDown={handleKeyDown}
                />
            </div>

            <div className="nav-buttons">
                <button className="nav-button" onClick={toggleTheme}>
                    <FaRegMoon />
                </button>
                <button className="nav-button" onClick={settings}>
                    <IoSettingsOutline />
                </button>
                <button className="nav-button" onClick={profile}>
                    <FaRegUser />
                </button>
                <button className="nav-button" onClick={heart}>
                    <FaRegHeart />
                </button>
            </div>

            {/* hamburger menu */}
            <div className="nav-buttons-hamburger-menu">
                <button className="nav-button-theme" onClick={toggleTheme}>
                    <FaRegMoon />
                </button>

                <button className="nav-dropdown-icon" onClick={toggleDropdown}>
                    {activeDropdown === 'nav-dropdown' ? (
                        <FaBars />
                    ) : (
                        <FaTimes />
                    )}
                </button>
            </div>

            <div className={activeDropdown}>
                <button className="nav-button" onClick={settings}>
                    <IoSettingsOutline />
                    <p>Setari</p>
                </button>
                <button className="nav-button" onClick={profile}>
                    <FaRegUser />
                    <p>Profilul tau</p>
                </button>
                <button className="nav-button" onClick={heart}>
                    <FaRegHeart />
                    <p>Favorite</p>
                </button>
            </div>
        </nav>
    )
}

export default Navbar
