import { useState } from 'react'
import { LuSend } from "react-icons/lu";
import { MdOutlineCancel } from "react-icons/md";

import './index.css'

import { Button } from '../../components'

function ReportRecipe() {
    const [formVariants, setFormVariants] = useState([
        { id: 1, text: 'Continut sexual', checked: false },
        { id: 2, text: 'Continut respingator/violent', checked: false },
        { id: 3, text: 'Continut instigator la ura/abuziv', checked: false },
        { id: 4, text: 'Hartuire sau intimidare', checked: false },
        { id: 5, text: 'Dezinformare', checked: false },
        { id: 6, text: 'Continut fals', checked: false },
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
            <div className="report-recipe-wrapper">
                <div className="report-recipe-wrapper-title">
                    <p>Raporteaza</p>
                </div>
                <div className="report-recipe-content">
                    <form className="report-recipe-form">
                        {formVariants.map((variant) => (
                            <div className="report-recipe-inputs" key={variant.id}>
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
                <div className="report-recipe-buttons">
                    <div className="report-recipe-send-button">
                        <Button
                            text="Trimite"
                            Icon={LuSend}
                            onClick={fuctionForButton}
                        />
                    </div>
                    <div className="report-recipe-give-up-button">
                        <Button
                            text="Renunta"
                            Icon={MdOutlineCancel}
                            onClick={fuctionForButton}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ReportRecipe
