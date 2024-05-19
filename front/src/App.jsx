import { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { ThemeContext } from './context'

import { Login, Register, Test, Verified } from './pages'

function App() {
    const [theme, setTheme] = useState(localStorage.getItem('theme') || '')

    const setThemeColors = (theme) => {
        document.documentElement.setAttribute('data-theme', theme)
    }

    useEffect(() => {
        if (theme === '') {
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                setTheme('dark')
            } else {
                setTheme('light')
            }
        }
    }, [])

    useEffect(() => {
        localStorage.setItem('theme', theme)
        setThemeColors(theme)
    }, [theme])

    const toggleTheme = () => {
        if (theme === 'light') {
            setTheme('dark')
        } else {
            setTheme('light')
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
