import { Controller, useFieldArray, useForm } from 'react-hook-form'
import './index.css'
import { FormInput, RichTextEditor } from '../../components'
import { useEffect } from 'react'
import { RxCross2 } from 'react-icons/rx'
import { TiPlus } from 'react-icons/ti'

export default function AddRecipe() {
    // TODO: if not logged in, show a "you must be logged in" message

    const {
        register,
        control,
        handleSubmit,
        setError,
        reset,
        clearErrors,
        formState: { errors },
    } = useForm({
        defaultValues: {
            steps: [{ step: '' }],
            ingredients: [{ ingredient: '' }],
        },
    })

    const {
        fields: ingredients,
        append: appendIngredient,
        remove: removeIngredient,
    } = useFieldArray({
        control,
        name: 'ingredients',
    })
    const {
        fields: steps,
        append: appendStep,
        remove: removeStep,
    } = useFieldArray({
        control,
        name: 'steps',
    })

    return (
        <form onSubmit={handleSubmit((data) => console.log(data))}>
            <div className="recipe-editor">
                <div className="recipe-editor-grid">
                    <h4>Titlu</h4>
                    <FormInput id={`title`} {...register(`title`)} />
                    <h4>Timp de preparare</h4>
                    {/* spinner */}
                    <FormInput id={`prepTime`} {...register(`prepTime`)} />
                </div>
                <h4>Descriere</h4>
                <Controller
                    render={({ field: { onChange, value } }) => (
                        <RichTextEditor defaultValue={value} onChange={onChange} />
                    )}
                    name={`description`}
                    control={control}
                />
            </div>
            <div className="recipe-editor-row">
                <h4>Ingrediente</h4>
                <button
                    type="button"
                    className="recipe-editor-button"
                    onClick={() => appendIngredient({ ingredient: '' })}
                >
                    <TiPlus />
                </button>
            </div>
            <div className="recipe-editor-field-array-container">
                {ingredients.map((item, index) => (
                    <div className="recipe-editor-row" key={item.id}>
                        <FormInput
                            placeholder={'Scrie aici un ingredient...'}
                            id={`ingredient-${index}`}
                            {...register(`ingredients.${index}.ingredient`)}
                        />
                        <button
                            type="button"
                            className="recipe-editor-button"
                            onClick={() => removeIngredient(index)}
                        >
                            <RxCross2 />
                        </button>
                    </div>
                ))}
            </div>
            <div className="recipe-editor-row">
                <h4>Pași</h4>
                <button
                    type="button"
                    className="recipe-editor-button"
                    onClick={() => appendStep({ step: '' })}
                >
                    <TiPlus />
                </button>
            </div>
            <div className="recipe-editor-field-array-container">
                {steps.map((item, index) => (
                    <Controller
                        render={({ field: { onChange, value } }) => (
                            <RichTextEditor
                                key={item.id}
                                defaultValue={value.step}
                                onRemove={() => removeStep(index)}
                                onChange={onChange}
                            />
                        )}
                        name={`steps.${index}.step`}
                        control={control}
                    />
                ))}
            </div>
            <input type="submit" />
        </form>
    )
}
