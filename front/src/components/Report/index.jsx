import React, { useState, useEffect, useRef } from 'react'
import './index.css'
import { ThemeContext, themes } from '../../context/index.jsx'
import PageButton from '../PageButton/index.jsx'
import Page from '../../pages/Page.jsx'

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
            <div className="wrapper">
                <div className="titlu">
                    <p>Raporteza o problema!</p>
                </div>
                <p>Descrie problema</p>
                <div className="textbox-container">
                    <textarea
                        value={text}
                        onChange={handleChange}
                        className="textarea"
                        placeholder="Atunci când utilizam aplicația, am întâlnit eroarea..."
                    />
                </div>
                <p>O captura de ecran ne-ar ajuta sa intelegem mai bine</p>
                <div className="image-container" style={{ textAlign: 'left' }}>
                    <div className="file">
                        <input
                            ref={fileInputRef}
                            type="file"
                            onChange={handleFileChange}
                            style={{ display: 'none' }}
                        />
                        <div
                            className="upload-button"
                            onClick={handleButtonClick}
                        >
                            {/* <FontAwesomeIcon icon={faPaperclip} /> */}
                            <span>
                                {selectedFile
                                    ? selectedFile.name
                                    : 'Incarca o captura de ecran'}
                            </span>
                        </div>
                    </div>
                </div>
                <div className="butoane">
                    <div className="buton1">
                        <PageButton
                            children="Trimite"
                            path={pathPage}
                            className="btn11"
                        />
                    </div>
                    <div className="buton2">
                        <PageButton
                            children="Renunta"
                            path={pathPage}
                            className={'btn22'}
                        />
                    </div>
                </div>
            </div>
        </div>
    )
}
