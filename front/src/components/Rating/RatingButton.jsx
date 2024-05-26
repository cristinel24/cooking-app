const RatingButton = ({ type = 'button', className, onClick, children }) => {
    return (
        <button
            type={type}
            className={`rating-card-button ${className ? className : ''}`}
            onClick={onClick}
        >
            {children}
        </button>
    )
}

export default RatingButton
