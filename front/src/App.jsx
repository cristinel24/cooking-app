import { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { ThemeContext, themes } from './context'

import { AddRecipe, CredentialsChange, Dashboard, EditRecipe, ErrorPage, Feed, ForgotPassword, Login, Profile, Recipe, Register, Search, Settings, Test, Verified } from './pages'
import { UserContext } from './context/user-context'
import { Page, ProtectedRoute } from './components'

function App() {
    const [token, setToken] = useState(localStorage.getItem('token') || '')
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')) || {})

    const login = (token, user) => {
        setToken(token)
        setUser(user)
        localStorage.setItem("token", token)
        localStorage.setItem("user", JSON.stringify(user))
    }

    const logout = () => {
        setToken('')
        setUser({})
        localStorage.setItem("token", '')
        localStorage.setItem("user", JSON.stringify({}))
    }

    const loggedIn = () => Object.keys(user).length !== 0

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
        <UserContext.Provider
            value={{
                user,
                token,
                login,
                logout,
                loggedIn,
            }}
        >
            <ThemeContext.Provider
                value={{
                    theme,
                    toggleTheme,
                }}
            >
                <Router>
                    <Routes>
                        <Route path="/" element={<Page />}>
                            {/* error route */}
                            <Route path="/" element={<ErrorPage />} />

                            <Route path="/popular" element={<Feed />} />
                            <Route path="/best" element={<Feed />} />
                            <Route path="/recommended" element={<Feed />} />
                            {/* <Route path="/:type" element={<Feed />} /> */}

                            <Route path="/" element={<ProtectedRoute />}>
                                <Route path="/favorite" element={<Feed />} />
                                <Route path="/followed" element={<Feed />} />
                                <Route path="/recommended" element={<Feed />} />
                            </Route>

                            <Route path="/reset/:type" element={<CredentialsChange />} />
                            <Route path="/forgot-password" element={<ForgotPassword />} />
                            <Route path="/login" element={<Login />} />
                            <Route path="/profile/:userId" element={<Profile />} />
                            <Route path="/recipe/:recipeId" element={<Recipe />} />
                            <Route path="/register" element={<Register />} />
                            <Route path="/search" element={<Search />} />
                            <Route path="/settings" element={<Settings />} />
                            <Route path="/test" element={<Test />} />
                            <Route path="/verify" element={<Verified />} />

                            {/* protected routes */}
                            <Route path="/recipe/add" element={<AddRecipe />} />
                            <Route path="/recipe/:recipeId/edit" element={<EditRecipe />} />

                            {/* admin routes */}
                            <Route path="/dashboard" element={<Dashboard />} />
                        </Route>
                    </Routes>
                </Router>
            </ThemeContext.Provider>
        </UserContext.Provider>
    )
}

export default App
