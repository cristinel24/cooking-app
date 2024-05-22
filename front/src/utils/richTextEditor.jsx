import { Editor } from '@tiptap/core'

import Document from '@tiptap/extension-document'
import History from '@tiptap/extension-history'
import Paragraph from '@tiptap/extension-paragraph'
import Text from '@tiptap/extension-text'
import Bold from '@tiptap/extension-bold'
import Italic from '@tiptap/extension-italic'
import Underline from '@tiptap/extension-underline'
import Strike from '@tiptap/extension-strike'
import ListItem from '@tiptap/extension-list-item'
import BulletList from '@tiptap/extension-bullet-list'
import OrderedList from '@tiptap/extension-ordered-list'
import HardBreak from '@tiptap/extension-hard-break'
import Image from '@tiptap/extension-image'

export const extensions = [
    Document,
    History,
    Paragraph,
    Text,
    Bold,
    Italic,
    Underline,
    Strike,
    ListItem,
    BulletList.configure({
        keepMarks: true,
        keepAttributes: false,
    }),
    OrderedList.configure({
        keepMarks: true,
        keepAttributes: false,
    }),
    HardBreak,
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
