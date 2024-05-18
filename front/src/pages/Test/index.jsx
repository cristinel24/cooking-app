import React, { useState } from 'react'

import {
    ActionButton,
    PageButton,
    PopUpChat,
    Recipe,
    Footer,
    UserProfile,
    Navbar,
    AdminBox,
    PreviewRecipe,
    Filters,
    ShowMenu,
    ReportBug,
    Report,
    Categories,
    Tag,
    TagSelector,
    RecipeCard,
    UserCard,
    RichTextEditor,
} from '../../components'

import { MdWavingHand } from 'react-icons/md'

import { uploadImage } from '../../services/image'

import { base64ToFile } from '../../utils/base64'
import { renderJSONtoHTML } from '../../utils/richTextEditor'

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
        obj.content.forEach((contentObj) =>
            replaceImageSrcs(contentObj, sourceMap)
        )
    }
}

function Test() {
    const [richTextData, setRichTextData] = useState({})
    const [finalData, setFinalData] = useState('')

    const handleSubmit = async (event) => {
        event.preventDefault()
        try {
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
            setRichTextData((data) => {
                replaceImageSrcs(data, imageLinkMap)
                return data
            })

            setFinalData(renderJSONtoHTML(richTextData))
        } catch (error) {
            console.error('Error submitting form:', error)
        }
    }

    return (
        <>
            <form onSubmit={handleSubmit}>
                <RichTextEditor
                    onChange={setRichTextData}
                    onRemove={() => {
                        console.log('clicked remove on first')
                    }}
                />
                <button type="submit">Submit</button>
            </form>

            <div className="preview" style={{ backgroundColor: 'white' }}>
                Preview:
                <div dangerouslySetInnerHTML={{ __html: finalData }} />
            </div>
        </>
    )
}

export default Test
