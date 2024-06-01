import { Controller, FormProvider, useFieldArray, useForm } from 'react-hook-form'
import './index.css'
import { FormInput, RichTextEditor } from '../../components'
import { useEffect, useState } from 'react'
import { RxCross2 } from 'react-icons/rx'
import { TiPlus } from 'react-icons/ti'
import { RecipeEditor } from '../../components/RecipeEditor'

export default function AddRecipe() {
    const onSubmit = (data) => {
        console.log(data)
    }
    const form = useForm()
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
        <FormProvider {...form}>
            <RecipeEditor onSubmit={onSubmit} submitText="Adaugă rețetă" />
        </FormProvider>
    )
}
