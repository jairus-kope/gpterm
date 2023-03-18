
def model_from_alias(alias):
    # see: https://beta.openai.com/docs/models
    alias_to_model = {'chatgpt': "gpt-3.5-turbo",
                      'davinci': "text-davinci-003",
                      'curie': "text-curie-001",
                      'babbage': "text-babbage-001",
                      'ada': "text-ada-001"}

    return alias_to_model.get(alias, alias)


def alias_for_model(model):
    model_to_alias = {"gpt-3.5-turbo": 'chatgpt',
                      "text-davinci-003": 'davinci',
                      "text-curie-001": 'curie',
                      "text-babbage-001": 'babbage',
                      "text-ada-001": 'ada'}

    return model_to_alias.get(model, model)


def model_name_for_print(model):
    model_alias = alias_for_model(model)
    model_name_print = f"{model}"
    if model_alias != model:
        model_name_print = f"{model_alias} ({model})"
    return model_name_print
