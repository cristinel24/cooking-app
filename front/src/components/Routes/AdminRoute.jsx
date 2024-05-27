import { useContext } from "react"
import { UserContext } from "../../context"
import { Navigate, Outlet } from "react-router-dom"

export default function AdminRoute() {
    const { isAdmin } = useContext(UserContext)

    if (!isAdmin()) {
        return <Navigate to="/" />
    }

    return <Outlet />
}
