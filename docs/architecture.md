# Architecture

## High-Level Runtime

```mermaid
flowchart LR
    User["User"] --> GUI["PySide6 Launcher"]
    GUI --> Discovery["App Discovery"]
    GUI --> Env["Environment Manager"]
    GUI --> PM["Process Manager"]
    Discovery --> Cache["Local App Cache"]
    Env --> Cache["Local Cache"]
    PM --> Streamlit["Streamlit on 127.0.0.1"]
    Streamlit --> Browser["Default Browser"]
```

## Network Drive, Many Users

```mermaid
flowchart LR
    Share["Network Share<br/>Unified-Streamlit-Launcher<br/>launcher.exe, apps, config, runtime"]
    U1["User 1 PC"]
    U2["User 2 PC"]
    U15["User 15 PC"]
    C1["User 1 Local Cache<br/>runtime, apps, venvs, logs"]
    C2["User 2 Local Cache<br/>runtime, apps, venvs, logs"]
    C15["User 15 Local Cache<br/>runtime, apps, venvs, logs"]
    B1["Browser localhost"]
    B2["Browser localhost"]
    B15["Browser localhost"]

    Share --> U1 --> C1 --> B1
    Share --> U2 --> C2 --> B2
    Share --> U15 --> C15 --> B15
```

The network share is the read-only distribution source. Each user machine receives its own local copy of the portable runtime, app source folders, virtual environments, logs, and state under `%LOCALAPPDATA%`.

## Launch Sequence

```mermaid
sequenceDiagram
    actor User
    participant GUI as Launcher GUI
    participant Cache as Local Cache
    participant EM as Environment Manager
    participant PM as Process Manager
    participant ST as Streamlit
    participant Browser
    User->>GUI: Double-click launcher.exe on network share
    GUI->>Cache: Sync runtime and app folders locally
    User->>GUI: Click Open
    GUI->>EM: Ensure app environment
    EM-->>GUI: Environment ready
    GUI->>PM: Start app
    PM->>ST: python -m streamlit run
    PM->>ST: Poll /_stcore/health
    ST-->>PM: Healthy
    PM-->>GUI: Running URL
    GUI->>Browser: Open localhost URL
```

```mermaid
flowchart TD
    A["Read local version"] --> B["Read published current.json"]
    B --> C["Stage release"]
    C --> D["Verify checksums"]
    D --> E["Validate manifests"]
    E --> F["Activate versioned local copy"]
    D --> G["Fail closed on checksum error"]
```

```mermaid
flowchart TD
    A["Check marker"] -->|Valid| B["Reuse environment"]
    A -->|Missing or stale| C["Create venv"]
    C --> D["Install requirements"]
    D --> E["Validate streamlit import"]
    E --> F["Write ready marker"]
```

```mermaid
stateDiagram-v2
    [*] --> Stopped
    Stopped --> Starting
    Starting --> Running
    Starting --> Failed
    Running --> Stopping
    Stopping --> Stopped
    Running --> Failed
```
