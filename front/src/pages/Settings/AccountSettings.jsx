import { Controller, useForm } from 'react-hook-form'
import { FormImagePicker, FormInput, InfoModal } from '../../components'
import { length } from '../../utils/form'
import { useOutletContext } from 'react-router-dom'
import { FormSelector } from '../../components/Form'
import { getAllergens } from '../../services/allergens'
import { useContext, useState } from 'react'
import { getErrorMessage } from '../../utils/api'
import { updateProfile } from '../../services/profile'
import { UserContext } from '../../context'
import { uploadImage } from '../../services/image'

export default function AccountSettings() {
    const {
        register,
        control,
        handleSubmit,
        setError,
        clearErrors,
        formState: { errors },
    } = useForm()
    const profile = useOutletContext()
    const [loading, setLoading] = useState(false)
    const { user, token } = useContext(UserContext)

    const onErrorModalClose = () => {
        clearErrors('api')
    }

    const onSubmit = async (data) => {
        setLoading(true)
        try {
            const icon = await uploadImage(token, data.icon)
            delete data.allergens
            await updateProfile(user.id, token, { ...data, icon })
        } catch (e) {
            setError('api', { message: getErrorMessage(e) })
        } finally {
            setLoading(false)
        }
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
        <div className="settings-page">
            <form id="form" className="form">
                <FormInput
                    label="Nume"
                    id="displayName"
                    defaultValue={profile.displayName}
                    errorCheck={errorCheck}
                    {...register('displayName', {
                        minLength: length('minim', 4),
                        maxLength: length('maxim', 64),
                    })}
                />
                <Controller
                    name="allergens"
                    control={control}
                    defaultValue={profile.allergens}
                    render={({ field }) => (
                        <FormSelector
                            label="Alergeni"
                            id={field.name}
                            value={field.value}
                            onChange={field.onChange}
                            onBlur={field.onBlur}
                            suggest={getAllergens}
                        />
                    )}
                />
                <Controller
                    name="icon"
                    control={control}
                    render={({ field }) => (
                        <FormImagePicker
                            label="Iconiță"
                            id={field.name}
                            value={field.value}
                            onChange={field.onChange}
                            originalIcon={profile.icon}
                        />
                    )}
                />
                {/* TODO: RTE */}
                {errors['api'] && (
                    <InfoModal isOpen={Boolean(errors['api'])} onClose={onErrorModalClose}>
                        <p className="form-error">{errors['api'].message}</p>
                    </InfoModal>
                )}
            </form>
            <button
                onClick={handleSubmit(onSubmit)}
                className="form-submit settings-submit"
                disabled={loading}
            >
                {loading ? 'Actualizare date...' : 'Salvați schimbările'}
            </button>
        </div>
    )
}
