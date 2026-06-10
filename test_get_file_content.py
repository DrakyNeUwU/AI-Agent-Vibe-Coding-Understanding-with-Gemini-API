from functions.get_file_content import get_file_content

# Test truncation
result = get_file_content("calculator", "lorem.txt")
print(f"lorem.txt length: {len(result)}")
print(f"lorem.txt truncated: {'truncated' in result}")
print()

# Test các case khác
result = get_file_content("calculator", "main.py")
print(f"main.py:\n{result}")
print()

result = get_file_content("calculator", "pkg/calculator.py")
print(f"pkg/calculator.py:\n{result}")
print()

result = get_file_content("calculator", "/bin/cat")
print(f"/bin/cat: {result}")
print()

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"pkg/does_not_exist.py: {result}")