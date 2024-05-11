import React, { useState } from 'react'
import './index.css'
import { TiPlus } from 'react-icons/ti'
import Tag from '../Tag'

function TagSelector(props) {
    const [inputValue, setInputValue] = useState('')
    const [suggestions, setSuggestions] = useState([])

    const handleInputChange = (e) => {
        const inputValue = e.target.value
        setInputValue(inputValue)
        const cleanInput = inputValue.trim()
        if (cleanInput !== '') {
            setSuggestions(props.searchTags(cleanInput).slice(0, 3))
        } else {
            setSuggestions([])
        }
    }

    const handleAddTag = (value) => {
        const trimmedValue = value.trim().toLowerCase()
        if (trimmedValue !== '') {
            props.addTag(trimmedValue)
            setInputValue('')
            setSuggestions([])
        }
    }

    const handleRemoveTag = (tag) => {
        const trimmedTag = tag.trim().toLowerCase()
        if (trimmedTag !== '') {
            props.removeTag(trimmedTag)
        }
    }

    return (
        <div className="tag-selector">
            <div className="tag-selector-drop-down">
                <div className="tag-selector-drop-down-search">
                    <input
                        type="text"
                        className="tag-selector-drop-down-search-input"
                        value={inputValue}
                        onChange={handleInputChange}
                        placeholder="Scrie aici"
                    />
                    <button
                        className="tag-selector-drop-down-search-button"
                        onClick={() => {
                            handleAddTag(inputValue)
                        }}
                    >
                        <TiPlus />
                    </button>
                </div>
                <div className="tag-selector-drop-down-suggestions">
                    {suggestions.map((suggestion) => (
                        <button
                            key={suggestion}
                            className="tag-selector-drop-down-suggestion-button"
                            onClick={() => {
                                handleAddTag(suggestion)
                            }}
                        >
                            {suggestion}
                        </button>
                    ))}
                </div>
            </div>
            <div className="tag-selector-tags">
                {props.tags.map((tag) => (
                    <Tag
                        key={tag}
                        text={tag}
                        onRemove={() => {
                            handleRemoveTag(tag)
                        }}
                    />
                ))}
            </div>
        </div>
    )
}

export default TagSelector
