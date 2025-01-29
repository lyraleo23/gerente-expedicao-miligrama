import os
import pandas as pd
from dotenv import load_dotenv
import time
import datetime
from api_smart import login_smart, status_receita
from api_miliapp import obter_tokens_tiny, get_vendas_filtro
from api_tiny_v3 import obter_pedidos_v3
from api_intelipost import consulta_entrega

load_dotenv()
CNPJ = str(os.getenv('CNPJ'))
USERNAME_ = str(os.getenv('USERNAME_'))
PASSWORD = str(os.getenv('PASSWORD'))
TOKEN_MILIAPP = str(os.getenv('TOKEN_MILIAPP'))
TOKEN_SMART = login_smart(CNPJ, USERNAME_, PASSWORD)
TOKEN_INTELIPOST = str(os.getenv('TOKEN_INTELIPOST'))
ACCESS_TOKEN, REFRESH_TOKEN = obter_tokens_tiny(TOKEN_MILIAPP, 'miligrama')

def main():
    start_time = time.time()
    xlsx_list = [
        [
            'id',
            'numero_pedido',
            'tipo_interno',
            'situacao_nome',
            'data_criacao',
            'forma_frete_nome',
            'codigo_rastreamento',
            'url_rastreamento',
            'status_intelipost',
            'created_iso_intelipost',
            'req',
            'status_bip_smart',
            'horario_bip_smart',
            'data_saida_smart'
        ]
    ]
    lista_situacao = [
        1,  #Faturado
        7,  #Pronto para envio
        5,  #Enviado
        9   #Não entregue
    ]
    lista_pedidos = []
    lista_req = []
    prazo_envio = 3

    for situacao in lista_situacao:
        os.system('cls')
        print(f'Buscando pedidos no status: {situacao}')
        params = {
            'situacao': situacao,
            'orderBy': 'asc',
            'dataInicial': '2024-06-01',
            # 'dataFinal': '2024-10-31'
        }
        lista_parcial = obter_pedidos_v3(ACCESS_TOKEN, params)
        print(len(lista_parcial))
        lista_pedidos = [*lista_pedidos, *lista_parcial]
        print(f'lista_pedidos: {len(lista_pedidos)}')
    print(f'total: {len(lista_pedidos)}')

    count = 0

    for pedido_atual in lista_pedidos:
        count = count + 1
        os.system('cls')
        print(f'===== {count}/{len(lista_pedidos)} =====')
        id = pedido_atual['id']
        situacao = pedido_atual['situacao']
        numero_pedido = pedido_atual['numeroPedido']
        print(numero_pedido)
        ecommerce = pedido_atual['ecommerce']
        data_criacao = pedido_atual['dataCriacao']
        transportador = pedido_atual['transportador']
        try:
            if transportador != None:
                forma_frete_nome = transportador['formaFrete']['nome']
                codigo_rastreamento = transportador['codigoRastreamento']
                url_rastreamento = transportador['urlRastreamento']
            else:
                forma_frete_nome = ''
                codigo_rastreamento = ''
                url_rastreamento = ''
        except Exception as e:
            print(e)
            forma_frete_nome = ''
            codigo_rastreamento = ''
            url_rastreamento = ''

        match situacao:
            case 0:
                situacao_nome = 'aberto'
            case 1:
                situacao_nome = 'faturado'
            case 2:
                situacao_nome = 'cancelado'
            case 3:
                situacao_nome = 'aprovado'
            case 4:
                situacao_nome = 'preparando_envio'
            case 5:
                situacao_nome = 'enviado'
            case 6:
                situacao_nome = 'entregue'
            case 7:
                situacao_nome = 'pronto_envio'
            case 8:
                situacao_nome = 'dados_incompletos'
            case 9:
                situacao_nome = 'nao_entregue'

        # ===== Busca as informações do pedido no miliapp =====
        try:
            pedido_miliapp = get_vendas_filtro(TOKEN_MILIAPP, numero_pedido)
            req_smart_list = pedido_miliapp.get('req_smart_list', [])
            numero_nota_fiscal = pedido_miliapp.get('numero_nota_fiscal', '')
            pedido_tipo_interno = pedido_miliapp.get('pedido_tipo_interno', '')
        except Exception as e:
            print(e)
            nova_linha = [id, numero_pedido, '', situacao_nome, data_criacao, forma_frete_nome, codigo_rastreamento, url_rastreamento, '', '', '']
            xlsx_list.append(nova_linha)
            continue

        # ===== Busca as informações do pedido na intelipost =====
        try:
            if ecommerce != None:
                try:
                    print('Buscando pelo numero e-commerce')
                    pedido_entrega = ecommerce['numeroPedidoEcommerce']
                    if pedido_entrega.find('-') == 3:
                        pedido_entrega = pedido_entrega[4:]
                    pedido_intelipost = consulta_entrega(TOKEN_INTELIPOST, pedido_entrega)
                    status_intelipost = pedido_intelipost['content']['shipment_order_volume_array'][0]['shipment_order_volume_state_localized']
                    created_iso_intelipost = pedido_intelipost['content']['shipment_order_volume_array'][0]['created_iso']
                except Exception as e:
                    print(e)
                    print('Buscando pelo nfe')
                    pedido_entrega = numero_nota_fiscal
                    pedido_intelipost = consulta_entrega(TOKEN_INTELIPOST, pedido_entrega)
                    status_intelipost = pedido_intelipost['content']['shipment_order_volume_array'][0]['shipment_order_volume_state_localized']
                    created_iso_intelipost = pedido_intelipost['content']['shipment_order_volume_array'][0]['created_iso']
            else:
                try:
                    print('Buscando pelo nfe')
                    pedido_entrega = numero_nota_fiscal
                    pedido_intelipost = consulta_entrega(TOKEN_INTELIPOST, pedido_entrega)
                    status_intelipost = pedido_intelipost['content']['shipment_order_volume_array'][0]['shipment_order_volume_state_localized']
                    created_iso_intelipost = pedido_intelipost['content']['shipment_order_volume_array'][0]['created_iso']
                except Exception as e:
                    print(f'Erro ao buscar dados na intelipost: {e}')
                    pedido_intelipost = None
                    status_intelipost = ''
                    created_iso_intelipost = ''
        except Exception as e:
            print(f'Erro ao buscar dados na intelipost: {e}')
            pedido_intelipost = None
            status_intelipost = ''
            created_iso_intelipost = ''
        print(f'status_intelipost: {status_intelipost}')
        print(f'created_iso_intelipost: {created_iso_intelipost}')

        if len(req_smart_list) > 0:
            for k in range(0, len(req_smart_list)):
                try:
                    codigo_req = req_smart_list[k]['codigo_req']
                    params = {
                        'page': 1,
                        'codigorec': codigo_req
                    }
                    response_status_smart = status_receita(TOKEN_SMART, params)
                    response_status_smart = response_status_smart.json()

                    qtd_sequenciais = len(response_status_smart)
                    print(f'qtd_sequenciais: {qtd_sequenciais}')

                    for x in range(0, qtd_sequenciais):
                        indice = response_status_smart[x]['indice']
                        data_saida = response_status_smart[x]['datasaida']
                        codigo_status_bip_smart = response_status_smart[x]['recstatus'][-1]['codigosp']
                        horario_status_bip_smart = response_status_smart[x]['recstatus'][-1]['created_at']

                        match codigo_status_bip_smart:
                            case 2:
                                status_bip_smart = 'PCP'
                            case 3:
                                status_bip_smart = 'FARMACÊUTICA'
                            case 4:
                                status_bip_smart = 'PESAGEM'
                            case 5:
                                status_bip_smart = 'ENCAPSULAÇÃO'
                            case 6:
                                status_bip_smart = 'P. MÉDIO / ENVASE'
                            case 7:
                                status_bip_smart = 'FINALIZAÇÃO'
                            case 8:
                                status_bip_smart = 'DERMATO'
                            case 9:
                                status_bip_smart = 'HOMEOPATIA'
            
                        nova_linha = [
                            id,
                            numero_pedido,
                            pedido_tipo_interno,
                            situacao_nome,
                            data_criacao,
                            forma_frete_nome,
                            codigo_rastreamento,
                            url_rastreamento,
                            status_intelipost,
                            created_iso_intelipost,
                            f'{codigo_req}-{indice}',
                            status_bip_smart,
                            horario_status_bip_smart,
                            data_saida
                        ]
                        xlsx_list.append(nova_linha)
                        df = pd.DataFrame(xlsx_list)
                        df.to_excel(f'lista_pedidos.xlsx', index=True, header=False)
                except Exception as e:
                    print(f'Erro ao buscar dados no smart: {e}')
                    codigo_req = ''
                    status_bip_smart = ''
                    horario_status_bip_smart = ''
                    data_saida = ''

                    nova_linha = [
                        id,
                        numero_pedido,
                        pedido_tipo_interno,
                        situacao_nome,
                        data_criacao,
                        forma_frete_nome,
                        codigo_rastreamento,
                        url_rastreamento,
                        status_intelipost,
                        created_iso_intelipost,
                        codigo_req,
                        status_bip_smart,
                        horario_status_bip_smart,
                        data_saida
                    ]
                    xlsx_list.append(nova_linha)
                    df = pd.DataFrame(xlsx_list)
                    df.to_excel(f'lista_pedidos.xlsx', index=True, header=False)

        else:
            data_saida = data_criacao
            data_saida = data_saida.split('-')
            data_saida = datetime.datetime(int(data_saida[0]), int(data_saida[1]), int(data_saida[2]))
            while prazo_envio > 0:
                print(f'type: {type(data_saida.strftime('%d'))}')
                dia = int(data_saida.strftime('%d')) + 1
                mes = int(data_saida.strftime('%m'))
                ano = int(data_saida.strftime('%Y'))
                data_saida = datetime.datetime(ano, mes, dia)

                if data_saida.strftime('%w') != 0 and data_saida.strftime('%w') != 6:
                    prazo_envio = prazo_envio - 1

                print(f'prazo_envio: {prazo_envio}')
                print(f'data_saida: {data_saida}')
            codigo_req = ''
            status_bip_smart = ''
            horario_status_bip_smart = ''
            
            nova_linha = [
                id,
                numero_pedido,
                pedido_tipo_interno,
                situacao_nome,
                data_criacao,
                forma_frete_nome,
                codigo_rastreamento,
                url_rastreamento,
                status_intelipost,
                created_iso_intelipost,
                codigo_req,
                status_bip_smart,
                horario_status_bip_smart,
                data_saida
            ]
            xlsx_list.append(nova_linha)
            df = pd.DataFrame(xlsx_list)
            df.to_excel(f'lista_pedidos.xlsx', index=True, header=False)
            
    # Horário da impressão
    now = datetime.datetime.now()
    now = str(now)
    now = now.split(' ')
    data = now[0]
    hora = now[1].split('.')
    hora = hora[0].replace(':','_')
    os.rename('lista_pedidos.xlsx', f'lista_pedidos_envios_pendentes_{data}_{hora}.xlsx')
    execution_time = time.time() - start_time
    os.system('cls')
    print("Execution time in seconds: " + str(execution_time))
    print('Concluído!')
    return

main()
