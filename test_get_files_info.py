from functions.get_files_info import get_files_info


def test(wd: str, dir: str) -> None:
    result = get_files_info(wd, dir)

    print("Result for " + dir + " directory:")
    print(result)


test("calculator", ".")
test("calculator", "pkg")
test("calculator", "/bin")
test("calculator", "../")
