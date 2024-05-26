import { forwardRef } from 'react'

const FormTextarea = forwardRef(function FormTextarea(
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
            <textarea className="form-textarea" id={id} ref={ref} {...other} />
            {errorCheck && errorCheck(id)}
        </div>
    )
})

export default FormTextarea
