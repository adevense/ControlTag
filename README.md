# ControlTag

## Como rodar o aplicativo

1. Crie o ambiente virtual (se ainda não existir):
   ```sh
   python -m venv .venv
   ```
2. Ative o ambiente virtual:
   - **Windows:**
     ```sh
     .venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```sh
     source .venv/bin/activate
     ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```
4. Execute o sistema:
   ```sh
   python run.py
   ```

## Como rodar os testes

```sh
python -m unittest discover tests
```

## Como rodar os testes com cobertura

1. Instale o pacote de cobertura (se ainda não tiver):
   ```sh
   pip install coverage
   ```
2. Execute os testes com cobertura:
   ```sh
   coverage run -m unittest discover tests
   coverage report -m
   ```
