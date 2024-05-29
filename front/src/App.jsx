import { useEffect, useState } from 'react'

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { UserContext, ThemeContext } from './context'
import {
    AccountSettings,
    AddRecipe,
    CredentialsChange,
    Dashboard,
    EditRecipe,
    ErrorPage,
    Feed,
    ForgotPassword,
    History,
    Login,
    Notifications,
    Profile,
    ProfileDescription,
    ProfileRecipes,
    ProfileFavorites,
    ProfileSettings,
    Recipe,
    RecipesSearch,
    Register,
    Search,
    Settings,
    UsersSearch,
    Verified,
} from './pages'
import { AdminRoute, Page, ProtectedRoute, UnprotectedRoute } from './components'

function App() {
    const [remember, setRemember] = useState(localStorage.getItem('user'))
    const [token, setToken] = useState(
        localStorage.getItem('token') || sessionStorage.getItem('token') || ''
    )
    const [user, setUser] = useState(
        JSON.parse(localStorage.getItem('user') || sessionStorage.getItem('user')) || {}
    )

    const login = (token, user, remember) => {
        setToken(token)
        setUser(user)
        setRemember(remember)
        if (remember) {
            localStorage.setItem('token', token)
            localStorage.setItem('user', JSON.stringify(user))
        } else {
            sessionStorage.setItem('token', token)
            sessionStorage.setItem('user', JSON.stringify(user))
        }
    }

    const logout = () => {
        setToken('')
        setUser({})
        if (remember) {
            localStorage.removeItem('token')
            localStorage.removeItem('user')
        } else {
            sessionStorage.removeItem('token')
            sessionStorage.removeItem('user')
        }
    }

    const loggedIn = () => Object.keys(user).length !== 0

    const isAdmin = () => user.roles & 0b10 // TODO: constants instead of magic numbers

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
                            <Route path="/recipe/:recipeId" element={<Recipe />} />
                              
                            {/* <Route path="/profile/:profileId" element={<ProfileDescription />} /> */}

                            <Route element={<Profile />}>
                                <Route
                                    path="/profile/:profileId"
                                    element={<ProfileDescription />}
                                />
                                <Route
                                    path="/profile/:profileId/description"
                                    element={<ProfileDescription />}
                                />
                                <Route
                                    path="/profile/:profileId/favorites"
                                    element={<ProfileFavorites />}
                                />
                                <Route
                                    path="/profile/:profileId/recipes"
                                    element={<ProfileRecipes />}
                                />
                            </Route>

                            <Route element={<Search />}>
                                <Route path="/search/users" element={<UsersSearch />} />
                                <Route path="/search/recipes" element={<RecipesSearch />} />
                            </Route>

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

                                <Route element={<Settings />}>
                                    <Route path="/settings" element={<AccountSettings />} />
                                    <Route path="/settings/account" element={<AccountSettings />} />
                                    <Route path="/settings/history" element={<History />} />
                                    <Route
                                        path="/settings/notifications"
                                        element={<Notifications />}
                                    />
                                    <Route path="/settings/profile" element={<ProfileSettings />} />
                                </Route>

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
