import { useState } from 'react'
import './index.css'
import photo from '/register.png'
import eyeIcon from '/eye.svg'
import { Page } from '../../components'
import { Link } from 'react-router-dom'
import { register } from '../../services/auth'

export default function Register() {
    const [data, setData] = useState({
        username: '',
        displayName: '',
        email: '',
        password: '',
        confirmPassword: '',
    })
    const [passwordVisible, setPasswordVisible] = useState(false)
    const [confirmPasswordVisible, setConfirmPasswordVisible] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault()

        // Validate input fields
        if (data.password !== data.confirmPassword) {
            alert('Parola si Confirmare parola nu se potrivesc.')
            return
        }

        data.confirmPassword = undefined
        await register(data)
    }

    const handleChange = (event) => {
        const { name, value } = event.target
        setData({
            ...data,
            [name]: value,
        })
    }

    const togglePasswordVisibility = () => {
        setPasswordVisible(!passwordVisible)
    }

    const toggleConfirmPasswordVisibility = () => {
        setConfirmPasswordVisible(!confirmPasswordVisible)
    }

    return (
        <div className="page">
            <div className="form-container">
                <h2>Inregistrare</h2>
                <form id="form" className="form" onSubmit={handleSubmit}>
                    <div className="form-row">
                        <div className="form-item">
                            <label
                                htmlFor="username"
                                className="form-label"
                            >
                                Nume de utilizator
                            </label>
                            <input
                                id="username"
                                name="username"
                                value={data.username}
                                onChange={handleChange}
                                className="form-input"
                                required
                                minLength={8}
                                maxLength={64}
                            />
                        </div>
                        <div className="form-item">
                            <label
                                htmlFor="displayName"
                                className="form-label"
                            >
                                Nume
                            </label>
                            <input
                                id="displayName"
                                name="displayName"
                                value={data.displayName}
                                onChange={handleChange}
                                className="form-input"
                                required
                                minLength={4}
                                maxLength={64}
                            />
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-item form-item--full">
                            <label htmlFor="email" className="form-label">
                                Email
                            </label>
                            <input
                                id="email"
                                name="email"
                                value={data.email}
                                onChange={handleChange}
                                className="form-input"
                                type="email"
                                required
                                maxLength={256}
                            />
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-item">
                            <label
                                htmlFor="password"
                                className="form-label"
                            >
                                Parolă
                            </label>
                            <input
                                id="password"
                                name="password"
                                value={data.password}
                                onChange={handleChange}
                                className="form-input form-input-password"
                                type={passwordVisible ? 'text' : 'password'}
                                required
                                minLength={8}
                                maxLength={64}
                            />
                            <img
                                className="form-icon"
                                src={eyeIcon}
                                alt={
                                    passwordVisible
                                        ? 'Hide password'
                                        : 'Show password'
                                }
                                onClick={togglePasswordVisibility}
                            />
                        </div>
                        <div className="form-item">
                            <label
                                htmlFor="confirmPassword"
                                className="form-label"
                            >
                                Confirmare parolă
                            </label>
                            <input
                                id="confirmPassword"
                                name="confirmPassword"
                                value={data.confirmPassword}
                                onChange={handleChange}
                                className="form-input form-input-password"
                                type={
                                    confirmPasswordVisible
                                        ? 'text'
                                        : 'password'
                                }
                                required
                                minLength={8}
                                maxLength={64}
                            />
                            <img
                                className="form-icon"
                                src={eyeIcon}
                                alt={
                                    passwordVisible
                                        ? 'Hide password'
                                        : 'Show password'
                                }
                                onClick={toggleConfirmPasswordVisibility}
                            />
                        </div>
                    </div>
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
                <img
                    className="bg-image"
                    src={photo}
                    alt="photo doesn't appear"
                />
            </div>
        </div>
    )
}
