import Modal from 'react-modal'
import './index.css'

export default function GenericModal({
    isOpen,
    onAfterOpen,
    onRequestClose,
    contentLabel,
    children,
}) {
    return (
        <Modal
            isOpen={isOpen}
            contentLabel="Example Modal"
            className="modal"
            overlayClassName="modal-overlay"
        >
            <div className="modal-title-bar">
                <h1>{contentLabel}</h1>
                {/* buton de close */}
                <button type="button" onClick={onRequestClose}>
                    Inchide
                </button>
            </div>
            <div className="modal-content">{children}</div>
        </Modal>
    )
}
