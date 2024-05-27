import { useForm } from 'react-hook-form'
import { FormInput } from '../../components'
import { length } from '../../utils/form'

export default function AccountSettings() {
    const {
        register,
        handleSubmit,
        formState: { errors }
    } = useForm()

    const onSubmit = async (data) => {
        console.log(data)
    }

    const errorCheck = (id) => {
        if (errors[id]) {
            if (errors[id].type == 'required') {
                return <p className="form-error">Acest câmp este obligatoriu</p>
            }

            return <p className="form-error">{errors[id].message}</p>
        }
    }

    return (
        <div>
            <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                <FormInput
                    label="Nume"
                    id="displayName"
                    errorCheck={errorCheck}
                    {...register('displayName', {
                        minLength: length('minim', 4),
                        maxLength: length('maxim', 64)
                    })}
                />
            </form>
        </div>
    )
}
