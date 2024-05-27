import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

import './index.css'
import photo from '/register-cover.png'

import { FormInput, FormPassword, InfoModal } from '../../components'
import { registerUser } from '../../services/auth'
import { length } from '../../utils/form'
import { getErrorMessage } from '../../utils/api'

export default function Register() {
    const {
        register,
        handleSubmit,
        watch,
        setError,
        clearErrors,
        formState: { errors },
    } = useForm()
    const password = watch('password')

    const navigate = useNavigate()

    const [loading, setLoading] = useState(false)
    const [showModal, setShowModal] = useState(false)

    const toggleModal = () => setShowModal((state) => !state)

    const onModalClose = () => {
        setShowModal(false)
        navigate('/login')
    }

    const onErrorModalClose = () => {
        clearErrors('api')
    }

    const onSubmit = async (data) => {
        delete data.confirmPassword // remove field

        setLoading(true)
        try {
            await registerUser(data)
            toggleModal()
        } catch (e) {
            setError('api', { message: getErrorMessage(e) })
        } finally {
            setLoading(false)
        }
    }

    const errorCheck = (id) => {
        if (errors[id]) {
            if (errors[id].type == 'required') {
                return <p className="form-error">Acest câmp este obligatoriu</p>
            }

            return <p className="form-error">{errors[id].message}</p>
        }
    }

    return (
        <div className="page">
            <div className="form-container">
                <h2>Înregistrare</h2>
                <InfoModal isOpen={showModal} onClose={onModalClose}>
                    <p>
                        Veți primi un email de confirmare la adresa furnizată. Vă rugăm să vă
                        verificați email-ul și să continuați de acolo.
                    </p>
                </InfoModal>
                <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                    <div className="form-row">
                        <FormInput
                            label="Nume de utilizator"
                            id="username"
                            errorCheck={errorCheck}
                            {...register('username', {
                                required: true,
                                minLength: length('minim', 8),
                                maxLength: length('maxim', 64),
                            })}
                        />
                        <FormInput
                            label="Nume"
                            id="displayName"
                            errorCheck={errorCheck}
                            {...register('displayName', {
                                minLength: length('minim', 4),
                                maxLength: length('maxim', 64),
                            })}
                        />
                    </div>
                    <div className="form-row">
                        <FormInput
                            type="email"
                            label="Email"
                            id="email"
                            errorCheck={errorCheck}
                            {...register('email', {
                                required: true,
                                maxLength: length('maxim', 256),
                            })}
                        />
                    </div>
                    <div className="form-row">
                        <FormPassword
                            label="Parolă"
                            id="password"
                            errorCheck={errorCheck}
                            {...register('password', {
                                required: true,
                                minLength: length('minim', 8),
                                maxLength: length('maxim', 64),
                            })}
                        />
                        <FormPassword
                            label="Confirmare parolă"
                            id="confirmPassword"
                            errorCheck={errorCheck}
                            {...register('confirmPassword', {
                                required: true,
                                validate: (v) =>
                                    v == password ||
                                    'Parola și confirmarea parolei nu se potrivesc.',
                            })}
                        />
                    </div>
                    {errors['api'] && (
                        <InfoModal isOpen={Boolean(errors['api'])} onClose={onErrorModalClose}>
                            <p className="form-error">{errors['api'].message}</p>
                        </InfoModal>
                    )}
                    <button type="submit" className="form-submit" disabled={loading}>
                        {loading ? 'Înregistrare...' : 'Înregistrați-vă'}
                    </button>
                </form>
                <span>
                    Ai deja un cont?{' '}
                    <Link className="form-link" to="/login">
                        Conectează-te aici
                    </Link>
                </span>
            </div>
            <div className="page-separator"></div>
            <div className="bg-image-container">
                <img className="bg-image" src={photo} alt="photo doesn't appear" />
            </div>
        </div>
    )
}
