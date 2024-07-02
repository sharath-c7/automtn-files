# check_pipe_format.py

def check_pipe_format(input_str):
    # Split the input string by '|'
    parts = input_str.split('|')
    fourth_chars={}
    for i in parts:
        if i == "":
            print("Incorrect Format")
            exit (1)

    for i in parts:
        if isinstance(i, str) and len(i) == 10:
            if i[:3] == "000":
                print(f"String '{i}' has length 10. and 1st 3 chars are 0")
            else:
                print(f"String '{i}' first 3 chars is not 0's")
                exit(1)     
        else:
            print(f"String '{i}' doesn't have length  10")
    
    i=0
    for i in parts:
        fourth_char=i[3]
        if fourth_char in fourth_chars:
            fourth_chars[fourth_char].append(i)
        else:
            fourth_chars[fourth_char] = [i]
    
    print(fourth_chars)
    
    for char, occurrences in fourth_chars.items():
        print(fourth_chars.items())
        if len(occurrences) == 1:
            print(f"The fourth character '{char}' is unique in {occurrences[0]}.")
        else:
            print(f"The fourth character '{char}' is not unique. Occurrences: {occurrences}")

if __name__ == "__main__":
    # Example usage:
    input_str1 = "0001asldkh|0002asdlkj|0003salkdj|0003loqifd"
    check_pipe_format(input_str1)




