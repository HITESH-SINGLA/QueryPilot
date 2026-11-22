import { useRef, useState } from "react";
import type { ChangeEvent, FormEvent, KeyboardEvent } from "react";
import { Paperclip, Send, X } from "lucide-react";

interface Props {
    disabled?: boolean;
    onSend: (text: string, files: File[]) => void;
}

export default function ChatInput({ disabled = false, onSend }: Props) {
    const [text, setText] = useState("");
    const [files, setFiles] = useState<File[]>([]);
    const [fileError, setFileError] = useState("");
    const fileInputRef = useRef<HTMLInputElement>(null);

    const submit = (event: FormEvent) => {
        event.preventDefault();
        const message = text.trim();
        if ((!message && files.length === 0) || disabled) return;
        onSend(message, files);
        setText("");
        setFiles([]);
    };

    const attachFiles = (event: ChangeEvent<HTMLInputElement>) => {
        const selected = Array.from(event.target.files ?? []);
        const pdfs = selected.filter((file) => file.type === "application/pdf" || file.name.toLowerCase().endsWith(".pdf"));
        setFileError(pdfs.length === selected.length ? "" : "Only PDF files can be attached.");
        setFiles((current) => [...current, ...pdfs]);
        event.target.value = "";
    };

    const handleKeyDown = (event: KeyboardEvent<HTMLTextAreaElement>) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            submit(event);
        }
    };

    return (
        <div className="border-t border-white/8 bg-slate-950/75 p-4 backdrop-blur sm:p-6">
            <form className="mx-auto max-w-4xl" onSubmit={submit}>
                <div className="rounded-3xl border border-white/10 bg-white/7 p-2 shadow-2xl shadow-black/20 transition focus-within:border-indigo-400/60 focus-within:ring-4 focus-within:ring-indigo-500/10">
                    {files.length > 0 && <div className="flex flex-wrap gap-2 px-2 pt-2">
                        {files.map((file, index) => <span key={`${file.name}-${index}`} className="flex max-w-full items-center gap-2 rounded-xl bg-indigo-500/15 px-3 py-1.5 text-xs text-indigo-100">
                            <span className="truncate">{file.name}</span>
                            <button type="button" onClick={() => setFiles((current) => current.filter((_, fileIndex) => fileIndex !== index))} aria-label={`Remove ${file.name}`}><X size={14} /></button>
                        </span>)}
                    </div>}
                    <div className="flex items-end gap-2">
                        <input ref={fileInputRef} type="file" accept="application/pdf,.pdf" multiple className="sr-only" onChange={attachFiles} />
                        <button type="button" onClick={() => fileInputRef.current?.click()} disabled={disabled} aria-label="Attach PDF" title="Attach PDF" className="mb-0.5 rounded-2xl p-3 text-slate-300 transition hover:bg-white/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-50"><Paperclip size={20} /></button>
                        <textarea value={text} onChange={(event) => setText(event.target.value)} onKeyDown={handleKeyDown} disabled={disabled} className="max-h-32 min-h-12 flex-1 resize-none bg-transparent px-2 py-3 text-sm text-white outline-none placeholder:text-slate-500 disabled:cursor-not-allowed" rows={1} placeholder="Ask anything about your PDF…" />
                        <button type="submit" disabled={disabled || (!text.trim() && files.length === 0)} aria-label="Send message" className="mb-0.5 rounded-2xl bg-indigo-500 p-3 text-white transition hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-40"><Send size={19} /></button>
                    </div>
                </div>
                <p className={`px-3 pt-2 text-center text-xs ${fileError ? "text-rose-400" : "text-slate-500"}`}>{fileError || (files.length > 0 ? "PDF attached. Send your message to analyse it." : "Attach a PDF, then send your question. Press Enter to send.")}</p>
            </form>
        </div>
    );
}
