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
        <div className="pop-up-chat-container">
            <img
                src={botLogo}
                alt="Logo"
                className="pop-up-chat-bot-logo"
                onClick={toggleModal}
            />
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={toggleModal}
                contentLabel="chat-modal"
                className="pop-up-chat-modal-content"
                overlayClassName="pop-up-chat-modal-overlay"
            >
                <div className="pop-up-chat-title">
                    <h2>Chat</h2>
                </div>
                <div className="pop-up-chat-conversation">
                    <p>Chatul tău va fi aici...</p>
                </div>
            </Modal>
        </div>
    )
}

export default PopUpChat
