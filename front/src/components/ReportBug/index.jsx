import { useState, useRef } from 'react'

import './index.css'

import { Button } from '../../components';

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
        <div>
            <div className="report-bug-wrapper">
                <div className="report-bug-wrapper-title">
                    <p>Raportează o problemă!</p>
                </div>
                <p>Descrie problema</p>
                <div className="report-bug-textbox-container">
                    <textarea
                        value={text}
                        onChange={handleChange}
                        placeholder="Atunci când utilizam aplicația, am întâlnit eroarea..."
                    />
                </div>
                <p>O captură de ecran ne-ar ajuta să înțelegem mai bine</p>
                <div className="report-bug-image-container">
                    <div className="report-bug-upload-file">
                        <input
                            ref={fileInputRef}
                            type="file"
                            onChange={handleFileChange}
                            className="report-bug-hide-initial-msg"
                        />
                        <div
                            className="report-bug-upload-button"
                            onClick={handleButtonClick}
                        >
                            {/* <FontAwesomeIcon icon={faPaperclip} /> */}
                            <span>
                                {selectedFile
                                    ? selectedFile.name
                                    : 'Încarcă o captură de ecran'}
                            </span>
                        </div>
                    </div>
                </div>
                <div className="report-bug-buttons">
                    <div className="report-bug-send-button">
                        <Button
                            className="report-bug-button1"
                            text="Trimite"
                            onClick={() => {
                                props.onSend({
                                    text: text,
                                    file: selectedFile,
                                })
                            }}
                        />
                    </div>
                    <div className="report-bug-give-up-button">
                        <Button
                            className="report-bug-button2"
                            text="Renunță"
                            onClick={props.onGiveUp}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}
