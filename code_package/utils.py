def generate_options(correct_translation, all_translations):
    """Генерируем список вариантов ответа."""
    import random
    options = [correct_translation]
    while len(options) < 4:
        option = random.choice(all_translations)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options