import { useForm } from 'react-hook-form'
import { changeEmail as apiChangeEmail } from '../../services/credentials'
import './index.css'

import { FormInput, FormPassword, InfoModal } from '../../components'
import { useState, useEffect } from 'react'
import { length } from '../../utils/form'
import { getErrorMessage } from '../../utils/api'
import { useNavigate, useSearchParams } from 'react-router-dom'

export default function ChangeEmail({}) {
    const {
        register,
        handleSubmit,
        watch,
        clearErrors,
        setError,
        formState: { errors },
    } = useForm()

    const navigate = useNavigate()
    const [params, _] = useSearchParams()
    const token = params?.get('token')

    const [loading, setLoading] = useState(false)
    const [tokenError, setTokenError] = useState(false)
    const [showModal, setShowModal] = useState(false)
    const password = watch('password')

    useEffect(() => {
        let ignore = false
        const verifyToken = async () => {
            setLoading(true)
            try {
                if (ignore) {
                    return
                }
                ignore = true

                if (token == null || token == undefined) {
                    setTokenError('Token-ul este invalid')
                    return
                }
            } catch (e) {
                setTokenError(getErrorMessage(e))
            } finally {
                setLoading(false)
            }
        }

        verifyToken()

        return () => {
            ignore = true
        }
    }, [])

    if (loading) {
        return (
            <div className="credentials-change-wrapper">
                <p>Se verifică token-ul... Nu părăsiți pagina</p>
            </div>
        )
    }

    if (tokenError) {
        return (
            <div className="credentials-change-wrapper">
                <p>Eroare: {tokenError}</p>
            </div>
        )
    }

    const onModalClose = () => {
        setShowModal(false)
        navigate('/')
    }

    const onErrorModalClose = () => {
        clearErrors('api')
    }

    const onSubmit = async (data) => {
        console.log(data)
        setLoading(true)
        try {
            await apiChangeEmail(data.email, token)
            setShowModal(true)
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
        <div className="credentials-change-wrapper">
            <div className="credentials-change-card">
                <h2>Schimbare parolă</h2>
                <p>Introduceți noua parolă pe care doriți să o asociați contului dumneavoastră.</p>
                <InfoModal isOpen={showModal} onClose={onModalClose}>
                    <p>
                        Parola dumneavoastră a fost schimbată. Veți fi redirecționat la pagina
                        principală.
                    </p>
                </InfoModal>
                <InfoModal isOpen={Boolean(errors['api'])} onClose={onErrorModalClose}>
                    <p>Eroare: {errors['api']?.message}</p>
                </InfoModal>
                <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                    <FormPassword
                        id={'password'}
                        label={'Parolă'}
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
                                v == password || 'Parola și confirmarea parolei nu se potrivesc.',
                        })}
                    />
                    <button type="submit" className="form-submit" disabled={loading}>
                        {loading ? 'Confirmare...' : 'Confirmare'}
                    </button>
                </form>
            </div>
        </div>
    )
}
