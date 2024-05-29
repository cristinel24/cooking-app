import { useForm } from 'react-hook-form'

export default function ChangeUsername({}) {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors },
    } = useForm()
    return <div className="credentials-change-card">Change email</div>
}
