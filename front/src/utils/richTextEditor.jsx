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

import { uploadImage } from '../services/image'
import { base64ToFile } from './base64'

// such that both the RTEs created in the frontend and the headless renderer have the same specs
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

// takes JSON object from RTE, returns HTML string ready to be sent to backend
export const renderJSONtoHTML = (json) => {
    let editor = new Editor({
        extensions: extensions,
        content: json,
    })
    return editor.getHTML()
}

// takes raw RTE JSON, returns RTE JSON with base64 images uploaded to the server
export async function uploadImagesInJSON(richTextData) {
    let images = new Set()
    collectImageSrcs(richTextData, images)
    let imageArray = Array.from(images)
    let imageLinkMap = new Map()
    await Promise.all(
        imageArray.map(async (base64Image) => {
            let formData = new FormData()
            formData.append('file', base64ToFile(base64Image))

            const response = await uploadImage(formData)
            imageLinkMap.set(base64Image, response)
        })
    )
    replaceImageSrcs(richTextData, imageLinkMap)
    return richTextData
}

// -- utils --

function collectImageSrcs(obj, srcs) {
    if (obj.type === 'image' && obj.attrs.src) {
        // testing if src is of type base64
        if (!/^(data:image\/\w+;base64,)/.test(obj.attrs.src)) {
            return
        }
        srcs.add(obj.attrs.src)
    } else if (obj.content) {
        obj.content.forEach((contentObj) => collectImageSrcs(contentObj, srcs))
    }
}

function replaceImageSrcs(obj, sourceMap) {
    if (obj.type === 'image') {
        if (sourceMap.has(obj.attrs.src)) {
            obj.attrs.src = sourceMap.get(obj.attrs.src)
        }
    } else if (obj.content) {
        obj.content.forEach((contentObj) => replaceImageSrcs(contentObj, sourceMap))
    }
}
