import { useState } from 'react'
import { LuSend } from 'react-icons/lu'
import { MdOutlineCancel } from 'react-icons/md'

import './index.css'

import { Button, GenericModal } from '../../components'

function Report(props) {
    const [formVariants, setFormVariants] = useState([
        { id: 1, text: 'Conținut sexual', checked: false },
        { id: 2, text: 'Conținut respingător/violent', checked: false },
        { id: 3, text: 'Conținut instigator la ură/abuziv', checked: false },
        { id: 4, text: 'Hărțuire sau intimidare', checked: false },
        { id: 5, text: 'Dezinformare', checked: false },
        { id: 6, text: 'Conținut fals', checked: false },
        { id: 7, text: 'Probleme legale', checked: false },
    ])

    const handleVariantChange = (id) => {
        setFormVariants((prevVariants) =>
            prevVariants.map((variant) =>
                variant.id === id ? { ...variant, checked: !variant.checked } : variant
            )
        )
    }

    return (
        <GenericModal className="report" isOpen={true}>
            <div className="report-wrapper">
                <p className="report-wrapper-title">Raportează</p>
                <form className="report-input-wrapper">
                    {formVariants.map((variant) => (
                        <div className="report-inputs" key={variant.id}>
                            <input
                                type="checkbox"
                                id={`variant-${variant.id}`}
                                checked={variant.checked}
                                onChange={() => handleVariantChange(variant.id)}
                            />
                            <label htmlFor={`variant-${variant.id}`}>{variant.text}</label>
                        </div>
                    ))}
                </form>
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
                        onClick={() => {
                            props.onSend(formVariants.filter((variant) => variant.checked === true))
                        }}
                    />
                </div>
            </div>
        </GenericModal>
    )
}

export default Report
