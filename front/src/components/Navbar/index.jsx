import { ThemeContext, themes } from '../../context'
import React, { useEffect, useState } from 'react'

import './index.css'

const Navbar = () => {
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
            document.getElementsByClassName('search')
        )
            .filter(
                (element) => window.getComputedStyle(element).display != 'none'
            )[0]
            .querySelector('.search__input')

        console.log(searchInput.value)
    }

    const handleKeyDown = (event) => {
        if (event.keyCode === 13) {
            //enter was pressed
            search()
        }
    }

    const [theme, setTheme] = useState(
        themes[localStorage.getItem('theme')] || ''
    )

    useEffect(() => {
        if (theme === '') {
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                setTheme(themes.dark)
                localStorage.setItem('theme', 'dark')
            } else {
                setTheme(themes.light)
                localStorage.setItem('theme', 'light')
            }
        }
    }, [])

    useEffect(() => {
        for (const color in theme) {
            document.documentElement.style.setProperty(
                `--${color}`,
                `${theme[color]}`
            )
        }
    }, [theme])

    const toggleTheme = () => {
        if (theme === themes.light) {
            setTheme(themes.dark)
            localStorage.setItem('theme', 'dark')
        } else {
            setTheme(themes.light)
            localStorage.setItem('theme', 'light')
        }
    }

    return (
        <ThemeContext.Provider
            value={{
                theme,
                toggleTheme,
            }}
        >
            <nav className="nav" id="nav">
                <a href="/" className="nav__brand">
                    <span>Cooking</span>
                    <span>App</span>
                    <img src="./logo.png"></img>
                </a>

                <div className="search" id="search">
                    <i
                        className="fa-solid fa-magnifying-glass search__icon"
                        onClick={search}
                    ></i>
                    <input
                        className="search__input"
                        placeholder="Search"
                        type="text"
                        id="searchInput"
                        onKeyDown={handleKeyDown}
                    />
                </div>

                <div className="nav__buttons">
                    <button className="nav__button" onClick={toggleTheme}>
                        <i className="fa-regular fa-moon"></i>
                    </button>
                    <button className="nav__button" onClick={settings}>
                        <i className="fa-solid fa-gear"></i>
                    </button>
                    <button className="nav__button" onClick={profile}>
                        <i className="fa-regular fa-user"></i>
                    </button>
                    <button className="nav__button" onClick={heart}>
                        <i className="fa-regular fa-heart"></i>
                    </button>
                </div>
            </nav>
        </ThemeContext.Provider>
    )
}

export default Navbar
