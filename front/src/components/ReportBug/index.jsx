import { useState, useRef } from 'react'
import './index.css'
import { Button, FormTextarea, InfoModal } from '../../components'
import { GoPaperclip } from 'react-icons/go'
import { useForm } from 'react-hook-form'

export default function ReportBug(props) {
    const [selectedFile, setSelectedFile] = useState(null)
    const fileInputRef = useRef(null)
    const {
        handleSubmit,
        setError,
        clearErrors,
        formState: { errors },
    } = useForm()

    const onErrorModalClose = () => {
        clearErrors('api')
    }

    const onSubmit = async () => {
        try {
            //try to send the form data
            props.onSend({
                text: text,
                file: selectedFile,
            })
        } catch (e) {
            setError('api', { message: getErrorMessage(e) })
        }
    }

    const handleFileChange = (event) => {
        const file = event.target.files[0]
        setSelectedFile(file)
    }

    const handleButtonClick = () => {
        fileInputRef.current.click()
    }

    const [text, setText] = useState('')

    const handleChange = (event) => {
        setText(event.target.value)
    }

    const errorCheck = (id) => {
        if (errors[id]) {
            return <p className="form-error">{errors[id].message}</p>
        }
    }

    return (
        <div className="report-bug-wrapper">
            <form id="reportForm" className="form" onSubmit={handleSubmit(onSubmit)}>
                <p className="report-bug-wrapper-title">Raportează o problemă</p>
                <div className="report-bug-input-wrapper">
                    <p>Descrie problema:</p>
                    <FormTextarea
                        label="Input text pentru a raporta un bug"
                        id="bugText"
                        errorCheck={errorCheck}
                        value={text}
                        onChange={handleChange}
                        placeholder="Atunci când utilizam aplicația, am întâlnit eroarea..."
                    ></FormTextarea>
                    <p>O captură de ecran ne-ar ajuta să înțelegem mai bine</p>
                    <div className="report-bug-upload-input">
                        <input
                            ref={fileInputRef}
                            type="file"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                            //should be added after FormFile component is created
                            //errorCheck={errorCheck}
                        />
                        <div className="report-bug-upload-input-text" onClick={handleButtonClick}>
                            <GoPaperclip />
                            <span>
                                {selectedFile ? selectedFile.name : 'Încarcă o captură de ecran'}
                            </span>
                        </div>
                    </div>
                </div>
                {errors['api'] && (
                    <InfoModal isOpen={Boolean(errors['api'])} onClose={onErrorModalClose}>
                        <p className="form-error">{errors['api'].message}</p>
                    </InfoModal>
                )}
                <div className="report-bug-buttons">
                    <Button
                        className="report-bug-button-cancel"
                        text="Renunță"
                        onClick={props.onCancel}
                    />
                    <Button
                        className="report-bug-button-send"//class doesn't exist
                        text="Trimite"
                        type="submit"
                    />
                </div>
            </form>
        </div>
    )
}
