import './index.css'

function Button({ className, onClick, text, Icon, iconAfter, disabled }) {
    return (
        <button
            type="button"
            className={`button ${className ? className : ''}`}
            onClick={onClick}
            {...(disabled === true && { disabled: 'disabled' })}
        >
            {!iconAfter && Icon && <Icon className="button-icon" />}
            {text && <span className="button-text">{text}</span>}
            {iconAfter && Icon && <Icon className="button-icon" />}
        </button>
    )
}

export default Button
