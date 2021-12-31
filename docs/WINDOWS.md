# Windows Usage and Support

Support for Windows is no longer active.

## Usage
```bash
python3 -m venv .\.venv\
pip3 install virtualenv
.\.venv\Scripts\activate
pip3 install -r .\requirements.txt
python3 cloner --help
```

## Other & Troubleshooting

If we can't activate the virtual env in Windows10, review with this:

```bash
> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser
> Get-ExecutionPolicy -List
```
