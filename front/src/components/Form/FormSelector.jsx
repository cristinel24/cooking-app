import { useState } from 'react'
import { Button } from '..'
import { IoClose } from 'react-icons/io5'

function FormSelectorItem({ item, onRemove }) {
    return (
        <Button
            className="form-selector-item"
            onClick={() => onRemove(item)}
            text={item}
            Icon={IoClose}
            iconAfter
        />
    )
}

function FormSelector({ label, id, value, onChange, onBlur, suggest }) {
    const [suggestionsActive, setSuggestionsActive] = useState(false)
    const [inputValue, setInputValue] = useState('')
    const [items, setItems] = useState([])

    const handleInputChange = (e) => {
        const newInputValue = e.target.value
        setInputValue(newInputValue)

        // don't suggest if less than 3 characters were given
        if (!suggest || newInputValue.length < 3) {
            setSuggestionsActive(false)
            setItems([])
            return
        }

        setSuggestionsActive(true)
        setItems(suggest(newInputValue))
    }

    const addItemAndClearSuggestions = (value) => {
        addItem(value)
        // reset state
        setSuggestionsActive(false)
        setInputValue('')
        setItems([])
    }

    const handleInputEnter = (e) => {
        if (e.code != 'Enter') {
            return
        }

        addItemAndClearSuggestions(inputValue)
    }

    const addItem = (item) => {
        if (!value.includes(item)) {
            onChange([...value, item])
        }
    }

    const removeItem = (item) => {
        onChange(value.filter((i) => i !== item))
    }

    window.addEventListener('click', (e) => {
        const selector = document.getElementById(id).parentNode

        if (!selector.contains(e.target)) {
            setSuggestionsActive(false)
            onBlur()
        }
    })

    return (
        <div className="form-item">
            <label htmlFor={id} className="form-label">
                {label}
            </label>
            <input
                autoComplete="off"
                className={`form-input form-selector ${
                    suggestionsActive ? 'form-selector-active' : ''
                }`}
                id={id}
                value={inputValue}
                onChange={handleInputChange}
                onFocus={handleInputChange}
                onKeyUp={handleInputEnter}
            />
            {suggestionsActive && (
                <div className="form-selector-dropdown">
                    <div className="form-selector-dropdown-sep" />
                    <div className="form-selector-dropdown-items">
                        {items.map((item) => (
                            <p
                                className="form-selector-dropdown-item"
                                key={item}
                                onClick={() => {
                                    addItemAndClearSuggestions(item)
                                }}
                            >
                                {item}
                            </p>
                        ))}
                    </div>
                </div>
            )}
            <div className="form-selector-items">
                {value.length > 0 &&
                    value.map((item) => (
                        <FormSelectorItem key={item} item={item} onRemove={removeItem} />
                    ))}
            </div>
        </div>
    )
}

export default FormSelector
