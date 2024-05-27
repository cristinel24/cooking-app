import { forwardRef } from 'react'

const FormCheckbox = forwardRef(function FormCheckbox({ label, id, ...other }, ref) {
    return (
        <div>
            <input type="checkbox" id={id} ref={ref} {...other} />
            <label htmlFor={id}>{label}</label>
        </div>
    )
})

export default FormCheckbox
