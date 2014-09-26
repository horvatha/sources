import coding


def get_distribution_and_symbols(source_description):
    symbols = []
    distribution = []
    for i in source_description.split():
        symbol, probablity = i.split(':')
        symbols.append(symbol)
        probablity = float(probablity)
        distribution.append(probablity)
    return distribution, "".join(symbols)


def get_source(source_description):
    if source_description.startswith("fix:"):
        return coding.FixSource(source_description[4:])
    distribution, symbols = get_distribution_and_symbols(source_description)
    return coding.Source(distribution, symbols=symbols)


def get_code(code_description):
    code_description = code_description.replace(",", "  ")
    parts = code_description.split()
    list_of_pairs = [part.split(':', 1) for part in parts]
    symbols, codes = zip(*list_of_pairs)
    return coding.Code(" ".join(codes), symbols="".join(symbols))


def get_channel(channel_description):
    return coding.Channel(normalize(channel_description))


def normalize(channel_description):
    if isinstance(channel_description, str) and \
            channel_description.startswith("["):
        channel_description = eval(channel_description)
    return channel_description
