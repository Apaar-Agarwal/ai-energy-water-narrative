# Run the integrated team story

This ZIP is a portable local snapshot of the Part 2 integration. It contains the active app, original source data, processed data, documentation and preserved member contributions. No Git history, passwords, virtual environments or logs are included. Nothing has been pushed to GitHub by making this ZIP.

## Before starting

1. Install Python 3.11 or newer (64-bit). On Windows, enable **Add Python to PATH** during installation.
2. Extract the entire ZIP into a normal folder. Do not run the app from inside the ZIP viewer.
3. Keep the folder structure intact. The app reads its packaged data locally.

Internet is needed for the first dependency installation. Data browsing afterward does not require a live data API. Each person runs their own local server; a localhost link on one person's computer is not a shared public URL.

## Windows — double-click method

1. Double-click **Setup Windows.cmd** once. Wait until installation completes successfully.
2. Double-click **Launch integrated story.cmd**.
3. Open **http://localhost:8511** if a browser does not open automatically.
4. Keep the terminal open. Press **Ctrl+C** there to stop the app.

The setup creates a project-local `.venv` so the team's dependencies do not interfere with other projects. The launcher uses it if present.

## Windows — manual PowerShell method

Open a terminal in the extracted project folder, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.port 8511
```

If `python` is not found but the Windows launcher is installed, use `py -3 -m venv .venv` for the first command. Activation of the environment is not required.

## macOS / Linux

Open a terminal in the extracted project folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run app.py --server.port 8511
```

Alternatively run `bash setup_unix.sh` once, then `bash launch_unix.sh`. Some Linux installations require the distribution's Python venv package before creating an environment.

## Explore the app

- Select US or China in the case panel; change the electricity year.
- Click a country bar to update the persistent profile.
- Compare electricity shares or change since 2020.
- Choose an optional working hypothesis, then continue to the water evidence below.
- Compare a water-only country, switch drought/flood, and inspect the blind-spot zone.
- Finish with the country evidence brief and choose what local evidence to request next.
- Expand the tables and source trace to inspect exact values.

All four charts are rendered on initial load, with no reveal button or interaction required. On a narrow screen, open the collapsed side panel for the case controls.

## Troubleshooting

- **Port 8511 already in use:** close the previous server or run with `--server.port 8512`, then open http://localhost:8512.
- **Module missing:** repeat the requirements installation using the same `.venv` Python used to launch the app.
- **Data file missing:** extract the full ZIP, preserving `data/raw`, `data/processed` and the other subfolders.
- **Old interface shown:** confirm you launched the root `app.py`, not an individual dashboard under `contributors/`, then refresh the browser.
- **Dependency installation fails:** confirm 64-bit Python >=3.11 and a working internet connection. Share the actual installation error with the team.

## Editing and submission

The active frontend is `frontend.py`; the entry point is `app.py`. Shared loading and evidence helpers are in `story.py`. Individual originals remain under `contributors/` and `contributors/Apaar/`. See README.md and docs/INTEGRATION_REPORT.md for scope decisions and remaining release tasks.

The integrated app is deployed at https://powering-ai-energy-water.streamlit.app/. All four contributor folders are present. Submit the final PDF containing the actual assessed revision; see submission/RELEASE_STEPS.md. Archived member files are labelled separately from the active app inputs.
