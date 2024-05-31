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
    const [loading, setLoading] = useState(false) // Set initial loading state to false
    const [modalIsOpen, setModalIsOpen] = useState(false)
    const [conversation, setConversation] = useState([])
    const { user } = useContext(UserContext)

    const handleInputChange = (event) => {
        setMessage(event.target.value)
    }

    const handleKeyPress = async (event) => {
        if (event.key === 'Enter') {
            event.preventDefault() // Prevent default form submission behavior
            console.log(message)
            setConversation((prevConversation) => [
                ...prevConversation,
                <div className="outgoing-chats">
                    <div className="outgoing-chats-img">
                        <img
                            className="outgoing-chats-img"
                            src="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                        ></img>
                    </div>
                    <div className="outgoing-msg">
                        <div className="outgoing-msg-inbox">
                            <p>{message}</p>
                        </div>
                    </div>
                </div>,
            ])
            event.target.value = null

            setLoading(true)
            try {
                const msg = await getResponse(message)
                console.log(msg)
                setConversation((prevConversation) => [
                    ...prevConversation,
                    <div className="received-chats">
                        <div className="received-chats-img">
                            <img
                                className="received-chats-img"
                                src="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                            ></img>
                        </div>
                        <div className="received-msg">
                            <div className="received-msg-inbox">
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
                        <div className="chat-page">
                            <div className="msg-inbox">
                                <div className="chats">
                                    <div className="msg-page">{conversation}</div>
                                </div>
                            </div>
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
            ) : null}
        </>
    )
}

export default PopUpChat
