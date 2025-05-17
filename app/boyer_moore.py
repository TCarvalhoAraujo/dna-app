def preprocessar_bad_character(padrao):
    tabela = {}
    for i in range(len(padrao)):
        tabela[padrao[i]] = i
    return tabela

def preprocessar_good_suffix(padrao):
    m = len(padrao)
    suffix = [0] * m
    shift = [0] * m

    suffix[m - 1] = m
    g = m - 1
    f = 0
    for i in range(m - 2, -1, -1):
        if i > g and suffix[i + m - 1 - f] < i - g:
            suffix[i] = suffix[i + m - 1 - f]
        else:
            g = i
            f = i
            while g >= 0 and padrao[g] == padrao[g + m - 1 - f]:
                g -= 1
            suffix[i] = f - g

    for i in range(m):
        shift[i] = m
    j = 0
    for i in range(m - 1, -1, -1):
        if suffix[i] == i + 1:
            for j in range(m - 1 - i):
                if shift[j] == m:
                    shift[j] = m - 1 - i
    for i in range(m - 1):
        shift[m - 1 - suffix[i]] = m - 1 - i

    return shift

def boyer_moore(texto, padrao):
    n = len(texto)
    m = len(padrao)
    passos = []

    if m == 0:
        return [], passos

    bad_char = preprocessar_bad_character(padrao)
    good_suffix = preprocessar_good_suffix(padrao)

    resultados = []
    i = 0

    while i <= n - m:
        j = m - 1
        while j >= 0 and padrao[j] == texto[i + j]:
            j -= 1
        if j < 0:
            resultados.append(i)
            i += good_suffix[0]
        else:
            char_ruim = texto[i + j]
            deslocamento_ruim = j - bad_char.get(char_ruim, -1)
            deslocamento_bom = good_suffix[j]
            deslocamento = max(deslocamento_ruim, deslocamento_bom)
            i += deslocamento

    return resultados, passos