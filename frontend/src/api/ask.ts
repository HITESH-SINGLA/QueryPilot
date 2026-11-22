import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
});

const apiBaseUrl = "http://127.0.0.1:8000";

interface AskResponse {
    answer: string;
    artifacts: string[];
}

export async function askQuestion(question: string, files: File[] = []): Promise<AskResponse> {
    const formData = new FormData();
    formData.append("question", question);
    files.forEach((file) => formData.append("files", file));

    const response = await api.post<AskResponse>("/ask", formData);
    return response.data;
}

export async function resetConversation(): Promise<void> {
    await api.post("/reset");
}

export function getArtifactUrl(filename: string) {
    return `${apiBaseUrl}/artifacts/${encodeURIComponent(filename)}`;
}
