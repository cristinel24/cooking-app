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
            Contul tău a fost înregistrat cu succes. Te poți întoarce la pagina principală.
        </Page>
    )
}

export default Verified
