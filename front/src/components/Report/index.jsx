import React, { useState, useEffect, useRef } from 'react'
import './index.css'
import PageButton from '../PageButton/index.jsx'

export default function Report() {
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
            <div className="report-wrapper">
                <div className="report-wrapper-title">
                    <p>Raporteaza o problema!</p>
                </div>
                <p>Descrie problema</p>
                <div className="report-textbox-container">
                    <textarea
                        value={text}
                        onChange={handleChange}
                        className="textarea"
                        placeholder="Atunci când utilizam aplicația, am întâlnit eroarea..."
                    />
                </div>
                <p>O captura de ecran ne-ar ajuta sa intelegem mai bine</p>
                <div className="report-image-container">
                    <div className="report-choose-file">
                        <input ref={fileInputRef}
                         type="file"
                         onChange={handleFileChange}
                         className="report-hide-initial-msg"
                        />
                        <div className="report-upload-button" onClick={handleButtonClick}>
                            {/* <FontAwesomeIcon icon={faPaperclip} /> */}
                            <span>
                                {selectedFile 
                                    ? selectedFile.name 
                                    : 'Incarca o captura de ecran'}
                            </span>
                        </div>
                    </div>
                </div>
                <div className="report-buttons">
                    <div className="report-button1">
                        <PageButton
                            children="Trimite"
                            path={pathPage}
                        />
                    </div>
                    <div className="report-button2">
                        <PageButton
                            children="Renunta"
                            path={pathPage}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}
