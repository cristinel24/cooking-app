import { Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'

import './index.css'

import photo from '/register.png'
import { FormInput, FormPassword, length } from '../../components'
import { registerUser } from '../../services/auth'

export default function Register() {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors },
    } = useForm()

    const onSubmit = async (data) => {
        console.log(data)

        // Validate input fields
        if (data.password !== data.confirmPassword) {
            setError('submit', { message: 'Parola și confirmarea parolei nu se potrivesc.' })
            return
        }

        data.confirmPassword = undefined
        await registerUser(data)

        // TODO: error handling for API
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
                            })}
                        />
                    </div>
                    {errorCheck('submit')}
                    <button type="submit" className="form-submit">
                        Înregistrare
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
