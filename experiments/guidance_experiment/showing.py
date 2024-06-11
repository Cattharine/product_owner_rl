import os

def main():
    current_dir = os.getcwd()
    content = os.listdir(current_dir)

    data_files = []
    for filename in content:
        if filename.startswith('guidance'):
            data_files.append(filename)
    print(data_files)

    with open('guidance_False_evals_2024-06-10-T-15-00-43.txt', 'r') as file:
        data = file.read()
    
    print(data)

    for item in eval(data):
        print(item)

if __name__ == '__main__':
    main()