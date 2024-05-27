import { useContext, useState } from 'react'
import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'

import './index.css'
import photo from '/login-cover.png'

import { UserContext } from '../../context/user-context'
import { FormCheckbox, FormInput, FormPassword, InfoModal } from '../../components'
import { length } from '../../utils/form'
import { loginUser } from '../../services/auth'
import { getErrorMessage } from '../../utils/api'

export default function Login() {
    const {
        register,
        handleSubmit,
        setError,
        clearErrors,
        formState: { errors },
    } = useForm()
    const [loading, setLoading] = useState(false)

    const { login } = useContext(UserContext)

    const onErrorModalClose = () => {
        clearErrors('api')
    }

    const onSubmit = async (data) => {
        setLoading(true)
        try {
            const { sessionToken, user } = await loginUser(data)
            login(sessionToken, user, data.remember)

            // if successful, user will automatically get rerouted to home page
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
                <h2>Autentificare</h2>
                <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                    <FormInput
                        label="Nume de utilizator sau email"
                        id="identifier"
                        errorCheck={errorCheck}
                        {...register('identifier', {
                            required: true,
                            minLength: length('minim', 8),
                            maxLength: length('maxim', 256),
                        })}
                    />
                    <FormPassword
                        label="Parolă"
                        id="password"
                        errorCheck={errorCheck}
                        {...register('password', {
                            require: true,
                            minLength: length('minim', 8),
                            maxLength: length('maxim', 64),
                        })}
                    />
                    <div className="form-others">
                        <FormCheckbox
                            label="Ține-mă minte"
                            id="remember"
                            {...register('remember')}
                        />
                        <Link className="form-link" to="/forgot-password">
                            Ți-ai uitat parola?
                        </Link>
                    </div>
                    {errors['api'] && (
                        <InfoModal isOpen={Boolean(errors['api'])} onClose={onErrorModalClose}>
                            <p className="form-error">{errors['api'].message}</p>
                        </InfoModal>
                    )}
                    <button type="submit" className="form-submit" disabled={loading}>
                        {loading ? 'Conectare...' : 'Conectați-vă'}
                    </button>
                </form>
                <div className="login-separator">
                    <div className="login-separator-line"></div>
                    <span className="login-separator-text">sau</span>
                    <div className="login-separator-line"></div>
                </div>
                <div className="login-external">Conectare cu Google</div>
                <span className="form-others">
                    Nu ai cont?{' '}
                    <Link className="form-link" to="/register">
                        Înregistrează-te
                    </Link>
                </span>
            </div>
            <div className="page-separator"></div>
            <div className="bg-image-container">
                <img className="bg-image" src={photo} alt="login page cover" />
            </div>
        </div>
    )
}
