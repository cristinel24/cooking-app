import { useContext, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

import photo from '/autentificare.png'
import eyeIcon from '/eye.svg'

import './index.css'
import { UserContext } from '../../context/user-context'
import { login as loginApi } from '../../services/auth'

export default function Login() {
    const {
        register, handleSubmit, formState: { errors }
    } = useForm()

    const { login } = useContext(UserContext)
    const navigate = useNavigate()

    const [showPassword, setShowPassword] = useState(false)

    const onSubmit = async (data) => {
        console.log(data)
        return
        // const { token, user } = await login(data)
        // loginContext(token, user)
        login("1234", {
            id: "1",
            username: "jimmy07_dylan04",
        })

        navigate("/")
    }

    const togglePasswordVisibility = () => {
        setShowPassword(!showPassword)
    }

    return (
        <div className="page">
            <div className="form-container">
                <h2>Autentificare</h2>
                <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                    <div className="form-row">
                        <div className="form-item form-item--full">
                            <label
                                htmlFor="identifier"
                                className="form-label"
                            >
                                Nume de utilizator sau email
                            </label>
                            <input
                                id="identifier"
                                className="form-input"
                                {...register("identifier", { required: true, maxLength: 256 })}
                            />
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-item form-item--full">
                            <label
                                htmlFor="password"
                                className="form-label"
                            >
                                Parolă
                            </label>
                            <input
                                type={showPassword ? 'text' : 'password'}
                                id="password"
                                className="form-input"
                                {...register("password", { required: true, minLength: 8, maxLength: 64 })}
                            />
                            <img
                                src={eyeIcon}
                                alt="Toggle password visibility"
                                className="form-icon"
                                onClick={togglePasswordVisibility}
                            />
                        </div>
                    </div>
                    <div className="form-others">
                        <div>
                            <input
                                type="checkbox"
                                id="remember"
                                {...register("remember")}
                            />
                            <label htmlFor="remember">Ține-mă minte</label>
                        </div>
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
                <img
                    className="bg-image"
                    src={photo}
                    alt="photo doesn't appear"
                />
            </div>
        </div>
    )
}
