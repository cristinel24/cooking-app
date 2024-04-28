import { useForm } from 'react-hook-form'
import './index.css'

const Form = ({ fields }) => {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm()

    const onSubmit = (data, event) => {
        event.preventDefault()
        console.log(data)
    }
    return (
        <div className="form-container">
            <form onSubmit={handleSubmit(onSubmit)}>
                {fields.map((field, index) => (
                    <div key={index} className="form-field">
                        <input
                            type={field.type}
                            className="form-input-field"
                            placeholder={field.placeholder}
                            {...register(field.name, {
                                required: field.required,
                                minLength: field.minLength,
                                maxLength: field.maxLength,
                            })}
                        />
                        {errors[field.name] && (
                            <div className="form-error-message">
                                Field not valid
                            </div>
                        )}
                    </div>
                ))}
                <input
                    type="submit"
                    className="form-submit-button"
                    value="Submit"
                />
            </form>
        </div>
    )
}

export default Form
