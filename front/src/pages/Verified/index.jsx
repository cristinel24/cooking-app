import { useSearchParams } from "react-router-dom"
import { useEffect } from "react"
import { verifyAccount } from "../../services/auth"
import PageButton from '../../components/PageButton/index.jsx'
import './index.css'

export default function Verified() {
    const [queryParams, _] = useSearchParams()

    useEffect(() => {
        const verifyToken = async () => {
            const token = queryParams.get("token")
            if (token == null) {
                return;
            }

            await verifyAccount(token)
        }

        verifyToken()
    }, [])

    return (
        <div className="verified-wrapper">
            <p>Contul tău a fost înregistrat cu succes. Te poți întoarce la pagina principală.</p>
            <div className="verified-button-wrapper">
                <PageButton path={'https://www.google.ro/'} className="verified-button">
                    Acasă
                </PageButton>
            </div>
        </div>
    )
}
