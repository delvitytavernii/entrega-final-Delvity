import os
import re

import pandas as pd


def imprimeLogo():
    """Imprime a logo da cafeteria"""
    print("========================\n")
    print("  CAFETERIA CHEVONICA\n")
    print("========================\n")


def imprimeOpcoes():
    """Imprime as 6 opções do menu: Add, excluir, alterar, buscar e listar item, além da opção de sair"""
    print("Selecione uma das opções:")
    print("1 - Adicionar item ao cardapio")
    print("2 - Excluir item do cardapio")
    print("3 - Alterar item do cardapio")
    print("4 - Buscar item do cardapio")
    print("5 - Listar todos os itens do cardápio")
    print("6 - Realizar pedido")
    print("7 - Sair")


def limpaATela():
    """Essa função limpa a tela do console"""
    print("")
    clear = lambda: os.system("clear")
    clear()


def leEntradaDoUsuario(texto: str):
    """Essa é igual a uma função input, ela recebe o texto que será exibido para o usuário e retorna o que o usuário digitou. Lembrando que o que a gente recebe de uma função input é uma string!"""
    return input(texto)


def entradaEhNumeroInteiro(entrada: str):
    """Essa função serve para validar se a entrada do usuário foi um número inteiro"""
    try:
        int(entrada)
        return True
    except:
        return False


def entradaEhNumeroFlutuante(entrada: str):
    """Essa função serve para validar se a entrada do usuário foi um número de ponto flutuante, ou seja, um número com virgula"""
    try:
        float(entrada)
        return True
    except:
        return False


def entradaEntreDoisNumeros(entrada: str, minimo: int, maximo: int):
    """
    Essa função recebe 3 parâmetros:\n
    1o - string - A entrada do usuário\n
    2o - inteiro - O menor número possivel para a entrada\n
    3o - inteiro - O maior número possivel para a entrada\n
    Ela vai pegar a entrada, validar se o usuário digitou um número inteiro, e depois verifica se esta dentro do range esperado.
    Se estiver tudo certo, ele retorna a entrada como um número inteiro, se não, a função irá retornar -1
    """
    if (
        entradaEhNumeroInteiro(entrada)
        and int(entrada) >= minimo
        and int(entrada) <= maximo
    ):
        return int(entrada)
    else:
        print(f"\nEntrada invalida! Digite um número entre {minimo} e {maximo}!\n")
        return -1


def escolherCategoriaDoItem():
    """Essa função informa as categorias possiveis e aceita apenas uma das categorias já informadas. Depois ela retorna a categoria escolhida pelo usuário"""
    catagorias = ["Bebida", "Entrada", "Prato principal", "Sobremesa"]
    categoriaValidada = -1
    while categoriaValidada == -1:
        print("Digite a categoria do item:")
        print("1 - Bebida")
        print("2 - Entrada")
        print("3 - Prato principal")
        print("4 - Sobremesa")
        categoria = leEntradaDoUsuario("Selecione uma opção entre 1 e 4: ")
        categoriaValidada = entradaEntreDoisNumeros(categoria, 1, 4)
    return catagorias[categoriaValidada - 1]


def definirValorDoItem():
    """Essa função a gente vai usar para saber o valor do item. O valor do item precisa ser:\n
    - Um número de ponto flutuante\n
    - Um número maior do que zero\n
    Se atende a esses dois requisitos, o número é aceito e retornado pela função"""
    valorItem = -1
    while valorItem == -1:
        valorItem = leEntradaDoUsuario("Digite o valor do produto: ")
        if entradaEhNumeroFlutuante(valorItem) and float(valorItem) > 0:
            valorItem = float(valorItem)
        else:
            print("Digite um valor valido!")
            valorItem = -1
    return valorItem


def adicionarLinhaAoDataframe(dataframeOriginal: object, linhaASerAdicionada: object):
    """Essa função apenas adiciona uma linha nova ao dataframe.\n
    Por conta de alguns problemas de performance, na versão 2.0 do pandas a função append foi depreciada. Por conta disso precisamos usar a função concat.\n
    Essa função recebe o dataframe original e a linha com os itens que devem ser adicionados. Por conta do funcionamento da biblioteca do pandas, precisamos passar essa nova linha como um array de array:
    [[itens, a, serem, adicionados]]
    """
    return pd.concat(
        [
            dataframeOriginal,
            pd.DataFrame(
                linhaASerAdicionada,
                columns=["Categoria", "Subcategoria", "NomeItem", "ValorItem"],
            ),
        ],
        ignore_index=True,
    )


def adicionarItemAoCardapio(dataframeOriginal: object):
    """Função usada para adicionar um item ao cardápio do restaurante"""
    limpaATela()
    categoriaDoItem = escolherCategoriaDoItem()
    subcategoriaDoItem = leEntradaDoUsuario("Digite qual é a subcategoria do produto: ")
    nomeDoItem = leEntradaDoUsuario("Digite o nome do item: ")
    valorDoItem = definirValorDoItem()
    itensASeremAdicionados = [
        [categoriaDoItem, subcategoriaDoItem, nomeDoItem, valorDoItem]
    ]
    dataframeComANovaLinha = adicionarLinhaAoDataframe(
        dataframeOriginal, itensASeremAdicionados
    )
    return dataframeComANovaLinha


def formataNumeroComVirgula(numero: float):
    """Essa função pega um número com virgula e retorna ele com duas casas decimais, ideal para imprimir como dinheiro"""
    return "%.2f" % numero


def ordenaListaDeItens(listaDeItens: object):
    """Essa função pega o Dataframe e ordena ele baseado primeiro nas categorias e, dentro delas, ordena baseado nas subcategorias"""
    return listaDeItens.sort_values(["Categoria", "Subcategoria"])


def dataframeParaLista(dataframeDeItens: object):
    """Essa função transforma um Dataframe em um array de arrays, e depois retorna ele"""
    return dataframeDeItens.to_numpy()


def listaParaDataFrame(listaDeItens: object):
    """Essa função pega uma lista e retorna um dataframe com as colunas da maneira correta"""
    df_itens = pd.DataFrame(
        listaDeItens, columns=["Categoria", "Subcategoria", "NomeItem", "ValorItem"]
    )
    return df_itens


def listaItensDoCardapioCompleto(listaDeItens: object):
    """Essa função recebe um dataframe com os itens do cardapio e lista eles para o usuário.\n
    A lista de itens aparece organizada!"""
    dataframeOrdenado = ordenaListaDeItens(listaDeItens)
    dataframeComoLista = dataframeParaLista(dataframeOrdenado)
    categoria = ""
    subcategoria = ""
    limpaATela()
    for i in dataframeComoLista:
        if i[0] != categoria:
            print("======================")
            print(i[0])
            categoria = i[0]
        if i[1] != subcategoria:
            print(f"  {i[1]}")
            subcategoria = i[1]
        print(f"    {i[2]} - R$ {formataNumeroComVirgula(i[3])}")
    print("======================\n")


def listaItensDoCardapioCompacta(listaDeItens: object):
    """Essa função recebe o array com os itens do estoque e lista eles para o usuário.\n
    A lista de itens NÃO aparece organizada! Ela esta na mesma ordem do Dataframe.
    """
    dataframeComoLista = dataframeParaLista(listaDeItens)
    print("Cód | Categoria | Subcategoria | Item")
    for i in range(len(dataframeComoLista)):
        print(
            f"{i+1} | {dataframeComoLista[i][0]} | {dataframeComoLista[i][1]} | {dataframeComoLista[i][2]}"
        )


def excluiItemDoDataFrame(dataFrame, indiceDoItem):
    """Essa função recebe um Dataframe e um índice, esse índice é a linha que a gente quer excluir. Ela retorna o Dataframe sem a linha que a gente pediu para remover."""
    return dataFrame.drop(dataFrame.index[indiceDoItem])


def excluirItemDoCardapio(listaDeItens: object):
    """Essa é a função que cuida da remoção de itens do cardapio"""
    listaItensDoCardapioCompacta(listaDeItens)
    itemASerExcluidoValidado = -1
    while itemASerExcluidoValidado == -1:
        itemASerExcluido = leEntradaDoUsuario(
            "Selecione o código de um item da lista ou 0 para voltar: "
        )
        itemASerExcluidoValidado = entradaEntreDoisNumeros(
            itemASerExcluido, 0, len(listaDeItens)
        )
        if itemASerExcluidoValidado == 0:
            return listaDeItens
        elif itemASerExcluidoValidado != -1:
            return excluiItemDoDataFrame(listaDeItens, itemASerExcluidoValidado - 1)


def editaCategoria(valorOriginal):
    print(f"A categoria atual é {valorOriginal}, qual é a nova categoria?")
    catagorias = ["Bebida", "Entrada", "Prato principal", "Sobremesa"]
    categoriaValidada = -1
    while categoriaValidada == -1:
        print("1 - Bebida")
        print("2 - Entrada")
        print("3 - Prato principal")
        print("4 - Sobremesa")
        categoria = leEntradaDoUsuario(
            "Selecione uma opção entre 1 e 4 ou 0 para cancelar a edição: "
        )
        categoriaValidada = entradaEntreDoisNumeros(categoria, 0, 4)
    if categoriaValidada == 0:
        return valorOriginal
    return catagorias[categoriaValidada - 1]


def editaSubcategoria(valorOriginal):
    print(f"A subcategoria atual é {valorOriginal}")
    subcategoria = leEntradaDoUsuario(
        "Digite a subcategoria do item 0 para cancelar a edição: "
    )
    if subcategoria == "0":
        return valorOriginal
    return subcategoria


def editaNome(valorOriginal):
    print(f"O nome atual é {valorOriginal}")
    nome = leEntradaDoUsuario("Digite o novo do item 0 para cancelar a edição: ")
    if nome == "0":
        return valorOriginal
    return nome


def editavalor(valorOriginal):
    print(f"O valor atual é {valorOriginal}")
    valor = leEntradaDoUsuario(
        "Digite o novo valor do item ou 0 para cancelar a edição: "
    )
    while True:
        if valor == 0:
            return valorOriginal
        elif entradaEhNumeroFlutuante(valor) and float(valor) > 0:
            return float(valor)
        else:
            valor = leEntradaDoUsuario(
                "Valor invalido, digite um número maior do que zero ou 0 para cancelar a edição"
            )


def editarCampo(codigoDoCampo, valorOriginal):
    if codigoDoCampo == 1:
        return editaCategoria(valorOriginal)
    elif codigoDoCampo == 2:
        return editaSubcategoria(valorOriginal)
    elif codigoDoCampo == 3:
        return editaNome(valorOriginal)
    elif codigoDoCampo == 4:
        return editavalor(valorOriginal)


def editarItem(itemASerEditado):
    limpaATela()
    while True:
        print(f"1- Categoria atual do item: {itemASerEditado[0]}")
        print(f"2- Subcategoria atual do item: {itemASerEditado[1]}")
        print(f"3- Nome atual do item: {itemASerEditado[2]}")
        print(f"4- Valor atual do item: {itemASerEditado[3]}")
        campoASerEditado = leEntradaDoUsuario(
            "Selecione o que você deseja editar ou digite 0 para terminar a edição: "
        )
        campoASerEditadoValidado = entradaEntreDoisNumeros(campoASerEditado, 0, 4)
        if campoASerEditadoValidado == 0:
            return itemASerEditado
        elif campoASerEditadoValidado != -1:
            itemASerEditado[campoASerEditadoValidado - 1] = editarCampo(
                campoASerEditadoValidado,
                itemASerEditado[campoASerEditadoValidado - 1],
            )


def alterarItemDoCardapio(listaDeItens: object):
    limpaATela()
    listaItensDoCardapioCompacta(listaDeItens)
    itemASerEditadoValidado = -1
    while itemASerEditadoValidado == -1:
        itemASerEditado = leEntradaDoUsuario(
            "Selecione o código de um item da lista ou 0 para voltar: "
        )
        itemASerEditadoValidado = entradaEntreDoisNumeros(
            itemASerEditado, 0, len(listaDeItens)
        )
        if itemASerEditadoValidado == 0:
            return listaDeItens
        elif itemASerEditadoValidado != -1:
            itemEditado = editarItem(
                dataframeParaLista(listaDeItens)[itemASerEditadoValidado - 1]
            )
            listaDeItens = excluiItemDoDataFrame(
                listaDeItens, itemASerEditadoValidado - 1
            )
            return adicionarLinhaAoDataframe(listaDeItens, [itemEditado])


def filtraItens(array: object, termoDeBusca: str):
    arrayDeValidos = []
    for linha in array:
        arrayDeValidos.append(
            bool(re.search(termoDeBusca, linha[0], re.IGNORECASE))
            or bool(re.search(termoDeBusca, linha[1], re.IGNORECASE))
            or bool(re.search(termoDeBusca, linha[2], re.IGNORECASE))
        )
    return arrayDeValidos


def buscaItensNoCardapio(listaDeItens: object):
    while True:
        termoDeBusca = leEntradaDoUsuario(
            "Digite uma categoria, subcategoria ou item ou 0 para sair da busca: "
        )
        if termoDeBusca == "0":
            return
        arrayDoDataFrame = dataframeParaLista(listaDeItens)
        arrayComOsItensPesquisados = arrayDoDataFrame[
            filtraItens(arrayDoDataFrame, termoDeBusca)
        ]
        dataframeComOsItensPesquisados = listaParaDataFrame(arrayComOsItensPesquisados)
        listaItensDoCardapioCompleto(dataframeComOsItensPesquisados)
        if len(arrayComOsItensPesquisados) == 0:
            print("Desculpe, nenhum item encontrado com o termo pesquisado!\n ")


def arquivoComCardapioExiste(nomeArquivo: str):
    return os.path.isfile(nomeArquivo)


def salvaCardapio(dataframe: object):
    dataframe.to_csv("cardapio.csv", index=False)


def CriaArquivoDeCardapio():
    cardapio = pd.DataFrame(
        [], columns=["Categoria", "Subcategoria", "NomeItem", "ValorItem"]
    )
    salvaCardapio(cardapio)


def adicionarItemAoPedido(cardapio: object):
    while True:
        listaItensDoCardapioCompacta(cardapio)
        itemASerAdicionado = leEntradaDoUsuario(
            "Digite o item a ser adicionado ao pedido, ou 0 para retornar ao menu anterior: "
        )
        if itemASerAdicionado == "0":
            return
        itemASerAdicionadoValidado = entradaEntreDoisNumeros(
            itemASerAdicionado, 1, len(cardapio)
        )
        if itemASerAdicionadoValidado != -1:
            cardapioLista = dataframeParaLista(cardapio)
            return cardapioLista[itemASerAdicionadoValidado - 1]
        print("Item invalido")


def fecharPedido(pedido: object):
    pedidoDataframe = listaParaDataFrame(pedido)
    ValortotalDoPedido = pedidoDataframe[["ValorItem"]].sum()
    limpaATela()
    print("============================")
    print("Pedido finalizado. Itens do pedido:\n")
    print(pedidoDataframe[["NomeItem", "ValorItem"]])
    print("")
    print(f"Valor total dos itens: {formataNumeroComVirgula(ValortotalDoPedido)}")
    print(f"Taxa de serviço: {formataNumeroComVirgula(ValortotalDoPedido*0.1)}")
    print(
        f"Valor total do pedido: {formataNumeroComVirgula(ValortotalDoPedido + ValortotalDoPedido*0.1)}"
    )
    print()
    return


def realizarPedido(cardapio: object):
    pedido = []
    limpaATela()
    while True:
        entradaUsuario = leEntradaDoUsuario(
            "Digite 1 para adicionar algo ao pedido ou 0 para fechar a conta: "
        )
        if entradaUsuario == "1":
            pedido.append(adicionarItemAoPedido(cardapio))
        elif entradaUsuario == "0":
            fecharPedido(pedido)
            leEntradaDoUsuario("Aperte uma tecla para retornar ao menu anterior")
            return
        else:
            print(
                "Entrada invalida, digite 1 para adicionar um item ao pedido ou 0 para fechar o pedido"
            )


"""
itens = [
    ["Bebida", "Refrigerante", "Coca-cola", 5.5],
    ["Bebida", "Café", "Café coado médio", 8.9],
    ["Prato principal", "Prato feito", "Alcatra acebolada", 36.9],
    ["Bebida", "Café", "Café coado grande", 10.9],
    ["Bebida", "Água", "Água copo", 3.9],
    ["Bebida", "Água", "Água garrafa(500ml)", 5.9],
    ["Prato principal", "Prato feito", "PF do dia", 26.9],
    ["Bebida", "Café", "Café coado pequeno", 6.9],
    ["Entrada", "Salgado", "Pão de queijo", 4.9],
    ["Prato principal", "Prato feito", "Frango grelhado", 29.9],
    ["Bebida", "Refrigerante", "Guarana", 5.5],
    ["Entrada", "Salada", "Caesar salad", 19.9],
]
df_itens = pd.DataFrame(
    itens, columns=["Categoria", "Subcategoria", "NomeItem", "ValorItem"]
)

df_itens.to_csv("cardapio.csv", index=False)

"""
if not arquivoComCardapioExiste("cardapio.csv"):
    CriaArquivoDeCardapio()
limpaATela()
imprimeLogo()
while True:
    cardapio = pd.read_csv("cardapio.csv")
    imprimeOpcoes()
    opcaoUsuario = leEntradaDoUsuario("Selecione uma opção entre 1 e 7: ")
    opcaoValidada = entradaEntreDoisNumeros(opcaoUsuario, 1, 7)
    if opcaoValidada == 1:
        cardapio = adicionarItemAoCardapio(cardapio)
        cardapio.to_csv("cardapio.csv", index=False)
        limpaATela()
        imprimeLogo()
    elif opcaoValidada == 2:
        cardapio = excluirItemDoCardapio(cardapio)
        cardapio.to_csv("cardapio.csv", index=False)
        limpaATela()
        imprimeLogo()
    elif opcaoValidada == 3:
        cardapio = alterarItemDoCardapio(cardapio)
        cardapio.to_csv("cardapio.csv", index=False)
        limpaATela()
        imprimeLogo()
    elif opcaoValidada == 4:
        buscaItensNoCardapio(cardapio)
        cardapio.to_csv("cardapio.csv", index=False)
        limpaATela()
        imprimeLogo()
    elif opcaoValidada == 5:
        listaItensDoCardapioCompleto(cardapio)
    elif opcaoValidada == 6:
        realizarPedido(cardapio)
        limpaATela()
        imprimeLogo()
    elif opcaoValidada == 7:
        print("Até logo!")
        break

"""
print("1 - Adicionar item ao cardapio") - Check
print("2 - Excluir item do cardapio") - Check
print("3 - Alterar item do cardapio") - Check
print("4 - Buscar item do cardapio") - Check
print("5 - Listar todos os itens do cardápio") - Check
print("6 - Sair") - Check
Persistencia de dados - Check
Função extra - A fazer
"""
