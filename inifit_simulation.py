import random


def fmt_int(n):
    return f"{n:,}".replace(",", ".")


def fmt_float(n):
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


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


def imprimir_resultado_final(cont_jogadas, premio_medio, maior_premio, menor_premio, media_rodadas, cont_caras, cont_coroas):
    print("\n" + "=" * 50)
    print("RESULTADO FINAL DA SIMULAÇÃO")
    print("=" * 50)
    print(f"Jogadas simuladas ........: {fmt_int(cont_jogadas)}")
    print(f"Prêmio médio .............: R$ {fmt_float(premio_medio)}")
    print(f"Maior prêmio .............: R$ {fmt_int(maior_premio)}")
    print(f"Menor prêmio .............: R$ {fmt_int(menor_premio)}")
    print(f"Média de rodadas/jogada ..: {fmt_float(media_rodadas)}")
    print(f"Total de caras ...........: {fmt_int(cont_caras)}")
    print(f"Total de coroas ..........: {fmt_int(cont_coroas)}")
    print("=" * 50)


def imprimir_distribuicao_rodadas(frequencia_rodadas):
    print("DISTRIBUIÇÃO DE RODADAS POR JOGADA")
    for qtd_rodadas in sorted(frequencia_rodadas):
        ocorrencias = frequencia_rodadas[qtd_rodadas]
        print(
            f"  {qtd_rodadas:>3} rodada(s) : {fmt_int(ocorrencias):>6} vez(s) || Prêmio: R$ {fmt_int(2 ** (qtd_rodadas - 1))}"
        )
    print("=" * 50)


def main():
    jogadas = 300
    print_cont_jogadas = 100
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

    imprimir_resultado_final(
        cont_jogadas, premio_medio, maior_premio, menor_premio, media_rodadas, cont_caras, cont_coroas
    )
    imprimir_distribuicao_rodadas(frequencia_rodadas)


if __name__ == "__main__":
    main()
