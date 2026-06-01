# it-cube-case-frontend-nyx-team

# Project Setup

## Windows

```powershell
cd <backend_folder>
```

```powershell
python -m venv venv
```

```powershell
.\venv\Scripts\Activate.ps1
```

```powershell
pip install -r requirements.txt
```

```powershell
uvicorn main:app --reload
```

## Podman (recommended)

```shell
podman build -t it-cube-case-frontend-nyx-team .
```

```shell
podman run -it --rm -p 8000:8000 it-cube-case-frontend-nyx-team
```