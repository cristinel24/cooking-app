import { useForm, Controller } from 'react-hook-form'
import { FormStars, FormTextarea } from '..'
import RatingButton from './RatingButton'
import { useEffect } from 'react'

const RatingForm = ({ defaultValues, onSubmit, onCancel, id, confirmText = 'Confirmă' }) => {
    const { register, handleSubmit, formState, reset, setValue, control } = useForm({
        defaultValues: defaultValues,
    })

    useEffect(() => {
        reset(defaultValues)
    }, [defaultValues])

    const onRatingChange = (data) => {
        setValue('rating', data)
    }

    return (
        <form
            id={`form-${id ? id : ''}`}
            className="form rating-card-form"
            onSubmit={handleSubmit(onSubmit)}
        >
            {defaultValues.rating !== undefined && (
                <>
                    <div className="rating-card-form-stars">
                        <Controller
                            control={control}
                            name="rating"
                            render={({ field: { onChange, value } }) => (
                                <FormStars onChange={onChange} value={value} />
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

            <div className="text-sth">
                {defaultValues?.text && (
                    <FormTextarea
                        className="rating-card-textarea"
                        {...register('text')}
                        placeholder="Editează comentariul..."
                    />
                )}
            </div>
            <div className="rating-card-buttons">
                <RatingButton type="button" onClick={onCancel}>
                    Anulează
                </RatingButton>
                <RatingButton type="submit">{confirmText}</RatingButton>
            </div>
        </form>
    )
}

export default RatingForm
