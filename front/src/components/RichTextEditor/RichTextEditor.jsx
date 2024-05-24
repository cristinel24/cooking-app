import React from 'react'

import './index.css'

import { EditorProvider } from '@tiptap/react'
import { extensions } from '../../utils/richTextEditor'

import { MenuBar as RTEMenuBar } from './MenuBar'

const content = ``

function RichTextEditor({ onChange, onRemove, allowImageUploads = true }) {
    return (
        <div className="rich-text-editor">
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
    )
}

export default RichTextEditor
