import './index.css'
import '../index'

export default function Dropdown({ options, option, setOption }) {
    return (
        <select 
            className="dropdown-item" 
            value={option} 
            onChange={(event) => setOption(event.target.value)}
        >
            {options.map((option) => (
                <option key={option} value={option} className="dropdown-option">
                    {option}
                </option>
            ))}
        </select>
    )
}
