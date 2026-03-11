from functions.get_files_info import get_files_info

def main():
    print("get_files_info(\"calculator\", \".\"):")
    print("Result for current directory:")
    result1 = get_files_info("calculator", ".")
    print("  " + result1.replace("\n", "\n  "))

    print("\nget_files_info(\"calculator\", \"pkg\"):")
    print("Result for 'pkg' directory:")
    result2 = get_files_info("calculator", "pkg")
    print("  " + result2.replace("\n", "\n  "))

    print("\nget_files_info(\"calculator\", \"/bin\"):")
    print("Result for '/bin' directory:")
    result3 = get_files_info("calculator", "/bin")
    print("    " + result3.replace("\n", "\n    "))

    print("\nget_files_info(\"calculator\", \"../\"):")
    print("Result for '../' directory:")
    result4 = get_files_info("calculator", "../")
    print("    " + result4.replace("\n", "\n    "))


if __name__ == "__main__":
    main()