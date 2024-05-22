import { forwardRef, useState } from 'react'
import { AiOutlineEye, AiOutlineEyeInvisible } from 'react-icons/ai'

const FormPassword = forwardRef(function FormPassword(
    { className, label, id, errorCheck, ...other },
    ref
) {
    const [showPassword, setShowPassword] = useState(false)

    const handleShowPassword = (e) => {
        e.preventDefault(setShowPassword((value) => !value))
    }

    return (
        <div className={`form-item ${className ? className : ''}`}>
            <label className="form-label" htmlFor="password">
                {label}
            </label>
            <input
                className="form-input"
                id={id}
                type={showPassword ? 'text' : 'password'}
                ref={ref}
                {...other}
            ></input>
            <button type="submit" className="form-password-button" onClick={handleShowPassword}>
                {showPassword ? (
                    <AiOutlineEyeInvisible  className="form-password-button-icon" />
                ) : (
                    <AiOutlineEye  className="form-password-button-icon" />
                )}
            </button>
            {errorCheck && errorCheck(id)}
        </div>
    )
})

export default FormPassword
