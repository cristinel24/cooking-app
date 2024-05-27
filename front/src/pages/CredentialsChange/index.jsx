import { Navigate, useParams } from "react-router-dom"
import { Page } from "../../components";

export default function CredentialsChange() {
    const { type } = useParams();

    if (!["email", "password", "username"].includes(type)) {
        return <Navigate to="/not-found" />
    }

    return (
        <div>CredentialsChange</div>
    )
}
