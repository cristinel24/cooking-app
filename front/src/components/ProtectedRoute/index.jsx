import { useContext } from "react"
import { UserContext } from "../../context"
import { Navigate } from "react-router-dom"

export default function ProtectedRoute({ children }) {
    const { loggedIn } = useContext(UserContext)

    if (!loggedIn()) {
        return <Navigate to="/" />
    }

    return children
}
