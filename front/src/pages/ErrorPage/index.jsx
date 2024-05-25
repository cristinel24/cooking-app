import { PageButton } from '../../components'
import './index.css'

// added Page suffix because it was clashing to another Error property before
export default function ErrorPage() {
    return (
        <div className="error">
            <img src="/logo.png" />
            <h1>404</h1>
            <p>Pagina nu a fost găsită.</p>
            <PageButton path="/">Acasă</PageButton>
        </div>
    )
}
