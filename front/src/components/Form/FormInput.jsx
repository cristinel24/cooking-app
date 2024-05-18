function FormInput({ register, title, id, type, errorCheck, defaultValue }) {
    return (
        <div className="form-item form-item--full">
            <label htmlFor={id} className="form-label">
                {title}
            </label>
            <input
                className="form-input"
                id={id}
				name={id}
				type={type}
				defaultValue={defaultValue}
				{...register(id, {
					required: true,
				})}
            />
            {errorCheck(id)}
        </div>
    )
}

export default FormInput
