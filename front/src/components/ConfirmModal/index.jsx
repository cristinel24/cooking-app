import './index.css'
import { Button, InfoModal } from '..'
import { LuSend } from 'react-icons/lu'
import { IoClose } from 'react-icons/io5'
import { FaRegCheckCircle } from 'react-icons/fa'
import { FaRegCircleStop } from 'react-icons/fa6'

export default function ConfirmModal({
    isOpen,
    onCancel,
    onConfirm,
    cancelText,
    confirmText,
    children,
}) {
    return (
        <InfoModal isOpen={isOpen} onClose={onCancel}>
            <div className="confirm-modal-content">{children}</div>
            <div className="confirm-modal-buttons">
                <Button
                    Icon={FaRegCircleStop}
                    onClick={onCancel}
                    className="confirm-modal-cancel"
                    text={cancelText}
                />
                <Button
                    Icon={FaRegCheckCircle}
                    onClick={onConfirm}
                    text={confirmText}
                    className="confirm-modal-confirm"
                />
            </div>
        </InfoModal>
    )
}
