

    gold_standard = mh.imread(self.label_path)
    gs_binary = np.arange(len(gold_standard)*len(gold_standard[0])).reshape(len(gold_standard), len(gold_standard[0]))
    for row in range(len(gold_standard)):
        for col in range(len(gold_standard[0])):
            gs_binary[row][col] = f(gold_standard[row][col])
    self.labels = gs_binary