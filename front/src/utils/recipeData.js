export const prepTimeDisplayText = (prepTime) => {
    const prepTimeHours = Math.floor(prepTime / 60)
    const prepTimeMinutes = prepTime % 60
    switch (true) {
        case prepTimeHours > 0 && prepTimeMinutes > 0:
            return `${prepTimeHours} ${
                prepTimeHours === 1 ? 'oră' : 'ore'
            } ${prepTimeMinutes} ${prepTimeMinutes === 1 ? 'minut' : 'minute'}`
        case prepTimeHours > 0:
            return `${prepTimeHours} ${prepTimeHours === 1 ? 'oră' : 'ore'}`
        default:
            return `${prepTimeMinutes} ${
                prepTimeMinutes === 1 ? 'minut' : 'minute'
            }`
    }
}

export const ratingToNumber = (ratingSum, ratingCount) => {
    if (ratingCount == 0) {
        return 0
    }
    return ratingSum / ratingCount
}
