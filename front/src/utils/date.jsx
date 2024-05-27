export const dateToRomanian = (dateString) => {
    const date = new Date(dateString)

    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
    }
    const formattedDate = date.toLocaleDateString('ro-RO', options)

    return formattedDate
}
