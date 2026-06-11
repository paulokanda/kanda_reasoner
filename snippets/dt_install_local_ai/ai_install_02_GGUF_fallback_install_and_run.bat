@echo off
setlocal ENABLEDELAYEDEXPANSION
REM === GGUF + llama.cpp fallback (Qwen2.5-Coder-14B-Instruct, Q5_K_M) ===

REM --- Paths ---
set "ENV_PREFIX=E:\my_deepseek"
set "WEBUI=%ENV_PREFIX%\text-generation-webui"
set "MODELS=%WEBUI%\models"
set "MODEL_DIR=%MODELS%\Qwen2.5-Coder-14B-Instruct-GGUF"

REM --- Network / API ---
set "PORT=5000"

REM --- Conda base + env ---
CALL "C:\Users\paulo\miniconda3\Scripts\activate.bat" || (echo [ERR] Conda base not found & pause & exit /b 1)
CALL conda activate "%ENV_PREFIX%" || (echo [ERR] Activate env failed & pause & exit /b 1)

REM --- WebUI present? ---
if not exist "%WEBUI%\server.py" (
  echo [ERR] WebUI not found at %WEBUI%. Run the EXL2 installer first.
  pause & exit /b 1
)

REM --- Make sure fast download pkgs exist (optional) ---
pip show hf_transfer >nul 2>&1 || pip install -U hf_transfer
pip show hf_xet >nul 2>&1 || pip install -U hf_xet
set HF_HUB_ENABLE_HF_TRANSFER=1

REM --- Download official GGUF (Q5_K_M) with NEW CLI ---
mkdir "%MODEL_DIR%" >nul 2>&1
hf download Qwen/Qwen2.5-Coder-14B-Instruct-GGUF ^
  --include "qwen2.5-coder-14b-instruct-q5_k_m*.gguf" ^
  --local-dir "%MODEL_DIR%" || (echo [ERR] GGUF download failed & pause & exit /b 1)

REM --- Pick the first matching file ---
set "GGUF_FILE="
for %%F in ("%MODEL_DIR%\qwen2.5-coder-14b-instruct-q5_k_m*.gguf") do (
  set "GGUF_FILE=%%~nxF"
  goto :gotfile
)
:gotfile
if "%GGUF_FILE%"=="" (echo [ERR] No GGUF file found & pause & exit /b 1)

REM --- Launch API (llama.cpp). Note: avoid --listen-host to prevent arg parsing issues ---
cd /d "%WEBUI%"
echo Starting GGUF llama.cpp server on http://127.0.0.1:%PORT% ...
set "CMD=python server.py --model ""Qwen2.5-Coder-14B-Instruct-GGUF\%GGUF_FILE%"" --loader llama.cpp --gpu-layers 80 --ctx-size 8192 --batch-size 64 --api --api-port %PORT% --listen --nowebui"
start "my_deepseek GGUF API" cmd /k "%CMD%"
timeout /t 3 >nul
start "" "http://127.0.0.1:%PORT%/docs"
exit /b 0
