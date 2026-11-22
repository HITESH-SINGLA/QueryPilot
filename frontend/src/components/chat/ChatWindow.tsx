import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";

export interface ChatMessageData {
    id: string;
    role: "user" | "assistant";
    text: string;
    attachments?: string[];
    artifacts?: string[];
}

interface Props {
    messages: ChatMessageData[];
    isThinking: boolean;
}

export default function ChatWindow({ messages, isThinking }: Props) {
    const chatEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isThinking]);

    return (
        <div className="h-full overflow-y-auto">
            {messages.length === 0 && !isThinking ? (
                <div className="mx-auto flex h-full max-w-4xl flex-col items-center justify-center px-6 pb-24 text-center">
                    <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-400 to-violet-600 text-2xl shadow-xl shadow-indigo-950/40">✦</div>
                    <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">What can I help you understand?</h2>
                    <p className="mt-3 max-w-md text-sm leading-6 text-slate-400">Attach a PDF and ask anything about it, or start with a question from your study material.</p>
                    <div className="mt-8 flex flex-wrap justify-center gap-2 text-sm text-slate-300">
                        <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2">Summarise a PDF</span>
                        <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2">Explain a concept</span>
                        <span className="rounded-full border border-white/10 bg-white/5 px-4 py-2">Create practice questions</span>
                    </div>
                </div>
            ) : (
            <div className="mx-auto flex min-h-full max-w-4xl flex-col justify-end px-4 py-8 sm:px-8">
                <div className="space-y-6">
                    {messages.map((message) => <ChatMessage key={message.id} {...message} />)}
                    {isThinking && (
                        <div className="flex items-end gap-3">
                            <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white"><span className="animate-pulse">•••</span></div>
                            <div className="rounded-3xl rounded-bl-md border border-white/8 bg-white/6 px-5 py-3 text-sm text-slate-300">Thinking…</div>
                        </div>
                    )}
                    <div ref={chatEndRef} />
                </div>
            </div>
            )}
        </div>
    );
}
