import { useSearchParams } from "react-router-dom"
import { Page } from "../../components"
import { useEffect } from "react"
import { verify } from "../../services/auth"

const Verified = () => {
    const [queryParams, _] = useSearchParams()

    useEffect(() => {
        const verifyToken = async () => {
            const token = queryParams.get("token")
            if (token == null) {
                return;
            }

            await verify(token)
        }

        verifyToken()
    }, [])

    return (
        <Page>
            Your email is confirmed. You may close this page now.
        </Page>
    )
}

export default Verified
