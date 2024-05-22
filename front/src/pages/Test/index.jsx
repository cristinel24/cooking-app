import React, { useState } from 'react'

import { RichTextEditor } from '../../components'

import { uploadImage } from '../../services/image'

import { base64ToFile } from '../../utils/base64'
import { renderJSONtoHTML, collectImageSrcs, replaceImageSrcs } from '../../utils/richTextEditor'

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
            const data = renderJSONtoHTML(richTextData)
            setFinalData(data)
            console.log(data)
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

            <div>
                Preview:
                <div dangerouslySetInnerHTML={{ __html: finalData }} />
            </div>
        </>
    )
}

export default Test
