import { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import { UserContext, ThemeContext, themes } from './context'
import { AddRecipe, CredentialsChange, Dashboard, EditRecipe, ErrorPage, Feed, ForgotPassword, Login, Profile, Recipe, Register, Search, Settings, Verified } from './pages'
import { AdminRoute, Page, ProtectedRoute, UnprotectedRoute } from './components'

function App() {
    const [remember, setRemember] = useState(localStorage.getItem('user'))
    const [token, setToken] = useState(localStorage.getItem('token') || sessionStorage.getItem('token') || '')
    const [user, setUser] = useState(JSON.parse(localStorage.getItem('user') || sessionStorage.getItem('user')) || {})

    const login = (token, user, remember) => {
        setToken(token)
        setUser(user)
        setRemember(remember)
        if (remember) {
            localStorage.setItem("token", token)
            localStorage.setItem("user", JSON.stringify(user))
        } else {
            sessionStorage.setItem("token", token)
            sessionStorage.setItem("user", JSON.stringify(user))
        }
    }

    const logout = () => {
        setToken('')
        setUser({})
        if (remember) {
            localStorage.removeItem("token")
            localStorage.removeItem("user")
        } else {
            sessionStorage.removeItem("token")
            sessionStorage.removeItem("user")
        }
    }

    const loggedIn = () => Object.keys(user).length !== 0

    const isAdmin = () => user.roles & 0b10 // TODO: constants instead of magic numbers

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
                isAdmin,
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
                        <Route element={<Page />}>
                            {/* error route */}
                            <Route path="*" element={<ErrorPage />} />

                            <Route path="/" element={<Feed />} />
                            <Route path="/popular" element={<Feed />} />
                            <Route path="/best" element={<Feed />} />
                            <Route path="/new" element={<Feed />} />

                            <Route path="/reset/:type" element={<CredentialsChange />} />
                            <Route path="/forgot-password" element={<ForgotPassword />} />
                            <Route path="/profile/:userId" element={<Profile />} />
                            <Route path="/recipe/:recipeId" element={<Recipe />} />
                            <Route path="/search" element={<Search />} />
                            <Route path="/settings" element={<Settings />} />

                            {/* unprotected routes */}
                            <Route element={<UnprotectedRoute />}>
                                <Route path="/login" element={<Login />} />
                                <Route path="/register" element={<Register />} />
                                <Route path="/verify" element={<Verified />} />
                            </Route>

                            {/* protected routes */}
                            <Route element={<ProtectedRoute />}>
                                <Route path="/favorite" element={<Feed />} />
                                <Route path="/followed" element={<Feed />} />
                                <Route path="/recommended" element={<Feed />} />

                                <Route path="/recipe/add" element={<AddRecipe />} />
                                <Route path="/recipe/:recipeId/edit" element={<EditRecipe />} />

                                {/* admin routes */}
                                <Route element={<AdminRoute />}>
                                    <Route path="/dashboard" element={<Dashboard />} />
                                </Route>
                            </Route>
                        </Route>
                    </Routes>
                </Router>
            </ThemeContext.Provider>
        </UserContext.Provider>
    )
}

export default App
