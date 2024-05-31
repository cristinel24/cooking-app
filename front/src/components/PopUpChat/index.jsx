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
    const [loading, setLoading] = useState(false) 
    const [modalIsOpen, setModalIsOpen] = useState(false)
    const [conversation, setConversation] = useState([])
    const { user } = useContext(UserContext)

    const handleInputChange = (event) => {
        setMessage(event.target.value)
    }

    const handleKeyPress = async (event) => {
        if (event.key === 'Enter' && !loading) {
            event.preventDefault() 
            console.log(message)
            setConversation((prevConversation) => [
                ...prevConversation,
                <div className="pop-up-outgoing-chats">
                    <div className="pop-up-outgoing-chats-img">
                        <img className="pop-up-outgoing-chats-img" src={user.icon} alt="User Icon"></img>
                    </div>
                    <div className="pop-up-outgoing-msg">
                        <div className="pop-up-outgoing-msg-inbox">
                            <p>{message}</p>
                        </div>
                    </div>
                </div>,
            ])
            event.target.value = null

            setLoading(true)
            setError('')
            try {
                const msg = await getResponse(message)
                console.log(msg)
                setConversation((prevConversation) => [
                    ...prevConversation,
                    <div className="pop-up-received-chats">
                        <div className="pop-up-received-chats-img">
                            <img className="pop-up-received-chats-img" src={botLogo} alt="Bot Logo"></img>
                        </div>
                        <div className="pop-up-received-msg">
                            <div className="pop-up-received-msg-inbox">
                                <p>{msg}</p>
                            </div>
                        </div>
                    </div>,
                ])
            } catch (e) {
                setError(getErrorMessage(e))
            } finally {
                setLoading(false)
            }
            setMessage('')
        }
    }

    const getErrorMessage = (error) => {
        return error.message
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
                            <h2>ChatBot Conversation</h2>
                        </div>

                        <div className="pop-up-chat-page">
                            {error && <div className="pop-up-chat-conversation-error">{error}</div>}
                            {!error && (
                                <div className="pop-up-message-inbox">
                                    <div className="pop-up-chats">
                                        <div className="pop-up-message-page">
                                            {conversation.map((item, index) => (
                                                <div key={index}>{item}</div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}

                            <input
                                className={`pop-up-chat-conversation-input ${loading ? 'loading' : ''}`}
                                type="text"
                                value={message}
                                onChange={handleInputChange}
                                onKeyDown={handleKeyPress}
                                placeholder="Scrie un mesaj..."
                                disabled={loading}
                            />
                        </div>
                    </Modal>
                </div>
            ) : null}
        </>
    )
}

export default PopUpChat
