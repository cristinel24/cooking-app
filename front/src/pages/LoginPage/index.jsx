import { useState } from 'react'
import './index.css'
import photo from '/autentificare.png'
import eyeIcon from '/eye.svg'
import { Page } from '../../components'
import { Link } from 'react-router-dom'

const LoginPage = () => {
    const [data, setData] = useState({
        identifier: '',
        password: '',
    })
    const [showPassword, setShowPassword] = useState(false)

    const handleSubmit = (e) => {
        e.preventDefault()

        console.log(data)
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
        <Page>
            <div className="page">
                <div className="form-container">
                    <h2>Autentificare</h2>
                    <form id="form" className="form" onSubmit={handleSubmit}>
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
                                    Parola
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
                            <span>Tine-ma minte</span>
                            <Link className="form-link" to="/forgot-password">
                                Ti-ai uitat parola?
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
                        <Link className="form-link" to="/RegisterPage">
                            Inregistreaza-te
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
        </Page>
    )
}

export default LoginPage
