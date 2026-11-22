import { Bot, CircleUserRound, FileText, Image } from "lucide-react";
import { getArtifactUrl } from "../../api/ask";

interface Props {
    role: "user" | "assistant";
    text: string;
    attachments?: string[];
    artifacts?: string[];
}

const isImage = (filename: string) => /\.(png|jpe?g|gif|webp|svg)$/i.test(filename);

export default function ChatMessage({ role, text, attachments = [], artifacts = [] }: Props) {
    const isUser = role === "user";

    return (
        <article className={`flex items-end gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
            {!isUser && (
                <div className="mb-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white shadow-lg shadow-indigo-950/30">
                    <Bot size={21} />
                </div>
            )}
            <div className={`max-w-[78%] rounded-3xl px-5 py-4 text-sm leading-6 shadow-sm whitespace-pre-wrap sm:max-w-[70%] ${isUser ? "rounded-br-md bg-indigo-600 text-white" : "rounded-bl-md border border-white/8 bg-white/6 text-slate-100"}`}>
                {attachments.length > 0 && (
                    <div className="mb-3 space-y-2">
                        {attachments.map((name) => (
                            <div key={name} className={`flex items-center gap-2 rounded-xl px-3 py-2 text-xs ${isUser ? "bg-white/15" : "bg-black/15"}`}>
                                <FileText size={15} aria-hidden="true" />
                                <span className="truncate">{name}</span>
                            </div>
                        ))}
                    </div>
                )}
                {text && <p>{text}</p>}
                {artifacts.length > 0 && (
                    <div className="mt-3 space-y-3">
                        {artifacts.map((artifact) => isImage(artifact) ? (
                            <a key={artifact} href={getArtifactUrl(artifact)} target="_blank" rel="noreferrer" className="block overflow-hidden rounded-2xl border border-white/10 bg-black/20">
                                <img src={getArtifactUrl(artifact)} alt="Generated analysis chart" className="max-h-96 w-full object-contain" />
                            </a>
                        ) : (
                            <a key={artifact} href={getArtifactUrl(artifact)} target="_blank" rel="noreferrer" className="flex items-center gap-2 rounded-xl bg-black/15 px-3 py-2 text-xs text-indigo-200 hover:bg-black/25">
                                <Image size={15} aria-hidden="true" />
                                <span className="truncate">View generated file: {artifact}</span>
                            </a>
                        ))}
                    </div>
                )}
            </div>
            {isUser && (
                <div className="mb-1 flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-emerald-500 text-white shadow-lg shadow-emerald-950/20">
                    <CircleUserRound size={22} />
                </div>
            )}
        </article>
    );
}
