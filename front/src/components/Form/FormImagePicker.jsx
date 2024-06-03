import { FaPencilAlt } from 'react-icons/fa'

function FormImagePicker({ label, id, value, onChange, errorCheck, originalIcon, ...other }) {
    const onInputChange = (e) => {
        onChange(e.target.files[0])
    }

    return (
        <div className="form-item form-image-item">
            <label className="form-label">{label}</label>
            <label htmlFor={id} className="form-image-label">
                <div
                    className="form-image-preview"
                    style={{
                        backgroundImage: value
                            ? `url(${URL.createObjectURL(value)})`
                            : `url(${originalIcon})`,
                    }}
                >
                    <div className="form-image-overlay">
                        <FaPencilAlt />
                    </div>
                </div>
                <input
                    className="form-input"
                    style={{ display: 'none' }}
                    id={id}
                    onChange={onInputChange}
                    type="file"
                    accept="image/*"
                    {...other}
                />
            </label>
            {errorCheck && errorCheck(id)}
        </div>
    )
}

export default FormImagePicker
