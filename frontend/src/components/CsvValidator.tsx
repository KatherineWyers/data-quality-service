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
                <div className="header">
                    <div>
                        <h1 className="title">Data Quality Service</h1>
                        <p className="subtitle">Inspect and validate your data pipeline</p>
                    </div>
                </div>

                <div className="divider" />

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
                            Run Validation
                        </>
                    )}
                </button>

                {/* Result area */}
                {status !== "idle" && (
                    <div className="result-wrap">
                        <div className={"divider"}></div>
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