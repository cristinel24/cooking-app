export default function FormCheckboxList({ options, setOptions, onChoice, multipleChoice }) {
    const handleOptionChange = (state, choice) => {
        setOptions((options) =>
            options.map((option) => ({
                ...option,
                // disable other inputs if multipleChoice is not true
                checked:
                    option.id === choice.id
                        ? state === 'on'
                        : Boolean(multipleChoice && option.checked),
            }))
        )
        if (state === 'on') {
            onChoice(choice)
        }
    }

    return (
        <div>
            {options.map((option) => (
                <div className="report-inputs" key={option.id}>
                    <input
                        type="checkbox"
                        id={`option-${option.id}`}
                        checked={option.checked}
                        onChange={(e) => handleOptionChange(e.target.value, option)}
                    />
                    <label htmlFor={`option-${option.id}`}>{option.label}</label>
                </div>
            ))}
        </div>
    )
}
