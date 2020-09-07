from Util.Excel_parse import HandleExcel


def test_data():
    exc = HandleExcel()
    exc_data = exc.get_all_data()
    result = []
    for item in exc_data:
        lst = []
        lst.append(item[0])
        lst.append(item[3].split('\n'))
        lst.append(item[5])
        result.append(lst)

    return result


if __name__ == "__main__":
    print(test_data())
