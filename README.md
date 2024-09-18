# Gerente Expedição<br/>

## Objetivo:<br/>
Obter todos os pedidos com status com status de Faturado, Pronto para envio, Enviado e Não entregue e procurar as informações dos bips de produção e de envio desses pedidos para avaliar as pendências e o real andamento dos pedidos.<br/>
<br/>

## Arquitetura<br/>
* Python<br/>
* API Tiny V3<br/>
* API Intelipost<br/>
* API Smartphar<br/>
<br/>

## Execução do código<br/>
Na função main.py, nas linhas 54 e 55, preencher a data inicial e data final respectivamentes, no formato AAAA-MM-DD.<br/>
Executar a função e aguardar a geração do excel.<br/>
Cada linha deve trazer:<br/>
As informações do pedido: id, número, situação, data de criação, forma de frete.<br/>
As informaões da Intelipost: código de rastreamento, url de rastreamento, status e data de criação.<br/>
As informações do Smartphar: código req com sequêncial, status de produção (bip), horário do status, data programada de saída.<br/>
<br/>
