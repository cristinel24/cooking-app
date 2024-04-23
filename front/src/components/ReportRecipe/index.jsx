import React, { useState, useEffect } from 'react'
import PageButton from '../PageButton'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './index.css'
function ReportRecipe() {
    const title1 = 'Trimite'
    const title2 = 'Renunta'
    const pathPage = 'https://www.google.ro/'
    localStorage.setItem('theme', 'light')

    // Variantele formularului
    const [formVariants, setFormVariants] = useState([
        { id: 1, text: 'Continut sexual', checked: false },
        { id: 2, text: 'Continut respingator/violent', checked: false },
        { id: 3, text: 'Continut instigator la ura/abuziv', checked: false },
        { id: 4, text: 'Hartuire sau intimidare', checked: false },
        { id: 5, text: 'Dezinformare', checked: false },
        { id: 6, text: 'Continut fals', checked: false },
        { id: 7, text: 'Probleme legale', checked: false },
    ])

    // Funcția pentru actualizarea stării unei variante
    const handleVariantChange = (id) => {
        setFormVariants((prevVariants) =>
            prevVariants.map((variant) =>
                variant.id === id
                    ? { ...variant, checked: !variant.checked }
                    : variant
            )
        )
    }
    return (
        <div>
            <div className="wrapper1">
                <div className="titlu1">
                    <p>Raporteaza</p>
                </div>
                <div className="continut1">
                    <form>
                        {formVariants.map((variant) => (
                            <div className="doamne" key={variant.id}>
                                <input
                                    type="checkbox"
                                    id={`variant-${variant.id}`}
                                    checked={variant.checked}
                                    onChange={() =>
                                        handleVariantChange(variant.id)
                                    }
                                    className="checkbox-style"
                                />
                                <label htmlFor={`variant-${variant.id}`}>
                                    {variant.text}
                                </label>
                            </div>
                        ))}
                    </form>
                </div>
                <div className="butoane1">
                    <div className="button1">
                        <PageButton
                            children={title1}
                            path={pathPage}
                            className="btn1"
                        />
                    </div>
                    <div className="button2">
                        <PageButton
                            children={title2}
                            path={pathPage}
                            className="btn2"
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ReportRecipe
