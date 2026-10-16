# Fast TCP Port Scanner 🔍

Um scanner de portas TCP rápido e leve desenvolvido em Python. Este script utiliza `concurrent.futures.ThreadPoolExecutor` para realizar varreduras em múltiplas threads simultaneamente, reduzindo drasticamente o tempo necessário para escanear grandes intervalos de portas em comparação com abordagens sequenciais.

## 🚀 Funcionalidades

* **Alta Performance:** Utiliza *multithreading* para testar várias portas ao mesmo tempo.
* **Flexibilidade de Uso:** Suporta execução tanto via argumentos de linha de comando (CLI) quanto via interface interativa no terminal.
* **Timeout Customizável:** Permite ajustar o tempo de limite de conexão, adaptando-se a redes locais rápidas ou conexões remotas mais lentas.
* **Sem dependências externas:** Construído inteiramente com bibliotecas padrão do Python (`socket`, `concurrent.futures`, `sys`, `time`, `datetime`).

## 📋 Pré-requisitos

* Python 3.x instalado em sua máquina.

## 💻 Como Usar

Você pode rodar o script de duas maneiras:

### 1. Modo Interativo
Basta executar o script sem argumentos e ele solicitará as informações necessárias passo a passo:
```bash
