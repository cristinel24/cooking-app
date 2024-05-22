export const length = (min, value) => {
    return {
        value,
        message: `Acest câmp trebuie să aibă ${min} ${value} caractere`,
    }
}
