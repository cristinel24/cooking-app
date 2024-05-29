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
                <div className="pop-up-user-message" key={prevConversation.length}>
                    {message}
                    <img
                        className="pop-up-image"
                        src={user.icon}
                        //src="https://tazzcdn.akamaized.net/uploads/cover/Cover_Ikura_Sushi_8.png"
                    ></img>
                </div>,
            ])
            event.target.value = null

            setLoading(true)
            try {
                const msg = await getResponse(message)
                console.log(msg)
                setConversation((prevConversation) => [
                    ...prevConversation,
                    <div className="pop-up-chat-message" key={prevConversation.length}>
                        <img className="pop-up-image" src="../public/logo.png"></img>
                        {msg}
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
            {loggedIn() ? (
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
                        <div className="pop-up-chat-conversation">
                            {error && <div className="pop-up-chat-conversation-error">{error}</div>}
                            {conversation.map((item, index) => (
                                <div key={index}>{item}</div>
                            ))}
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
