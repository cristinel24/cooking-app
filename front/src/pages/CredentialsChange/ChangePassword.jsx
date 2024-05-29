import { useForm } from 'react-hook-form'

export default function ChangePassword({}) {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors },
    } = useForm()
    return <div className="credentials-change-card">Change password</div>
}
