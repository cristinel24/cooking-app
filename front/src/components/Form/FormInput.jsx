import { forwardRef } from 'react'

const FormInput = forwardRef(function FormInput(
    { className, label, id, errorCheck, ...other },
    ref
) {
    return (
        <div className={`form-item ${className ? className : ''}`}>
            {label && (
                <label htmlFor={id} className="form-label">
                    {label}
                </label>
            )}
            <input className="form-input" id={id} ref={ref} {...other} />
            {errorCheck && errorCheck(id)}
        </div>
    )
})

export default FormInput
