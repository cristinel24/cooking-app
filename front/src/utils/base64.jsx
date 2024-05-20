// Function to encode the object to a base64 string
export function encodeObjectToBase64(obj) {
    // Convert the object to a JSON string
    const jsonString = JSON.stringify(obj);
    console.log(jsonString)

    // Encode the JSON string to a base64 string
    const base64String = btoa(encodeURIComponent(jsonString));

    return base64String;
}

// Function to decode the base64 string back to an object
export function decodeBase64ToObject(base64String) {
    // Decode the base64 string to a JSON string
    const jsonString = decodeURIComponent(atob(base64String));

    // Parse the JSON string to get the original object
    const obj = JSON.parse(jsonString);

    return obj;
}
