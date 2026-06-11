@echo off
REM Start DeepSeek LLM manually (no Conda)

cd /d "E:\deepseek\text-generation-webui"
echo Verificando/instalando dependencias...
pip install -r requirements/full/requirements.txt --no-cache-dir

echo Iniciando o servidor com WizardCoder...
python server.py --model-dir models --model WizardCoder-Python-13B-GGUF/ggml-model.gguf --loader llama.cpp --gpu-layers 35 --threads 12 --listen

pause
