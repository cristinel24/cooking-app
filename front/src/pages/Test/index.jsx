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

//pagina noua
function Test() {
    const [richTextData, setRichTextData] = useState([null, null])

    return (
        <>
            <RichTextEditor
                setData={setRichTextData}
                onRemove={() => {
                    console.log('clicked remove on first')
                }}
            />
            <span style={{ backgroundColor: '#ffffff' }}>
                Preview: {richTextData}
            </span>
        </>
    )
}

export default Test
