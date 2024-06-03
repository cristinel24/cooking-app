import { Controller, useForm } from 'react-hook-form'

import './index.css'

import { FormInput, FormSelector } from '../Form'
import { Button } from '..'
import { useSearch } from '../../hooks/useSearch'

/*
example filters

const filters = {
    ingredients: [],
    tags: [],
    allergens: [],
    authors: [],
    prepTime: 0,
    rating: 3,
    blacklist: {
        ingredients: [],
        tags: [],
        allergens: [],
    },
}
*/

export default function Filters() {
    const { filters, setParam } = useSearch()

    const {
        register,
        control,
        handleSubmit,
        reset,
        setError,
        formState: { errors },
    } = useForm({
        defaultValues: async () => ({
            ...filters,
            prepTime: 'prepTime' in filters ? filters.prepTime.toString() : '',
            rating: 'rating' in filters ? filters.rating.toString() : '',
        }),
    })

    const onSuggest = async (value) => {
        // for testing purposes
        const delay = (ms) => new Promise((res) => setTimeout(res, ms))
        await delay(500)

        return [
            value,
            'nuci cu muci',
            'zahăr cu ceva bun',
            'despre ce vorbești',
            'cartof',
            'pantooooooooooooooooooooooooooooof',
        ]
    }

    const onSubmit = (data) => {
        if (data.prepTime.length > 0) {
            const prepTime = parseInt(data.prepTime)

            if (isNaN(prepTime)) {
                setError('prepTime', { message: 'Câmpul trebuie să conțină un număr' })
                return
            }

            if (!(prepTime > 0 && prepTime % 5 == 0)) {
                setError('prepTime', {
                    message: 'Timpul de preparere trebuie să fie un multiplu de 5 nenul',
                })
                return
            }

            data.prepTime = prepTime
        } else {
            delete data.prepTime
        }

        if (data.rating.length > 0) {
            const rating = parseInt(data.rating)

            if (isNaN(rating)) {
                setError('rating', {
                    message: 'Câmpul trebuie să conțină un număr',
                })
                return
            }

            if (!(0 <= rating && rating <= 5)) {
                setError('rating', { message: 'Nota trebuie să fie un număr între 0 și 5' })
                return
            }

            data.rating = rating
        } else {
            delete data.rating
        }

        setParam('filters', data)
    }

    const errorCheck = (id) => {
        if (errors[id]) {
            return <p className="form-error">{errors[id].message}</p>
        }
    }

    return (
        <div className="search-page-section">
            <h3>Filtre</h3>
            <form id="form" className="form" onSubmit={(e) => e.preventDefault()}>
                <Controller
                    name="ingredients"
                    control={control}
                    defaultValue={[]}
                    render={({ field }) => (
                        <FormSelector
                            label="Ingrediente"
                            id={field.name}
                            value={field.value}
                            onChange={field.onChange}
                            onBlur={field.onBlur}
                        />
                    )}
                />
                <Controller
                    name="tags"
                    control={control}
                    defaultValue={[]}
                    render={({ field }) => (
                        <FormSelector
                            label="Tag-uri"
                            id={field.name}
                            value={field.value}
                            onChange={field.onChange}
                            onBlur={field.onBlur}
                            suggest={onSuggest}
                        />
                    )}
                />
                <Controller
                    name="allergens"
                    control={control}
                    defaultValue={[]}
                    render={({ field }) => (
                        <FormSelector
                            label="Alergeni"
                            id={field.name}
                            value={field.value}
                            onChange={field.onChange}
                            onBlur={field.onBlur}
                            suggest={onSuggest}
                        />
                    )}
                />
                <Controller
                    name="authors"
                    control={control}
                    defaultValue={[]}
                    render={({ field }) => (
                        <FormSelector
                            label="Autori"
                            id={field.name}
                            value={field.value}
                            onChange={field.onChange}
                            onBlur={field.onBlur}
                            suggest={onSuggest}
                        />
                    )}
                />
                <FormInput
                    label="Timp de preparare"
                    id="prepTime"
                    errorCheck={errorCheck}
                    {...register('prepTime')}
                />
                <FormInput
                    label="Notă"
                    id="rating"
                    errorCheck={errorCheck}
                    {...register('rating')}
                />
            </form>
            <Button
                className="filters-button filters-button-secondary"
                text="Curăță filtre"
                onClick={() => reset({ prepTime: '', rating: '' })}
            />
            <Button
                className="filters-button"
                text="Salvează filtre"
                onClick={handleSubmit(onSubmit)}
            />
        </div>
    )
}
