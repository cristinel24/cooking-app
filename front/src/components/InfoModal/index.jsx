import Modal from 'react-modal'
import { IoClose } from 'react-icons/io5'

import './index.css'
import { Button } from '..'

export default function InfoModal({ isOpen, onClose, children }) {
    return (
        <Modal
            isOpen={isOpen}
            onRequestClose={onClose}
            className="info-modal"
            overlayClassName="info-modal-overlay"
            ariaHideApp={false}
        >
            <Button Icon={IoClose} onClick={onClose} className="info-modal-close" />
            {children}
        </Modal>
    )
}
