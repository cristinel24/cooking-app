import { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { ThemeContext, themes } from './context'

import { Login, Register, Test, Verified } from './pages'

function App() {
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
                    <Route path="/test" element={<Test />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/verify" element={<Verified />} />
                </Routes>
            </Router>
        </ThemeContext.Provider>
    )
}

export default App
