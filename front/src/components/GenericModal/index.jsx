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
    return (
        <Modal
            isOpen={isOpen}
            onAfterOpen={onAfterOpen}
            contentLabel="Example Modal"
            className={`modal ${className ? className : ''}`}
            overlayClassName="modal-overlay"
            ariaHideApp={false}
        >
            <div className="modal-title-bar">
                <h3>{contentLabel}</h3>
                <button type="button" onClick={onRequestClose} className="modal-close-button">
                    <IoIosClose />
                </button>
            </div>
            {children}
        </Modal>
    )
}
