import { useState } from 'react'
import { LuSend } from 'react-icons/lu'
import { MdOutlineCancel } from 'react-icons/md'

import './index.css'

import { Button, GenericModal } from '../../components'
import { FormCheckboxList } from '../../components'

function Report(props) {
    const [formVariants, setFormVariants] = useState([
        { id: 1, label: 'Conținut sexual', checked: false },
        { id: 2, label: 'Conținut respingător/violent', checked: false },
        { id: 3, label: 'Conținut instigator la ură/abuziv', checked: false },
        { id: 4, label: 'Hărțuire sau intimidare', checked: false },
        { id: 5, label: 'Dezinformare', checked: false },
        { id: 6, label: 'Conținut fals', checked: false },
        { id: 7, label: 'Probleme legale', checked: false },
    ])

    const handleChoice = (choice) => {
        console.log('Selected choice:', choice)
    }

    return (
        <GenericModal className="report" isOpen={true} onRequestClose={props.onCancel}>
            <div className="report-wrapper">
                <p className="report-wrapper-title">Raportează</p>
                <form className="report-input-wrapper">
                    <FormCheckboxList
                        options={formVariants}
                        setOptions={setFormVariants}
                        onChoice={handleChoice}
                        multipleChoice={true}
                    />
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
                            props.onSend(formVariants.filter((variant) => variant.checked))
                        }}
                    />
                </div>
            </div>
        </GenericModal>
    )
}

export default Report
