import os
import random
import sys
from datetime import datetime

JOGADAS_PADRAO = 500


def fmt_int(n):
    return f"{n:,}".replace(",", ".")


def fmt_float(n):
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def nova_config_entrada(preco_entrada):
    return {
        "preco_entrada": preco_entrada,
        "resultado_acc": 0,
        "parada_com_lucro": [],
        "em_lucro": False,
    }


def simular_jogada():
    rodadas = 1
    premio = 1
    caras = 0
    coroas = 0

    sorteio = True
    while sorteio:
        sorteio = random.random() <= 0.5
        if sorteio:
            caras += 1
            rodadas += 1
            premio *= 2
        else:
            coroas += 1

    return premio, rodadas, caras, coroas


def atualizar_lucro_prejuizo(lucro_prejuizo, premio, rodadas, cont_jogadas):
    for entrada in lucro_prejuizo:
        entrada["resultado_acc"] += premio - entrada["preco_entrada"]

        if entrada["resultado_acc"] > 0 and not entrada["em_lucro"]:
            entrada["em_lucro"] = True
            entrada["parada_com_lucro"].append(
                {"jogada": cont_jogadas, "rodadas": rodadas, "lucro": entrada["resultado_acc"]}
            )
        elif entrada["resultado_acc"] <= 0 and entrada["em_lucro"]:
            entrada["em_lucro"] = False


def escrever(arquivo, texto=""):
    print(texto)
    arquivo.write(texto + "\n")


def imprimir_resultado_final(arquivo, cont_jogadas, premio_medio, maior_premio, menor_premio, media_rodadas, cont_caras, cont_coroas):
    escrever(arquivo, "\n" + "=" * 50)
    escrever(arquivo, "RESULTADO FINAL DA SIMULAÇÃO")
    escrever(arquivo, "=" * 50)
    escrever(arquivo, f"Jogadas simuladas ........: {fmt_int(cont_jogadas)}")
    escrever(arquivo, f"Prêmio médio .............: R$ {fmt_float(premio_medio)}")
    escrever(arquivo, f"Maior prêmio .............: R$ {fmt_int(maior_premio)}")
    escrever(arquivo, f"Menor prêmio .............: R$ {fmt_int(menor_premio)}")
    escrever(arquivo, f"Média de rodadas/jogada ..: {fmt_float(media_rodadas)}")
    escrever(arquivo, f"Total de caras ...........: {fmt_int(cont_caras)}")
    escrever(arquivo, f"Total de coroas ..........: {fmt_int(cont_coroas)}")
    escrever(arquivo, "=" * 50)


def imprimir_distribuicao_rodadas(arquivo, frequencia_rodadas):
    escrever(arquivo, "=" * 50)
    escrever(arquivo, "DISTRIBUIÇÃO DE RODADAS POR JOGADA")
    for qtd_rodadas in sorted(frequencia_rodadas):
        ocorrencias = frequencia_rodadas[qtd_rodadas]
        escrever(
            arquivo,
            f"  {qtd_rodadas:>3} rodada(s) : {fmt_int(ocorrencias):>6} vez(s) || Prêmio: R$ {fmt_int(2 ** (qtd_rodadas - 1))}"
        )
    escrever(arquivo, "=" * 50)


def imprimir_lucro_prejuizo(arquivo, lucro_prejuizo, cont_jogadas, limite_pontos=50):
    escrever(arquivo, "RESULTADO POR PREÇO DE ENTRADA")
    escrever(arquivo, f"Resultado Acc = Resultado acumulado após jogar todas as {fmt_int(cont_jogadas)} vezes")
    escrever(arquivo, "Chances de saída => Em quantas jogadas saiu com lucro")
    for entrada in lucro_prejuizo:
        situacao = "LUCRO" if entrada["resultado_acc"] > 0 else "PREJUÍZO"
        escrever(
            arquivo,
            f"  Entrada R$ {fmt_int(entrada['preco_entrada']):>3} ..: "
            f"resultado acumulado R$ {fmt_float(entrada['resultado_acc']):>12} ({situacao}) "
            f"|| ficou positivo {fmt_int(len(entrada['parada_com_lucro']))}x"
        )
    escrever(arquivo, "=" * 50)
    escrever(arquivo, "\n")
    escrever(arquivo, "=" * 50)

    for entrada in lucro_prejuizo:
        if not entrada["parada_com_lucro"]:
            continue
        escrever(arquivo, f"  Entrada R${fmt_int(entrada['preco_entrada']):>3},00 parou com lucro em nos seguintes pontos:")
        for ponto in entrada["parada_com_lucro"][:limite_pontos]:
            # escrever(arquivo, str(ponto))
            jogada, rodadas, lucro = ponto.values()
            escrever(arquivo, f"Jogada: {jogada} | Rodadas: {rodadas} | Lucro: R$ {fmt_int(lucro)}")
        escrever(arquivo, "=" * 50)


def main():
    jogadas = int(sys.argv[1]) if len(sys.argv) > 1 else JOGADAS_PADRAO
    print_cont_jogadas = max(1, jogadas // 50)
    cont_jogadas = 0

    premio_acc = 0
    premio_medio = 0
    maior_premio = 0
    menor_premio = 0

    rodadas_acc = 0
    media_rodadas = 0
    frequencia_rodadas = {}

    cont_caras = 0
    cont_coroas = 0

    lucro_prejuizo = [nova_config_entrada(preco) for preco in range(5, 51, 5)]

    print("=" * 50)
    print("SIMULAÇÃO DO PARADOXO DE SÃO PETERSBURGO")
    print(f"Total de jogadas a simular: {jogadas}")
    print("=" * 50)

    while cont_jogadas < jogadas:
        cont_jogadas += 1
        if cont_jogadas % print_cont_jogadas == 0:
            print(f"\n--- Jogada {fmt_int(cont_jogadas)}/{fmt_int(jogadas)} ---")

        premio, rodadas, caras, coroas = simular_jogada()
        cont_caras += caras
        cont_coroas += coroas

        atualizar_lucro_prejuizo(lucro_prejuizo, premio, rodadas, cont_jogadas)

        premio_acc += premio
        rodadas_acc += rodadas
        frequencia_rodadas[rodadas] = frequencia_rodadas.get(rodadas, 0) + 1

        if cont_jogadas == 1:
            maior_premio = premio
            menor_premio = premio
        else:
            maior_premio = max(maior_premio, premio)
            menor_premio = min(menor_premio, premio)

        premio_medio = premio_acc / cont_jogadas
        media_rodadas = rodadas_acc / cont_jogadas

    pasta_resultados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resultados")
    os.makedirs(pasta_resultados, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho_arquivo = os.path.join(pasta_resultados, f"simulacao_{fmt_int(jogadas)}_jogadas-{timestamp}.txt")

    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
        imprimir_resultado_final(
            arquivo, cont_jogadas, premio_medio, maior_premio, menor_premio, media_rodadas, cont_caras, cont_coroas
        )
        imprimir_distribuicao_rodadas(arquivo, frequencia_rodadas)
        imprimir_lucro_prejuizo(arquivo, lucro_prejuizo, cont_jogadas)

    print(f"\nResultado salvo em: {caminho_arquivo}")


if __name__ == "__main__":
    main()
