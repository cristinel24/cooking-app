export const base64ToFile = (base64Image) => {
    const buffer = base64Image.split(',')[1].trim()
    const byteCharacters = atob(buffer)
    const byteArrays = []
    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
        const slice = byteCharacters.slice(offset, offset + 512)
        const byteNumbers = new Array(slice.length)
        for (let i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i)
        }
        const byteArray = new Uint8Array(byteNumbers)
        byteArrays.push(byteArray)
    }
    const blob = new Blob(byteArrays, {
        type: base64Image.split(',')[0].trim(),
    })
    return new File([blob], '', { type: base64Image.split(',')[0].trim() })
}

// must be awaited; returns a promise
export const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.onload = () => {
            console.log(reader.result.slice(0, 100))
            resolve(reader.result)
        }
        reader.onerror = () => {
            reject(reader.error)
        }
        reader.readAsDataURL(file)
    })
}

export function encodeObjectToBase64(obj) {
    const jsonString = JSON.stringify(obj)
    const base64String = btoa(encodeURIComponent(jsonString))
    return base64String
}

export function decodeBase64ToObject(base64String) {
    const jsonString = decodeURIComponent(atob(base64String))
    const obj = JSON.parse(jsonString)
    return obj
}
