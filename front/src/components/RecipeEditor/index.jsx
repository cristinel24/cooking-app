import { Controller, useFieldArray, useForm, useFormContext } from 'react-hook-form'
import { FormInput, RichTextEditor } from '../../components'
import './index.css'
import { RxCross2 } from 'react-icons/rx'
import { TiPlus } from 'react-icons/ti'
import { length } from '../../utils/form'

export const RecipeEditor = ({ onSubmit, submitText = 'Trimite' }) => {
    const renderError = (error) => {
        console.log(errors)
        if (error) {
            if (error.type == 'required') {
                return <p className="form-error">Acest câmp este obligatoriu</p>
            }

            return <p className="form-error">{error.message}</p>
        }
    }

    const errorCheck = (id) => {
        return renderError(errors[id])
    }

    const arrayErrorCheck = (id) => {
        const fields = id.split('.')
        try {
            const error = errors[fields[0]][fields[1]][fields[2]]
            return renderError(error)
        } catch (e) {}
    }

    const onSubmitWithErrorChecking = (data) => {
        if (data.prepTime.length > 0) {
            const prepTime = parseInt(data.prepTime)

            if (isNaN(prepTime)) {
                setError('prepTime', { message: 'Câmpul trebuie să conțină un număr' })
                return
            }

            if (!(prepTime > 0 && prepTime % 5 == 0)) {
                setError('prepTime', {
                    message: 'Timpul de preparare trebuie să fie un multiplu de 5 nenul',
                })
                return
            }

            data.prepTime = prepTime
        }
        onSubmit(data)
    }

    const {
        register,
        control,
        handleSubmit,
        setError,
        reset,
        setValue,
        clearErrors,
        formState: { errors },
    } = useFormContext()

    const {
        fields: ingredients,
        append: appendIngredient,
        remove: removeIngredient,
    } = useFieldArray({
        control,
        name: 'ingredients',
        rules: { required: true },
    })
    const {
        fields: steps,
        append: appendStep,
        remove: removeStep,
    } = useFieldArray({
        control,
        name: 'steps',
        rules: { required: true },
    })

    return (
        <form onSubmit={handleSubmit(onSubmitWithErrorChecking)}>
            <div className="recipe-editor">
                <div className="recipe-editor-grid">
                    <h4>Titlu</h4>
                    <FormInput
                        id={`title`}
                        placeholder={'Titlu...'}
                        errorCheck={errorCheck}
                        {...register(`title`, {
                            required: true,
                            maxLength: length('maxim', 10000),
                        })}
                    />
                    <h4>Timp de preparare</h4>
                    {/* spinner */}
                    <FormInput
                        id={`prepTime`}
                        errorCheck={errorCheck}
                        {...register(`prepTime`, {
                            required: true,
                        })}
                    />
                </div>
                <h4>Descriere</h4>
                <Controller
                    defaultValue={''}
                    render={({ field: { onChange, value } }) => (
                        <RichTextEditor value={value} onChange={onChange} errorCheck={errorCheck} />
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
                            id={`ingredients.${index}.ingredient`}
                            errorCheck={arrayErrorCheck}
                            {...register(`ingredients.${index}.ingredient`, {
                                required: true,
                            })}
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
                {errors?.ingredients?.root && renderError(errors.ingredients?.root)}
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
                        key={item.id}
                        render={({ field: { onChange, value } }) => (
                            <RichTextEditor
                                value={value}
                                id={`steps.${index}.step`}
                                errorCheck={arrayErrorCheck}
                                onRemove={() => removeStep(index)}
                                onChange={onChange}
                            />
                        )}
                        name={`steps.${index}.step`}
                        control={control}
                    />
                ))}
                {errors?.steps?.root && renderError(errors.steps.root)}
            </div>
            <div className="recipe-editor-center-row">
                <button type="submit" className="form-submit">
                    {submitText}
                </button>
            </div>
        </form>
    )
}
