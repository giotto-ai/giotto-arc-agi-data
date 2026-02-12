from giotto_arc_data.load import load_dataset


def test_load():
    # load only a split
    data = load_dataset(stream=False, part="automata")
    print(len(data))

    assert len(data) > 0
    sample = data[0]

    assert isinstance(sample[0], str)
    assert isinstance(sample[1], dict)

    # load all the splis
    data = load_dataset(stream=False)
    print(len(data))

    assert len(data) > 0
    sample = data[0]

    assert isinstance(sample[0], str)
    assert isinstance(sample[1], dict)


# test_load()


def test_load_stream():

    # load only a split
    data_iterator = load_dataset(stream=True, part="automata")

    count = 0
    for sample in data_iterator:
        count += 1
    assert count > 0
    assert isinstance(sample[0], str)
    assert isinstance(sample[1], dict)

    # load all the splis
    data_iterator = load_dataset(stream=True)
    count = 0
    for sample in data_iterator:
        count += 1
    assert count > 0
    assert isinstance(sample[0], str)
    assert isinstance(sample[1], dict)
