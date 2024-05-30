export const sendReport = async (reportData) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (Math.random() < 0.5) {
                resolve({ status: 'ok' })
            } else {
                reject({ errorCode: 12345 })
            }
        }, 1000)
    })
}
