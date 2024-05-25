import Modal from 'react-modal'
import './index.css'

import { IoIosClose } from 'react-icons/io'

export default function GenericModal({
    className,
    isOpen,
    onAfterOpen,
    onRequestClose,
    contentLabel,
    children,
}) {
    contentLabel = 'dsfdbffss'
    return (
        <Modal
            isOpen={isOpen}
            contentLabel="Example Modal"
            className={`modal ${className ? className : ''}`}
            overlayClassName="modal-overlay"
        >
            <div className="modal-title-bar">
                <button type="button" onClick={onRequestClose} className="modal-close-button">
                    <IoIosClose />
                </button>
            </div>
            {children}
        </Modal>
    )
}
