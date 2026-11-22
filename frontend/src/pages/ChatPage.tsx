import { useState } from "react";
import { MessageSquarePlus, Sparkles } from "lucide-react";
import { askQuestion, resetConversation } from "../api/ask";
import ChatWindow from "../components/chat/ChatWindow";
import type { ChatMessageData } from "../components/chat/ChatWindow";
import ChatInput from "../input/Input";

export default function ChatPage() {
    const [messages, setMessages] = useState<ChatMessageData[]>([]);
    const [isThinking, setIsThinking] = useState(false);
    const [isResetting, setIsResetting] = useState(false);

    const startNewChat = async () => {
        if (isResetting || isThinking) return;

        setIsResetting(true);

        try {
            await resetConversation();
            setMessages([]);
        } finally {
            setIsResetting(false);
        }
    };

    const sendMessage = async (text: string, files: File[]) => {
        setMessages((current) => [...current, { id: crypto.randomUUID(), role: "user", text, attachments: files.map((file) => file.name) }]);
        setIsThinking(true);
        try {
            const response = await askQuestion(text || "Please analyse the attached PDF.", files);
            setMessages((current) => [...current, { id: crypto.randomUUID(), role: "assistant", text: response.answer, artifacts: response.artifacts }]);
        } catch {
            setMessages((current) => [...current, { id: crypto.randomUUID(), role: "assistant", text: "I couldn’t reach the server. Please make sure the backend is running, then try again." }]);
        } finally {
            setIsThinking(false);
        }
    };

    return (
        <div className="flex h-screen flex-col overflow-hidden bg-[radial-gradient(circle_at_top,_#1e2f5c_0,_#0c1222_42%,_#070b14_100%)] text-white">
            <header className="border-b border-white/8 bg-slate-950/45 px-5 py-4 backdrop-blur sm:px-8">
                <div className="mx-auto flex max-w-6xl items-center justify-between">
                    <div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-indigo-500 shadow-lg shadow-indigo-950/30"><Sparkles size={20} /></div><div><h1 className="font-semibold tracking-tight">Adaptive RAG</h1><p className="text-xs text-slate-400">JEE preparation assistant</p></div></div>
                    <button onClick={startNewChat} disabled={isResetting || isThinking} className="flex items-center gap-2 rounded-xl px-3 py-2 text-sm text-slate-300 transition hover:bg-white/8 hover:text-white disabled:cursor-not-allowed disabled:opacity-50" title="Start a new chat"><MessageSquarePlus size={18} /> <span className="hidden sm:inline">{isResetting ? "Resetting…" : "New chat"}</span></button>
                </div>
            </header>
            <div className="flex-1 overflow-hidden"><ChatWindow messages={messages} isThinking={isThinking} /></div>
            <ChatInput onSend={sendMessage} disabled={isThinking} />
        </div>
    );
}
