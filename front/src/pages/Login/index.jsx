import { useContext, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'

import photo from '/autentificare.png'
import eyeIcon from '/eye.svg'

import './index.css'
import { Page } from '../../components'
import { UserContext } from '../../context/user-context'
import { login as loginApi } from '../../services/auth'

export default function Login() {
    const {
        register, handleSubmit, formState: { errors }
    } = useForm()

    const { login } = useContext(UserContext)
    const navigate = useNavigate()

    const [data, setData] = useState({
        identifier: '',
        password: '',
    })
    const [showPassword, setShowPassword] = useState(false)

    const onSubmit = async (e) => {
        // const { token, user } = await login(data)
        // loginContext(token, user)
        login("1234", {
            id: "1",
            username: "jimmy07_dylan04",
        })

        navigate("/")
    }

    const handleChange = (event) => {
        const { name, value } = event.target
        setData({
            ...data,
            [name]: value,
        })
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
                                Username sau email
                            </label>
                            <input
                                id="identifier"
                                name="identifier"
                                className="form-input"
                                value={data.identifier}
                                onChange={handleChange}
                                maxLength={256}
                                required
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
                                name="password"
                                className="form-input"
                                value={data.password}
                                onChange={handleChange}
                                required
                                minLength={8}
                                maxLength={64}
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
                        <span>Ține-mă minte</span>
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
