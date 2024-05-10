import React, { useState, useEffect } from 'react'
import ActionButton from '../ActionButton'
import './index.css'
import { LuSend } from "react-icons/lu";
import { MdOutlineCancel } from "react-icons/md";
function Report(props) {
    const pathPage = 'https://www.google.ro/'
    localStorage.setItem('theme', 'light')

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
                variant.id === id
                    ? { ...variant, checked: !variant.checked }
                    : variant
            )
        )
    }

    const fuctionForButton = ()=>{}
    return (
        <div>
            <div className="report-wrapper">
                <div className="report-wrapper-title">
                    <p>Raportează</p>
                </div>
                <div className="report-content">
                    <form className="report-form">
                        {formVariants.map((variant) => (
                            <div className="report-inputs" key={variant.id}>
                                <input
                                    type="checkbox"
                                    id={`variant-${variant.id}`}
                                    checked={variant.checked}
                                    onChange={() =>
                                        handleVariantChange(variant.id)
                                    }
                                />
                                <label htmlFor={`variant-${variant.id}`}>
                                    {variant.text}
                                </label>
                            </div>
                        ))}
                    </form>
                </div>
                <div className="report-buttons">
                    <div className="report-send-button">
                        <ActionButton
                            text="Trimite"
                            Icon={LuSend}
                            onClick={() => {
                                props.onSend(
                                    formVariants.filter(
                                        (variant) => variant.checked == true
                                    )
                                )
                            }}
                        />
                    </div>
                    <div className="report-give-up-button">
                        <ActionButton
                            text="Renunță"
                            Icon={MdOutlineCancel}
                            onClick={props.onGiveUp}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Report
