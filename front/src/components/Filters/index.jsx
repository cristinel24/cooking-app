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
            prepTime: "prepTime" in filters ? filters.prepTime.toString() : '',
            rating: "rating" in filters ? filters.rating.toString() : '',
        }),
    })

    const onSuggest = (value) => {
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

// /* daca vrei sa folosesti filtre, componenta pe care o vei folosi este ShowMenu*/
// /*componenta asta le tine mereu afisate*/
//
// import { useState } from 'react'
//
// import './index.css'
//
// import { Button } from '../../components'
//
// function Filters() {
//     const [filterSearchTerm, setFilterSearchTerm] = useState('')
//     const [alergenSearchTerm, setAlergenSearchTerm] = useState('')
//
//     const handleFilterSearchChange = (event) => {
//         setFilterSearchTerm(event.target.value)
//     }
//
//     const handleAlergenSearchChange = (event) => {
//         setAlergenSearchTerm(event.target.value)
//     }
//
//     const filters = [
//         'Vegetarian',
//         'Vegan',
//         'Carnivor',
//         'Fara zahar',
//         'High-protein',
//         'Post',
//     ]
//
//     const alergens = ['Lapte', 'Oua', 'Gluten', 'Crustacee', 'Nuci', 'Soia']
//
//     const handleFilterClick = (filterName) => {
//         console.log(`Filter "${filterName}" clicked`)
//     }
//
//     const handleAlergenClick = (alergenName) => {
//         console.log(`Alergen "${alergenName}" clicked`)
//     }
//
//     return (
//         <div className="container1">
//             <div className="filters">
//                 <div className="nameAndSearch1">
//                     <div className="TitluTip">Filtre</div>
//                     <div className="search-bar1">
//                         <input
//                             type="text"
//                             value={filterSearchTerm}
//                             onChange={handleFilterSearchChange}
//                             placeholder="Caută..."
//                         />
//                     </div>
//                 </div>
//                 <div className="filter-buttons">
//                     {filters
//                         .filter((filter) =>
//                             filter
//                                 .toLowerCase()
//                                 .includes(filterSearchTerm.toLowerCase())
//                         )
//                         .map((filter) => (
//                             <Button
//                                 key={filter}
//                                 onClick={() => handleFilterClick(filter)}
//                                 text={filter}
//                             />
//                         ))}
//                 </div>
//                 <div className="alergens">
//                     <div className="nameAndSearch2">
//                         <div className="TitluTip">Alergeni</div>
//                         <div className="search-bar2">
//                             <input
//                                 type="text"
//                                 value={alergenSearchTerm}
//                                 onChange={handleAlergenSearchChange}
//                                 placeholder="Caută..."
//                             />
//                         </div>
//                     </div>
//                     <div className="alergen-buttons">
//                         {alergens
//                             .filter((alergen) =>
//                                 alergen
//                                     .toLowerCase()
//                                     .includes(alergenSearchTerm.toLowerCase())
//                             )
//                             .map((alergen, index) => (
//                                 <Button
//                                     key={index}
//                                     onClick={() => handleAlergenClick(alergen)}
//                                     text={alergen}
//                                 />
//                             ))}
//                     </div>
//                 </div>
//             </div>
//         </div>
//     )
// }
// export default Filters
