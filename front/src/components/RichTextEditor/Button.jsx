import './index.css'

export const Button = ({ title, onClick, disabled, className, Icon, active }) => {
    return (
        <button
            type="button"
            title={title}
            onClick={onClick}
            disabled={disabled}
            className={
                'rich-text-editor-button' +
                (className ? ' ' + className : '') +
                (active ? ' rich-text-editor-button-active' : '')
            }
        >
            {Icon && <Icon className="rich-text-editor-button-icon" />}
        </button>
    )
}
