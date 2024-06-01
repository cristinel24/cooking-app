import { Controller, FormProvider, useFieldArray, useForm } from 'react-hook-form'
import './index.css'
import { FormInput, RichTextEditor } from '../../components'
import { useEffect, useState } from 'react'
import { RxCross2 } from 'react-icons/rx'
import { TiPlus } from 'react-icons/ti'
import { RecipeEditor } from '../../components/RecipeEditor'

export default function EditRecipe() {
    const [formShowing, setFormShowing] = useState(false)

    const form = useForm()

    const onSubmit = (data) => {
        console.log(data)
    }

    useEffect(() => {
        const fetch = async () => {
            const delay = (ms) => new Promise((res) => setTimeout(res, ms))
            await delay(1200)

            reset({
                description: 'sab sab sab',
                steps: [{ step: 'sabina' }, { step: 'alina' }],
                ingredients: [{ ingredient: 'sabina' }, { ingredient: 'alex' }],
            })
            setFormShowing(true)
        }
        fetch()
    }, [])

    const {
        register,
        control,
        handleSubmit,
        setError,
        reset,
        setValue,
        clearErrors,
        formState: { errors },
    } = form

    return (
        formShowing && (
            <FormProvider {...form}>
                <RecipeEditor onSubmit={onSubmit} submitText="Editează rețeta" />
            </FormProvider>
        )
    )
}
