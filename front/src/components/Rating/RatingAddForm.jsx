import { useForm } from 'react-hook-form'
import { FormTextarea } from '..'
import RatingButton from './RatingButton'
import { useEffect } from 'react'

const RatingAddForm = ({ defaultValue, onSubmit, onCancel }) => {
    const { register, handleSubmit, formState, setValue } = useForm({
        defaultValues: {
            text: defaultValue,
        },
    })
    useEffect(() => {
        setValue('text', defaultValue)
    }, [defaultValue])
    return (
        <form id="form" className="form rating-card-form" onSubmit={handleSubmit(onSubmit)}>
            <FormTextarea
                className="rating-card-textarea"
                {...register('text')}
                placeholder="Scrie comentariul..."
            />
            <div className="rating-card-buttons">
                <RatingButton type="button" onClick={onCancel}>
                    Anulează
                </RatingButton>
                <RatingButton type="submit">Confirmă</RatingButton>
            </div>
        </form>
    )
}

export default RatingAddForm
