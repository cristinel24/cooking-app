import { Editor } from '@tiptap/core'
import ListItem from '@tiptap/extension-list-item'
import TextStyle from '@tiptap/extension-text-style'
import StarterKit from '@tiptap/starter-kit'
import Image from '@tiptap/extension-image'

export const extensions = [
    TextStyle.configure({ types: [ListItem.name] }),
    StarterKit.configure({
        bulletList: {
            keepMarks: true,
            keepAttributes: false,
        },
        orderedList: {
            keepMarks: true,
            keepAttributes: false,
        },
    }),
    Image.configure({
        allowBase64: true,
    }),
]

export const renderJSONtoHTML = (json) => {
    let editor = new Editor({
        extensions: extensions,
        content: json,
    })
    return editor.getHTML()
}
