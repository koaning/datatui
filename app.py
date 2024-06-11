from datatui import datatui

def generator():
    i = 0
    for i in range(100):
        yield {"content": f"example {i}"}
        i += 1

if __name__ == "__main__":
    datatui("annotations", list(generator()), "default", pbar=True)
