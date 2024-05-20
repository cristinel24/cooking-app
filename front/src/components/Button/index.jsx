import './index.css'

function Button({ className, onClick, text, Icon, iconAfter }) {
    return (
        <button type="button" className={`action-button ${className}`} onClick={onClick}>
            {!iconAfter && Icon && <Icon className="action-button-icon" />}
            {text && <span className="action-button-text">{text}</span>}
            {iconAfter && Icon && <Icon className="action-button-icon" />}
        </button>
    )
}

export default Button
