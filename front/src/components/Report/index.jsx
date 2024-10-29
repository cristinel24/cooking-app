import { useState } from 'react'
import { LuSend } from 'react-icons/lu'
import { MdOutlineCancel } from 'react-icons/md'
import { useForm, Controller } from 'react-hook-form'

import './index.css'

import { Button, GenericModal } from '../../components'
import { FormCheckboxList } from '../../components'
import { sendReport } from '../../services/report'
import { getErrorMessage } from '../../utils/api'

function Report(props) {
    const {
        control,
        handleSubmit,
        setError,
        clearErrors,
        formState: { errors },
    } = useForm({
        defaultValues: {
            formVariants: [
                { id: 1, label: 'Conținut sexual', checked: false },
                { id: 2, label: 'Conținut respingător/violent', checked: false },
                { id: 3, label: 'Conținut instigator la ură/abuziv', checked: false },
                { id: 4, label: 'Hărțuire sau intimidare', checked: false },
                { id: 5, label: 'Dezinformare', checked: false },
                { id: 6, label: 'Conținut fals', checked: false },
                { id: 7, label: 'Probleme legale', checked: false },
            ],
        },
    })

    const onSubmit = async (data) => {
        clearErrors('api')
        try {
            const response = await sendReport(
                data.formVariants.filter((variant) => variant.checked)
            )
            if (response.status === 'ok') {
                console.log('Report sent successfully')
                props.onCancel()
            }
        } catch (e) {
            setError('api', { message: getErrorMessage(e) })
        }
    }
    return (
        <GenericModal className="report" isOpen={true} onRequestClose={props.onCancel}>
            <div className="report-wrapper">
                <p className="report-wrapper-title">Raportează</p>
                <form className="report-input-wrapper" onSubmit={handleSubmit(onSubmit)}>
                    <Controller
                        name="formVariants"
                        control={control}
                        render={({ field: { value, onChange } }) => (
                            <FormCheckboxList
                                options={value}
                                setOptions={onChange}
                                onChoice={() => {}}
                                multipleChoice={true}
                            />
                        )}
                    />
                    {errors.api && (
                        <div className="form-error">
                            <p>{errors.api.message}</p>
                        </div>
                    )}
                    <div className="report-buttons">
                        <Button
                            className="report-button-cancel"
                            text="Renunță"
                            Icon={MdOutlineCancel}
                            onClick={props.onCancel}
                        />
                        <Button
                            className="report-send-button"
                            text="Trimite"
                            Icon={LuSend}
                            type="submit"
                        />
                    </div>
                </form>
            </div>
        </GenericModal>
    )
}

export default Report
