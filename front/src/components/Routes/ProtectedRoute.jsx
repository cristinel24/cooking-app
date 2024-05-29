import { useContext } from "react"
import { UserContext } from "../../context"
import { Navigate, Outlet } from "react-router-dom"

export default function ProtectedRoute() {
    const { loggedIn } = useContext(UserContext)

    if (!loggedIn()) {
        return <Navigate to="/" />
    }

    return <Outlet />
}
