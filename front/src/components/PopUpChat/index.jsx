import React, { useState } from 'react'
import Modal from 'react-modal'
import './index.css'
import botLogo from '/bot.png'

function PopUpChat() {
    const [modalIsOpen, setModalIsOpen] = useState(false)

    const toggleModal = () => {
        setModalIsOpen(!modalIsOpen)
    }

    return (
        <div className="popUpChat-Container">
            <img
                src={botLogo}
                alt="Logo"
                className="popUpChat-bot-logo"
                onClick={toggleModal}
            />
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={toggleModal}
                contentLabel="Chat Modal"
                className="popUpChat-modal-content"
                overlayClassName="popUpChat-modal-overlay"
            >
                <div className="popUpChat-title">
                    <h2>Chat</h2>
                </div>
                <div className="popUpChat-chat-content">
                    <p>Chatul tău va fi aici...</p>
                </div>
            </Modal>
        </div>
    )
}

export default PopUpChat
