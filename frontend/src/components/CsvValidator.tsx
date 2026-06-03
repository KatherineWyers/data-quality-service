import { useState } from "react";

type ValidationResult = Record<string, unknown> | unknown[] | null;

export default function CsvValidator() {
    const [result, setResult] = useState<ValidationResult>(null);
    const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
    const [errorMsg, setErrorMsg] = useState<string>("");

    const runValidation = async () => {
        setStatus("loading");
        setResult(null);
        setErrorMsg("");
        try {
            const res = await fetch("/validate");
            if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
            const data = await res.json();
            setResult(data);
            setStatus("success");
        } catch (err) {
            setErrorMsg(err instanceof Error ? err.message : "Unknown error");
            setStatus("error");
        }
    };

    return (
        <div className="page">
            <div className="card">
                {/* Header */}
                <div className="header">
                    <div className="icon-wrap">
                        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                            <line x1="16" y1="13" x2="8" y2="13"/>
                            <line x1="16" y1="17" x2="8" y2="17"/>
                            <polyline points="10 9 9 9 8 9"/>
                        </svg>
                    </div>
                    <div>
                        <h1 className="title">CSV Validator</h1>
                        <p className="subtitle">Inspect and validate your data pipeline</p>
                    </div>
                </div>

                {/* Divider */}
                <div className="divider" />

                {/* Button */}
                <button
                    className="btn"
                    onClick={runValidation}
                    disabled={status === "loading"}
                >
                    {status === "loading" ? (
                        <>
                            <span className="spinner" />
                            Running…
                        </>
                    ) : (
                        <>
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: 8 }}>
                                <polygon points="5 3 19 12 5 21 5 3"/>
                            </svg>
                            Run Validation
                        </>
                    )}
                </button>

                {/* Result area */}
                {status !== "idle" && (
                    <div className="result-wrap">
                        <pre className={`pre${status === "error" ? " pre-error" : ""}`}>
                    {status === "loading" && "Running…"}
                            {status === "error" && errorMsg}
                            {status === "success" && JSON.stringify(result, null, 2)}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
}