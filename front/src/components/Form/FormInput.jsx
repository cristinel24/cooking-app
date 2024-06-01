import { forwardRef } from 'react'

const FormInput = forwardRef(function FormInput(
    { className, label, id, errorCheck, placeholder, ...other },
    ref
) {
    return (
        <div className={`form-item ${className ? className : ''}`}>
            {label && (
                <label htmlFor={id} className="form-label">
                    {label}
                </label>
            )}
            <input
                className="form-input"
                placeholder={placeholder ? placeholder : ''}
                id={id}
                ref={ref}
                {...other}
            />
            {errorCheck && errorCheck(id)}
        </div>
    )
})

export default FormInput
