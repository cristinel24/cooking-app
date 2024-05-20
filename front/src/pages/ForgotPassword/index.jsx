import { useForm } from 'react-hook-form'

import './index.css'

import { FormInput } from '../../components'
import { useState } from 'react'
import { length } from '../../utils/form'

export default function ForgotPassword() {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm()
    const [submit, setSubmit] = useState(false)

    const onSubmit = async (data) => {
        console.log(data)

        setSubmit(true)

        // TODO: error handling for API

        // const { token, user } = await login(data)
        // loginContext(token, user, remember)
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
        <div className="page">
            <div className="form-container">
                <h2>Resetare parolă</h2>
                <p>
                    Dacă v-ați uitat parola, completați email-ul dumneavoastră aici pentru a primi
                    un link de resetare a parolei.
                </p>
                <form id="form" className="form" onSubmit={handleSubmit(onSubmit)}>
                    <FormInput
                        label="Email"
                        id="identifier"
                        type="email"
                        errorCheck={errorCheck}
                        {...register('identifier', {
                            required: true,
                            maxLength: length('maxim', 256),
                        })}
                    />
                    <button
                        {...(submit ? { disabled: true } : {})}
                        type="submit"
                        className="form-submit"
                    >
                        Trimitere email
                    </button>
                    {submit && <p>Email-ul a fost trimis, puteți închide această pagină acum.</p>}
                </form>
            </div>
        </div>
    )
}
