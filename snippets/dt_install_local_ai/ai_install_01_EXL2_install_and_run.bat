@echo off
setlocal ENABLEDELAYEDEXPANSION
REM === EXL2 + exllamav2 (Qwen2.5-Coder-14B-Instruct EXL2) ===

REM --- Paths ---
set "ENV_PREFIX=E:\my_deepseek"
set "WEBUI=%ENV_PREFIX%\text-generation-webui"
set "MODELS=%WEBUI%\models"
set "MODEL_DIR=%MODELS%\Qwen2.5-Coder-14B-Instruct-exl2"
set "EXL2_BRANCH=6_5"   REM 6_5 = mais qualidade (usa mais VRAM)

REM --- Network / API ---
set "HOST=127.0.0.1"
set "PORT=5000"

REM --- Conda base ---
CALL "C:\Users\paulo\miniconda3\Scripts\activate.bat" || (echo [ERR] Conda base not found & pause & exit /b 1)

REM --- Cria/ativa env (Python 3.11) ---
if not exist "%ENV_PREFIX%\python.exe" (
  conda create -y -p "%ENV_PREFIX%" python=3.11 || (echo [ERR] Failed to create env & pause & exit /b 1)
)
CALL conda activate "%ENV_PREFIX%" || (echo [ERR] Failed to activate env & pause & exit /b 1)

REM --- PyTorch CUDA 12.4 (estável p/ 40xx) ---
pip install --index-url https://download.pytorch.org/whl/cu124 ^
  torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 || (echo [ERR] Torch install failed & pause & exit /b 1)

REM --- WebUI (se faltar) ---
if not exist "%WEBUI%\.git" (
  mkdir "%ENV_PREFIX%" >nul 2>&1
  cd /d "%ENV_PREFIX%"
  git clone https://github.com/oobabooga/text-generation-webui || (echo [ERR] git clone failed & pause & exit /b 1)
)

REM --- Dependencias WebUI (full) ---
cd /d "%WEBUI%" || (echo [ERR] WebUI path missing & pause & exit /b 1)
pip install -r requirements\full\requirements.txt --no-cache-dir || (echo [ERR] pip install failed & pause & exit /b 1)

REM --- Garante exllamav2 compatível com Torch 2.6.0 + cu124 ---
pip uninstall -y exllamav2 exllamav3 flash-attn >nul 2>&1
pip install "https://github.com/turboderp-org/exllamav2/releases/download/v0.3.1/exllamav2-0.3.1+cu124.torch2.6.0-cp311-cp311-win_amd64.whl" || (echo [ERR] exllamav2 pin failed & pause & exit /b 1)

REM --- HF client (novo) + aceleração de download opcional ---
pip install -U "huggingface_hub[cli]" || (echo [ERR] HF tools failed & pause & exit /b 1)
setx HF_HUB_ENABLE_HF_TRANSFER 1 >nul

REM --- Baixa o modelo EXL2 (branch = %EXL2_BRANCH%) ---
mkdir "%MODEL_DIR%" >nul 2>&1
hf download bartowski/Qwen2.5-Coder-14B-Instruct-exl2 --revision %EXL2_BRANCH% --local-dir "%MODEL_DIR%" --exclude ".git/*" || (echo [ERR] EXL2 download failed & pause & exit /b 1)

REM --- Sobe API (exllamav2). Ajuste ctx-size conforme VRAM ---
echo.
echo Starting EXL2 server on http://%HOST%:%PORT% ...
start "my_deepseek EXL2 API" cmd /k ^
  python server.py ^
    --model "Qwen2.5-Coder-14B-Instruct-exl2" ^
    --loader exllamav2 ^
    --api --api-port %PORT% ^
    --listen --listen-host=%HOST% ^
    --nowebui ^
    --threads 16 ^
    --batch-size 128 ^
    --ctx-size 4096

timeout /t 3 >nul
start "" "http://%HOST%:%PORT%/docs"
exit /b 0
