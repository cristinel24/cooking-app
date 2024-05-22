import { useContext } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

import photo from '/autentificare.png'

import './index.css'
import { UserContext } from '../../context/user-context'
import { FormCheckbox, FormInput, FormPassword } from '../../components'
import { length } from '../../utils/form'

export default function Login() {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm()

    const { login } = useContext(UserContext)
    const navigate = useNavigate()

    const onSubmit = async (data) => {
        console.log(data)
        login(
            '1234',
            {
                id: '1',
                username: 'jimmy07_dylan04',
            },
            data.remember
        )

        navigate('/')

        // TODO: error handling for API

        // const { token, user } = await login(data)
        // loginContext(token, user, remember)
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
                    <button type="submit" className="form-submit">
                        Conectare
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
