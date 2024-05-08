import React, { useState, useEffect, useRef } from 'react'
import './index.css'
import PageButton from '../PageButton/index.jsx'

export default function ReportBug() {
    //Rutele pentru butoane
    const title1 = 'Trimite'
    const title2 = 'Renunta'
    const pathPage = 'https://www.google.ro/'

    //FileUploader
    const [selectedFile, setSelectedFile] = useState(null)
    const fileInputRef = useRef(null)

    const handleFileChange = (event) => {
        const file = event.target.files[0]
        setSelectedFile(file)
    }

    const handleButtonClick = () => {
        fileInputRef.current.click()
    }
    //TextBox
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
                        placeholder="Atunci când utilizăm aplicația, am întâlnit eroarea..."
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
                        <PageButton path={pathPage} className="report-bug-button1">
                            Trimite
                        </PageButton>
                    </div>
                    <div className="report-bug-give-up-button">
                        <PageButton path={pathPage} className="report-bug-button2">
                            Renunță
                        </PageButton>
                    </div>
                </div>
            </div>
        </div>
    )
}
