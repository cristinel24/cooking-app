import { useSearchParams } from "react-router-dom"
import { Page } from "../../components"
import { useEffect } from "react"
import { verify } from "../../services/auth"
import PageButton from '../../components/PageButton/index.jsx'
import './index.css'

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
            <div className="verified-wrapper">
                <p>Contul tău a fost înregistrat cu succes. Te poți întoarce la pagina principală.</p>
            <div className="verified-home-button">
                <PageButton path={'https://www.google.ro/'} className="verified-button">
                     Acasă
                </PageButton>
            </div>
            </div>
        </Page>
    )
}

export default Verified
