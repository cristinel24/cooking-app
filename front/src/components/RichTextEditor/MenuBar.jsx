import React, { useEffect, useRef } from 'react'

import './index.css'
import { Button as RTEButton } from './Button'

import { useCurrentEditor } from '@tiptap/react'

import { FiBold } from 'react-icons/fi'
import { FiUnderline } from 'react-icons/fi'
import { FiItalic } from 'react-icons/fi'
import { FiImage } from 'react-icons/fi'
import { GrTextAlignLeft } from 'react-icons/gr'
import { GoListOrdered, GoStrikethrough } from 'react-icons/go'
import { GoListUnordered } from 'react-icons/go'
import { IoIosReturnLeft } from 'react-icons/io'
import { LuUndo } from 'react-icons/lu'
import { LuRedo } from 'react-icons/lu'
import { RxCross2 } from 'react-icons/rx'
import { MdFormatClear } from 'react-icons/md'

import { fileToBase64 } from '../../utils/base64'

export const MenuBar = ({ content, onChange, onRemove, allowImageUploads }) => {
    const { editor } = useCurrentEditor()
    const timeoutRef = useRef(null)

    useEffect(() => {
        if (!editor || editor.isDestroyed) {
            return
        }
        if (!editor.isFocused || !editor.isEditable) {
            if (timeoutRef.current != null) {
                // force onChange before proceeding
                clearTimeout(timeoutRef.current)
                onChange(editor.getJSON())
                timeoutRef.current = null
            }
        }
    }, [editor, editor?.isEditable, editor?.isFocused])

    useEffect(() => {
        // Use queueMicrotask per https://github.com/ueberdosis/tiptap/issues/3764#issuecomment-1546854730
        queueMicrotask(() => {
            const currentSelection = editor.state.selection
            editor.chain().setContent(content).setTextSelection(currentSelection).run()
        })
    }, [content])

    const handleContentChange = (editor) => {
        clearTimeout(timeoutRef.current)
        timeoutRef.current = setTimeout(() => {
            if (onChange) {
                onChange(editor.getJSON())
                timeoutRef.current = null
            }
        }, 300)
    }

    editor.on('update', ({ editor }) => {
        handleContentChange(editor)
    })
    const fileInputRef = useRef(null)

    if (!editor) {
        return null
    }

    const handleImageUpload = async (event) => {
        const file = event.target.files[0]
        if (!file) return

        const base64Buffer = await fileToBase64(file)
        editor.chain().focus().setImage({ src: base64Buffer }).run()
    }

    return (
        <div className="rich-text-editor-menu-bar">
            <div className="rich-text-editor-menu-bar-buttons">
                <RTEButton
                    title="Bold"
                    onClick={() => editor.chain().focus().toggleBold().run()}
                    disabled={!editor.can().chain().focus().toggleBold().run()}
                    active={editor.isActive('bold')}
                    Icon={FiBold}
                />
                <RTEButton
                    title="Italic"
                    onClick={() => editor.chain().focus().toggleItalic().run()}
                    disabled={!editor.can().chain().focus().toggleItalic().run()}
                    active={editor.isActive('italic')}
                    Icon={FiItalic}
                />
                <RTEButton
                    title="Subliniat"
                    onClick={() => editor.chain().focus().toggleUnderline().run()}
                    disabled={!editor.can().chain().focus().toggleUnderline().run()}
                    active={editor.isActive('underline')}
                    Icon={FiUnderline}
                />
                <RTEButton
                    title="Tăiat"
                    onClick={() => editor.chain().focus().toggleStrike().run()}
                    disabled={!editor.can().chain().focus().toggleStrike().run()}
                    active={editor.isActive('strike')}
                    Icon={GoStrikethrough}
                />
                <RTEButton
                    title="Ștergere formatare"
                    onClick={() => editor.chain().focus().unsetAllMarks().run()}
                    Icon={MdFormatClear}
                />

                <hr className="rich-text-editor-menu-bar-divider" />

                <RTEButton
                    title="Paragraf"
                    onClick={() => editor.chain().focus().setParagraph().run()}
                    Icon={GrTextAlignLeft}
                />
                <RTEButton
                    title="Puncte de paragraf"
                    onClick={() => editor.chain().focus().toggleBulletList().run()}
                    active={editor.isActive('bulletList')}
                    Icon={GoListUnordered}
                />
                <RTEButton
                    title="Listă ordonată"
                    onClick={() => editor.chain().focus().toggleOrderedList().run()}
                    active={editor.isActive('orderedList')}
                    Icon={GoListOrdered}
                />
                <RTEButton
                    title="Rând nou"
                    onClick={() => editor.chain().focus().setHardBreak().run()}
                    Icon={IoIosReturnLeft}
                />

                <hr className="rich-text-editor-menu-bar-divider" />

                {allowImageUploads && (
                    <>
                        <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            style={{ display: 'none' }}
                            ref={fileInputRef}
                        />
                        <RTEButton
                            title="Adaugă o imagine"
                            onClick={() => {
                                fileInputRef.current.click()
                            }}
                            Icon={FiImage}
                        />
                    </>
                )}

                <RTEButton
                    title="Înapoi"
                    onClick={() => editor.chain().focus().undo().run()}
                    disabled={!editor.can().chain().focus().undo().run()}
                    Icon={LuUndo}
                />

                <RTEButton
                    title="Înainte"
                    onClick={() => editor.chain().focus().redo().run()}
                    disabled={!editor.can().chain().focus().redo().run()}
                    Icon={LuRedo}
                />
            </div>
            {onRemove && <RTEButton title="Șterge" onClick={onRemove} Icon={RxCross2} />}
        </div>
    )
}
