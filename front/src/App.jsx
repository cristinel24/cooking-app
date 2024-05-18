import { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { ThemeContext, themes } from './context'

import { Login, Register, Test, Verified } from './pages'

function App() {
    const [theme, setTheme] = useState(
        themes[localStorage.getItem('theme')] || {}
    )

    const setColorsFromTheme = (theme) => {
        for (const color in theme) {
            const kebabColor = color.replace(
                /[A-Z]/g,
                (match) => '-' + match.toLowerCase()
            )
            document.documentElement.style.setProperty(
                `--${kebabColor}`,
                `${theme[color]}`
            )
        }
    }

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
        setColorsFromTheme(theme)
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
