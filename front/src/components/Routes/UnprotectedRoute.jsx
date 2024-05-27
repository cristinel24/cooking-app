import { useContext } from "react"
import { UserContext } from "../../context"
import { Navigate, Outlet } from "react-router-dom"

// the user MUST NOT be logged in in order to access this page
export default function UnprotectedRoute() {
    const { loggedIn } = useContext(UserContext)

    if (loggedIn()) {
        return <Navigate to="/" />
    }

    return <Outlet />
}
