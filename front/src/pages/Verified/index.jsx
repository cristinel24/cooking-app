import { useSearchParams } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { verifyAccount } from '../../services/auth'
import PageButton from '../../components/PageButton/index.jsx'
import './index.css'
import { getErrorMessage } from '../../utils/api'

export default function Verified() {
    const [params] = useSearchParams()
    const [error, setError] = useState()
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        const verifyToken = async () => {
            setLoading(true)
            try {
                const token = params.get('token')

                if (token == null) {
                    setError('Token-ul este invalid')
                    return
                }

                await verifyAccount(token)
            } catch (e) {
                setError(getErrorMessage(e))
            } finally {
                setLoading(false)
            }
        }

        verifyToken()
    }, [])

    if (loading) {
        return (
            <div className="verified-wrapper">
                <p>Se verifică contul dumneavoastră... Nu părăsiți pagina</p>
            </div>
        )
    }

    if (error) {
        return (
            <div className="verified-wrapper">
                <p>Eroare: {error}</p>
            </div>
        )
    }

    return (
        <div className="verified-wrapper">
            <p>Contul tău a fost înregistrat cu succes. Te poți întoarce la pagina principală.</p>
            <div className="verified-button-wrapper">
                <PageButton path="/" className="verified-button">
                    Acasă
                </PageButton>
            </div>
        </div>
    )
}
