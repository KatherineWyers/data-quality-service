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
                        <p className="subtitle">Inspect and validate your data pipeline. Test the system below</p>
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
                            {status === "success" && result && (
                                <>
                                    <p>Result: {result.success ? "Success" : "Failed"}</p>
                                    <p>Message: {result.message}</p>
                                </>
                            )}

                            {status === "success" && result && (
                                <table className="issues-table" style={{ borderCollapse: "collapse", width: "100%" }}>
                                    <thead>
                                    <tr>
                                        {Object.keys(result.issues[0] || {}).map((key) => (
                                            <th key={key} style={{ border: "1px solid #ccc", padding: "8px", textAlign: "left" }}>
                                                {key}
                                            </th>
                                        ))}
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {result.issues.map((issue, i) => (
                                        <tr key={i}>
                                            {Object.values(issue).map((val, j) => (
                                                <td key={j} style={{ border: "1px solid #ccc", padding: "8px" }}>
                                                    {typeof val === "object" ? JSON.stringify(val) : String(val)}
                                                </td>
                                            ))}
                                        </tr>
                                    ))}
                                    </tbody>
                                </table>
                            )}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
}