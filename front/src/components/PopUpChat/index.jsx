import React, { useContext, useState } from 'react'
import { UserContext } from '../../context'
import Modal from 'react-modal'
import './index.css'
import botLogo from '/bot.png'
import { getResponse } from '../../services/chatbot'

function PopUpChat() {
    const [error, setError] = useState('')
    const [message, setMessage] = useState('')
    const { logout, loggedIn } = useContext(UserContext)
    const [loading, setLoading] = useState(true)
    const [modalIsOpen, setModalIsOpen] = useState(false)

    const handleInputChange = (event) => {
        setMessage(event.target.value)
    }

    const handleKeyPress = async (event) => {
        if (event.key === 'Enter') {
            console.log(message)
            event.target.value = null

            setLoading(true)
            try {
                const msg = await getResponse(message)
                console.log(msg)
            } catch (e) {
                setError('api', { message: getErrorMessage(e) })
            } finally {
                setLoading(false)
            }
            setMessage('')
        }
    }

    const toggleModal = () => {
        setModalIsOpen(!modalIsOpen)
    }

    return (
        <>
            {!loggedIn() ? (
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
                            <input
                                className="pop-up-chat-conversation-input"
                                type="text"
                                value={message}
                                onChange={handleInputChange}
                                onKeyDown={handleKeyPress}
                                placeholder="Scrie un mesaj..."
                            />
                        </div>
                    </Modal>
                </div>
            ) : (
                <></>
            )}
        </>
    )
}

export default PopUpChat
