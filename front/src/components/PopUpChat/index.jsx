import { useContext, useEffect, useRef, useState } from 'react'
import Modal from 'react-modal'
import { SyncLoader } from 'react-spinners'

import './index.css'

import { UserContext } from '../../context'
import { getResponse } from '../../services/chatbot'
import { getErrorMessage } from '../../utils/api'

function ChatMessage({ message, icon, left, loading }) {
    return (
        <div className={`pop-up-message pop-up-message-${left ? 'left' : 'right'}`}>
            {loading ? (
                <SyncLoader
                    size={8}
                    color="#eeeeee50"
                    speedMultiplier={0.5}
                    cssOverride={{ alignSelf: 'center' }}
                />
            ) : (
                <p className="pop-up-message-content">{message}</p>
            )}
            <img className="pop-up-message-icon" src={icon} alt="Participant icon"></img>
        </div>
    )
}

function PopUpChat() {
    const [error, setError] = useState('')
    const [message, setMessage] = useState('')
    const [loading, setLoading] = useState(false)
    const [modalIsOpen, setModalIsOpen] = useState(false)
    const [conversation, setConversation] = useState([])
    const { token, user } = useContext(UserContext)

    const ref = useRef()

    // scroll to bottom when a new message gets added
    useEffect(() => {
        if (ref.current) {
            ref.current.scrollIntoView(false)
        }
    }, [conversation])

    useEffect(() => {

    })

    const handleInputChange = (event) => {
        setMessage(event.target.value)
        setError('')
    }

    const handleKeyPress = async (event) => {
        if (event.code != 'Enter' || loading) {
            return
        }

        setError('')
        setConversation((prevConversation) => [...prevConversation, message])
        setLoading(true)

        try {
            const response = await getResponse(token, message)
            setConversation((prevConversation) => [...prevConversation, response])
            setMessage('')
        } catch (e) {
            setConversation((prevConversation) =>
                prevConversation.slice(0, prevConversation.length - 1)
            )
            setError(getErrorMessage(e))
        } finally {
            setLoading(false)
        }
    }

    const toggleModal = () => {
        setModalIsOpen(!modalIsOpen)
    }

    return (
        <div className="pop-up-chat-container">
            <img src="/bot.png" alt="Logo" className="pop-up-chat-logo" onClick={toggleModal} />
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={toggleModal}
                contentLabel="chat-modal"
                className="pop-up-chat-modal-content"
                overlayClassName="pop-up-chat-modal-overlay"
                ariaHideApp={false}
            >
                <h2 className="pop-up-chat-title">Sesiune live</h2>
                <div className="pop-up-chat-messages">
                    {conversation.map((message, index) => (
                        <ChatMessage
                            key={index}
                            message={message}
                            icon={index % 2 == 0 ? user.icon : '/bot.png'}
                            left={index % 2 == 1}
                        />
                    ))}
                    {loading && <ChatMessage icon="/bot.png" left loading />}
                    {error && <div className="pop-up-chat-error">{error}</div>}
                    <div ref={ref} />
                </div>
                <input
                    className={`pop-up-chat-input ${loading ? 'loading' : ''}`}
                    type="text"
                    value={message}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyPress}
                    placeholder="Scrie un mesaj..."
                    disabled={loading}
                />
            </Modal>
        </div>
    )
}

export default PopUpChat
