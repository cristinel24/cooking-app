import { useForm, Controller } from 'react-hook-form'
import { FormStars, FormTextarea, InfoModal } from '..'
import RatingButton from './RatingButton'
import { useEffect, useState } from 'react'
import { getErrorMessage } from '../../utils/api'

const RatingForm = ({ defaultValues, onSubmit, onCancel, id, confirmText = 'Confirmă' }) => {
    const {
        register,
        handleSubmit,
        reset,
        setValue,
        control,
        setError,
        clearErrors,
        formState: { errors },
    } = useForm({
        defaultValues: defaultValues,
    })

    const [isSuccessful, setIsSuccessful] = useState(false)

    useEffect(() => {
        reset(defaultValues)
    }, [defaultValues])

    useEffect(() => {
        if (isSuccessful) {
            reset(defaultValues)
        }
        setIsSuccessful(false)
    }, [isSuccessful])

    const onRatingChange = (data) => {
        setValue('rating', data)
    }

    const errorCheck = (id) => {
        console.log(`error checking ${id}`)
        if (errors[id]) {
            if (errors[id].type == 'required') {
                return <p className="form-error">Acest câmp este obligatoriu</p>
            }

            return <p className="form-error">{errors[id].message}</p>
        }
    }

    const submitForm = async (data) => {
        try {
            await onSubmit(data)
            setIsSuccessful(true)
        } catch (e) {
            setError('api', {
                message: getErrorMessage(e),
            })
        }
    }

    const onCloseModal = () => {
        clearErrors('api')
    }

    return (
        <form
            id={`form-${id ? id : ''}`}
            className="form rating-card-form"
            onSubmit={handleSubmit(submitForm)}
        >
            {errors['api'] && (
                <InfoModal isOpen={Boolean(errors['api'])} onClose={onCloseModal}>
                    <p className="form-error">{errors['api'].message}</p>
                </InfoModal>
            )}
            {defaultValues.rating !== undefined && (
                <>
                    <div className="rating-card-form-stars">
                        <Controller
                            control={control}
                            name="rating"
                            render={({ field: { onChange, value } }) => (
                                <FormStars
                                    key={`rating-${id ? id : ''}`}
                                    id="rating"
                                    onChange={onChange}
                                    errorCheck={errorCheck}
                                    value={value}
                                />
                            )}
                        />
                        <RatingButton
                            type="button"
                            onClick={() => {
                                onRatingChange(0)
                            }}
                        >
                            Resetează nota
                        </RatingButton>
                    </div>
                    <p>
                        <em>(Recenziile cu nota 0 sunt considerate comentarii.)</em>
                    </p>
                </>
            )}

            {defaultValues.text !== undefined && (
                <FormTextarea
                    id="text"
                    className="rating-card-textarea"
                    {...register('text')}
                    errorCheck={errorCheck}
                    placeholder="Scrie comentariul..."
                />
            )}
            <div className="rating-card-buttons">
                {onCancel && (
                    <RatingButton type="button" onClick={onCancel}>
                        Anulează
                    </RatingButton>
                )}
                <RatingButton type="submit">{confirmText}</RatingButton>
            </div>
        </form>
    )
}

export default RatingForm
