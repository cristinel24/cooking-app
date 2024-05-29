import { useForm } from 'react-hook-form'

import './index.css'

import { FormInput, InfoModal } from '../../components'
import { useState } from 'react'
import { length } from '../../utils/form'
import { credentialChange } from '../../services/auth'
import { getErrorMessage } from '../../utils/api'
import { useNavigate } from 'react-router-dom'

export default function ForgotPassword() {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors }
    } = useForm()

    const navigate = useNavigate()

    const [loading, setLoading] = useState(false)
    const [showModal, setShowModal] = useState(false)

    const onModalClose = () => {
        setShowModal(false)
        navigate('/')
    }

    const onSubmit = async (data) => {
        console.log(data)
        setLoading(true)
        try {
            await credentialChange(data.email, 'password')
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
        <div className="page">
            <div className="form-container">
                <h2>Resetare parolă</h2>
                <p>
                    Dacă v-ați uitat parola, completați email-ul dumneavoastră aici pentru a primi
                    un link de resetare a parolei.
                </p>
                <InfoModal isOpen={showModal} onClose={onModalClose}>
                    <p>Email-ul a fost trimis, puteți închide această pagină acum.</p>
                </InfoModal>
                <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                    <FormInput
                        label="Email"
                        id="identifier"
                        type="email"
                        errorCheck={errorCheck}
                        {...register('identifier', {
                            required: true,
                            maxLength: length('maxim', 256)
                        })}
                    />
                    <button type="submit" className="form-submit" disabled={loading}>
                        {loading ? 'Trimitere email...' : 'Trimiteți email'}
                    </button>
                </form>
            </div>
        </div>
    )
}
