# 📦 Gerente de Expedição Miligrama

## 📋 Descrição

Este projeto em Python foi desenvolvido para cruzar os status dos pedidos de diferentes plataformas:  

- **Olist Tiny** → Status do pedido  
- **Smartphar** → Status de produção  
- **Intelipost** → Status de envio  

O resultado do cruzamento de dados é uma planilha que permite acompanhar de forma consolidada a situação de cada pedido, facilitando a gestão da expedição.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.  
- **Bibliotecas Principais**:
  - `pandas`: Para manipulação e análise dos dados.
  - `openpyxl`: Para geração da planilha consolidada.
  - `requests`: Para comunicação com APIs das plataformas.

## 🚀 Como Utilizar o Projeto

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/lyraleo23/gerente-expedicao-miligrama.git
cd gerente-expedicao-miligrama
```

### Passo 2: Instalar Dependências
Certifique-se de ter o Python instalado. Instale as dependências listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Passo 3: Executar o Script Principal
O script coleta os dados das plataformas e gera uma planilha consolidada:
```bash
python main.py
```

### Passo 4: Analisar a Planilha
O arquivo gerado será salvo no diretório raíz, contendo o cruzamento dos status dos pedidos.

### 📄 Estrutura do Projeto  
```markdown
📂 gerente-expedicao-miligrama  
 ├── main.py              # Script principal para cruzamento de status dos pedidos  
 ├── requirements.txt     # Arquivo com as dependências do projeto  
 ├── README.md            # Documentação do projeto  
 ├── input/               # Pasta para arquivos de entrada (se necessário)  
 └── output/              # Pasta onde a planilha consolidada será salva  
```

## 🧠 Conceitos Aplicados

- **Integração de APIs**: Comunicação com Olist Tiny, Smartphar e Intelipost.
- **Manipulação de Dados com Pandas**: Cruzamento de informações e análise de status.
- **Geração de Relatórios**: Criação de planilhas consolidadas para facilitar a visualização e gestão dos pedidos.

## 🤝 Contribuições

Contribuições são bem-vindas! Caso encontre melhorias ou problemas, sinta-se à vontade para abrir issues ou pull requests.

## 📞 Contato

- **Autor**: Leonardo Lyra  
- **GitHub**: [lyraleo23](https://github.com/lyraleo23)  
- **LinkedIn**: [Leonardo Lyra](https://www.linkedin.com/in/leonardo-lyra/)  
