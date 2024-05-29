import { useForm, Controller } from 'react-hook-form'
import { FormStars, FormTextarea, InfoModal } from '..'
import RatingButton from './RatingButton'
import { useEffect, useState } from 'react'
import { getErrorMessage } from '../../utils/api'
import { length } from '../../utils/form'
import { ClipLoader } from 'react-spinners'

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

    const [isSubmitCallbackLoading, setIsSubmitCallbackLoading] = useState(false)
    const [isSubmitCallbackSuccessful, setIsSubmitCallbackSuccessful] = useState(false)

    useEffect(() => {
        reset(defaultValues)
    }, [defaultValues])

    useEffect(() => {
        reset(defaultValues)
        if (isSubmitCallbackSuccessful) {
            setIsSubmitCallbackSuccessful(false)
        }
    }, [isSubmitCallbackSuccessful])

    const onRatingChange = (data) => {
        setValue('rating', data)
    }

    const errorCheck = (id) => {
        if (errors[id]) {
            if (errors[id].type == 'required') {
                return <p className="form-error">Acest câmp este obligatoriu</p>
            }

            return <p className="form-error">{errors[id].message}</p>
        }
    }

    const submitForm = async (data) => {
        try {
            if (isSubmitCallbackLoading) {
                return
            }
            setIsSubmitCallbackLoading(true)
            await onSubmit(data)
            setIsSubmitCallbackSuccessful(true)
        } catch (e) {
            setError('api', {
                message: getErrorMessage(e),
            })
        } finally {
            setIsSubmitCallbackLoading(false)
        }
    }

    const onCloseModal = () => {
        clearErrors('api')
    }

    return (
        <form
            id={`form-${id !== undefined ? id : ''}`}
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

            {defaultValues.description !== undefined && (
                <FormTextarea
                    id="description"
                    className="rating-card-textarea"
                    errorCheck={errorCheck}
                    placeholder="Scrie comentariul..."
                    {...register('description', {
                        required: true,
                        maxLength: length('maxim', 10000),
                    })}
                />
            )}
            <div className="rating-card-buttons">
                {onCancel && (
                    <RatingButton type="button" onClick={onCancel}>
                        Anulează
                    </RatingButton>
                )}

                <ClipLoader
                    className="loading"
                    cssOverride={{
                        borderColor: 'var(--text-color)',
                        color: 'var(--text-color)',
                        alignSelf: 'center',
                    }}
                    width={'100%'}
                    loading={isSubmitCallbackLoading}
                    aria-label="Se încarcă..."
                    data-testid="loader"
                />
                {!isSubmitCallbackLoading && (
                    <RatingButton type="submit">{confirmText}</RatingButton>
                )}
            </div>
        </form>
    )
}

export default RatingForm
