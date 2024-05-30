import React from 'react'

import './index.css'

import { EditorProvider } from '@tiptap/react'
import { extensions } from '../../utils/richTextEditor'

import { MenuBar as RTEMenuBar } from './MenuBar'

function RichTextEditor({
    onChange,
    onRemove,
    allowImageUploads = true,
    defaultValue,
    className,
    id,
    errorCheck,
}) {
    const content = defaultValue ? defaultValue : ''

    return (
        <div className={`form-item ${className ? className : ''}`}>
            <div className="rich-text-editor" id={id}>
                <EditorProvider
                    slotBefore={
                        <RTEMenuBar
                            onRemove={onRemove}
                            onChange={onChange}
                            allowImageUploads={allowImageUploads}
                        />
                    }
                    extensions={extensions}
                    content={content}
                    editorProps={{
                        attributes: {
                            class: 'rich-text-editor-content',
                        },
                    }}
                ></EditorProvider>
            </div>
            {errorCheck && errorCheck(id)}
        </div>
    )
}

export default RichTextEditor
