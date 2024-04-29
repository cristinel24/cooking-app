import React, { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom' //necesara pt redirectionarea de la o pag la alta

import { ThemeContext, themes } from './context'

import {
    ActionButton,
    PageButton,
    PopUpChat,
    Recipe,
    Footer,
    UserProfile,
    Navbar,
    AdminBox,
    PreviewRecipe,
    Filters,
    ShowMenu,
    Report,
    ReportRecipe,
    Categories,
} from './components'

import Page from './pages/Page'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

function App() {
    const titlu = 'Buton'

    localStorage.setItem('theme', 'dark')

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
            <Router>
                <Routes>
                    <Route path="/Page" element={<Page />} />
                    <Route path="/LoginPage" element={<LoginPage />} />
                    <Route path="/UserProfile" element={<UserProfile />} />
                    <Route path="/RegisterPage" element={<RegisterPage />} />
                </Routes>
            </Router>
        </ThemeContext.Provider>
    )
}

export default App
