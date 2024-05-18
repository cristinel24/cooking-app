import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai"

function FormPassword({ register, showPassword, setShowPassword }) {
    const handleShowPassword = e => {
        e.preventDefault(setShowPassword(value => !value))
    }

    return (
        <div className="form-item">
            <label className="form-label" htmlFor="password">
                Password
            </label>
            <input
                className="form-input"
                id="password"
                name="password"
                type={showPassword ? "text" : "password"}
                {...register("password", {
                    required: true,
                })}
            />
            <button type="submit" className="password_button" onClick={handleShowPassword}>
                {showPassword ? (
                    <AiOutlineEyeInvisible className="form-icon" />
                ) : (
                    <AiOutlineEye className="form-icon" />
                )}
            </button>
        </div>
    )
}

export default FormPassword
