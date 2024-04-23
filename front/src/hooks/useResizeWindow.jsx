import { useEffect, useState } from 'react'

const useResizeWindow = () => {
    const [width, setWidth] = useState(window.innerWidth)

    useEffect(() => {
        window.addEventListener('resize', () => {
            setWidth(window.innerWidth)
        })
    }, [])

    return width
}

export default useResizeWindow
