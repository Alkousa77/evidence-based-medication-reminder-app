import axios from "axios";

const api = axios.create({
    baseURL: process.env.EXPO_PUBLIC_API_URL, //backend server address (through ngrok URL)
    withCredentials: true, // attach cookies with requests (used to ensure FLask can read session["user_id"]from client)
    headers: {
        "ngrok-skip-browser-warning": "true"
    }
});

export default api;
