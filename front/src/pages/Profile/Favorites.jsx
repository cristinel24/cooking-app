import { useContext } from 'react'
import { UserContext } from '../../context'
import { useOutletContext } from 'react-router-dom'
import ErrorMessage from './ErrorMessage'

export default function Favorites() {
    const { profileData } = useOutletContext()
    const { token, user, loggedIn } = useContext(UserContext)
    return !(loggedIn() && user.id === profileData?.id) ? (
        <ErrorMessage>
            <p>Nu aveți permisiunea să vizualizați rețetele favorite ale acestui utilizator.</p>
        </ErrorMessage>
    ) : (
        <div>Favorites</div>
    )
}
