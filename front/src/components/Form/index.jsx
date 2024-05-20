import './index.css'

export { default as FormCheckbox } from './FormCheckbox'
export { default as FormInput } from './FormInput'
export { default as FormPassword } from './FormPassword'

export const length = (min, value) => {
    return {
        value,
        message: `Acest câmp trebuie să aibă ${min} ${value} caractere`,
    }
}
