import { useForm } from 'react-hook-form'
import { credentialChange as apiCredentialChange } from '../../services/auth'

export default function ChangeEmail({}) {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors },
    } = useForm()

    const changeCredential = async () => {
        await apiCredentialChange()
    }
    return <div className="credentials-change-card">Change email</div>
}
