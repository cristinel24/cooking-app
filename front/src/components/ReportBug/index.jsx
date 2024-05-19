import { useState, useRef } from 'react'
import './index.css'
import { Button } from '../../components'
import { GoPaperclip } from 'react-icons/go'

export default function ReportBug(props) {
    const [selectedFile, setSelectedFile] = useState(null)
    const fileInputRef = useRef(null)

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

    return (
        <div className="report-bug-wrapper">
            <p className="report-bug-wrapper-title">Raportează o problemă</p>
            <div className="report-bug-input-wrapper">
                <p>Descrie problema:</p>
                <textarea
                    value={text}
                    onChange={handleChange}
                    placeholder="Atunci când utilizam aplicația, am întâlnit eroarea..."
                />
                <p>O captură de ecran ne-ar ajuta să înțelegem mai bine</p>
                <div className="report-bug-upload-input">
                    <input
                        ref={fileInputRef}
                        type="file"
                        onChange={handleFileChange}
                        style={{ display: 'none' }}
                    />
                    <div
                        className="report-bug-upload-input-text"
                        onClick={handleButtonClick}
                    >
                        <GoPaperclip />
                        <span>
                            {selectedFile
                                ? selectedFile.name
                                : 'Încarcă o captură de ecran'}
                        </span>
                    </div>
                </div>
            </div>
            <div className="report-bug-buttons">
                <Button
                    className="report-bug-button-cancel"
                    text="Renunță"
                    onClick={props.onCancel}
                />
                <Button
                    className="report-bug-button-send"
                    text="Trimite"
                    onClick={() => {
                        props.onSend({
                            text: text,
                            file: selectedFile,
                        })
                    }}
                />
            </div>
        </div>
    )
}
