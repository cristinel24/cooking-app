import React, { useState, useEffect, useRef } from 'react'
import './index.css'

import ListItem from '@tiptap/extension-list-item'
import TextStyle from '@tiptap/extension-text-style'
import { EditorProvider, useCurrentEditor } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { FiBold } from 'react-icons/fi'
import { FiUnderline } from 'react-icons/fi'
import { FiItalic } from 'react-icons/fi'
import { FiImage } from 'react-icons/fi'
import { GrTextAlignLeft } from 'react-icons/gr'
import { GoListOrdered } from 'react-icons/go'
import { GoListUnordered } from 'react-icons/go'
import { IoIosReturnLeft } from 'react-icons/io'
import { LuUndo } from 'react-icons/lu'
import { LuRedo } from 'react-icons/lu'
import { RxCross2 } from 'react-icons/rx'
import { MdFormatClear } from 'react-icons/md'

const MenuBar = ({ onRemove }) => {
    const { editor } = useCurrentEditor()

    if (!editor) {
        return null
    }

    return (
        <div className="rich-text-editor-menu-bar">
            <div className="rich-text-editor-menu-bar-buttons">
                <button
                    title="Bold"
                    onClick={() => editor.chain().focus().toggleBold().run()}
                    disabled={!editor.can().chain().focus().toggleBold().run()}
                    className={
                        editor.isActive('bold')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <FiBold />
                </button>
                <button
                    title="Italic"
                    onClick={() => editor.chain().focus().toggleItalic().run()}
                    disabled={
                        !editor.can().chain().focus().toggleItalic().run()
                    }
                    className={
                        '' +
                        ' ' +
                        (editor.isActive('italic')
                            ? 'rich-text-editor-button-active'
                            : '')
                    }
                >
                    <FiItalic />
                </button>
                <button
                    title="Ștergere formatare"
                    onClick={() => editor.chain().focus().unsetAllMarks().run()}
                >
                    <MdFormatClear />
                </button>
                <button
                    title="Paragraf"
                    onClick={() => editor.chain().focus().setParagraph().run()}
                    className={
                        '' + ' ' + editor.isActive('paragraph')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <GrTextAlignLeft />
                </button>
                <button
                    title="Puncte de paragraf"
                    onClick={() =>
                        editor.chain().focus().toggleBulletList().run()
                    }
                    className={
                        '' + ' ' + editor.isActive('bulletList')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <GoListUnordered />
                </button>
                <button
                    title="Listă ordonată"
                    onClick={() =>
                        editor.chain().focus().toggleOrderedList().run()
                    }
                    className={
                        '' + ' ' + editor.isActive('orderedList')
                            ? 'rich-text-editor-button-active'
                            : ''
                    }
                >
                    <GoListOrdered />
                </button>
                <button
                    title="Rând nou"
                    onClick={() => editor.chain().focus().setHardBreak().run()}
                >
                    <IoIosReturnLeft />
                </button>
                <button
                    title="Înapoi"
                    onClick={() => editor.chain().focus().undo().run()}
                    disabled={!editor.can().chain().focus().undo().run()}
                >
                    <LuUndo />
                </button>
                <button
                    title="Înainte"
                    onClick={() => editor.chain().focus().redo().run()}
                    disabled={!editor.can().chain().focus().redo().run()}
                >
                    <LuRedo />
                </button>
            </div>
            <button onClick={onRemove}>
                <RxCross2 />
            </button>
        </div>
    )
}

const extensions = [
    TextStyle.configure({ types: [ListItem.name] }),
    StarterKit.configure({
        bulletList: {
            keepMarks: true,
            keepAttributes: false, // TODO : Making this as `false` becase marks are not preserved when I try to preserve attrs, awaiting a bit of help
        },
        orderedList: {
            keepMarks: true,
            keepAttributes: false, // TODO : Making this as `false` becase marks are not preserved when I try to preserve attrs, awaiting a bit of help
        },
    }),
    Image.configure({
        allowBase64: true,
    }),
]

const content = `
<p>
  this is a <em>basic</em> example of <strong>tiptap</strong>. Sure, there are all kind of basic text styles you’d probably expect from a text editor. But wait until you see the images :D
</p>

`

function RichTextEditor({ onRemove }) {
    return (
        <div className="rich-text-editor">
            <EditorProvider
                slotBefore={<MenuBar onRemove={onRemove} />}
                extensions={extensions}
                content={content}
            ></EditorProvider>
        </div>
    )
}

export default RichTextEditor
