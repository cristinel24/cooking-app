import './index.css'
import '../index'

export default function Dropdown({ options, option, setOption }) {
    return (
        <select
            className="dropdown-item"
            value={option.name}
            onChange={(event) =>
                setOption(options.find((option) => option.name === event.target.value))
            }
        >
            {options.map((option) => (
                <option key={option.name} value={option.name} className="dropdown-option">
                    {option.name}
                </option>
            ))}
        </select>
    )
}
