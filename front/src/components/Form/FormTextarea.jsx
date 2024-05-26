import { forwardRef } from 'react'

import TextareaAutosize from 'react-textarea-autosize'

const FormTextarea = forwardRef(function FormInput(
    { className, label, id, errorCheck, grow = true, resize = false, ...other },
    ref
) {
    return (
        <div className={`form-item ${className ? className : ''}`}>
            {label && (
                <label htmlFor={id} className="form-label">
                    {label}
                </label>
            )}
            {grow ? (
                <TextareaAutosize
                    style={resize ? {} : { resize: 'none' }}
                    className="form-input"
                    id={id}
                    ref={ref}
                    {...other}
                />
            ) : (
                <textarea
                    style={resize ? {} : { resize: 'none' }}
                    className="form-input"
                    id={id}
                    ref={ref}
                    {...other}
                />
            )}
            {errorCheck && errorCheck(id)}
        </div>
    )
})

export default FormTextarea
