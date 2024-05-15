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
    return (
        <>
            <Navbar />
            <RichTextEditor
                onRemove={() => {
                    console.log('clicked remove on first')
                }}
            />
            <RichTextEditor
                onRemove={() => {
                    console.log('clicked remove on second')
                }}
            />
        </>
    )
}

export default Test
