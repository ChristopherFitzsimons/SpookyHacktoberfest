from socket import socket
import time
run = True

while run == True:
    found_numbers = {0:"",1:"",2:"",3:"",4:""}
    maybe_numbers = []
    output = []
    sock = socket()
    sock.connect(('austiccquals.cyber.uq.edu.au', 3005))
    sock.send(b'01234\n')
    response = str(sock.recv(1024))
    output.append(response)
    split = response.split('\\n')
    try:
        guess = split[7]
        result = split[8]
    except:
        print(split)
    zero,one,two,three,four = guess.split(' ')
    zero_result,one_result,two_result,three_result,four_result = result.split(' ')
    print(guess+"\n"+result)
    time.sleep(0.25)
    sock.send(b'56789\n')
    response = str(sock.recv(1024))
    output.append(response)
    split = response.split('\\n')
    try:
        guess2 = split[1]
        result2 = split[2]
    except:
        print(split)
    print(guess2+"\n"+result2)
    five,six,seven,eight,nine = guess2.split(' ')
    five_result,six_result,seven_result,eight_result,nine_result = result2.split(' ')
    time.sleep(0.25)
    if zero_result == "=":
        found_numbers[0] = zero
    elif five_result == "=":
        found_numbers[0] = five
    if zero_result == "+":
        maybe_numbers.append(zero)
    if five_result == "+":
        maybe_numbers.append(five)

    if one_result == "=":
        found_numbers[1] = one
    elif six_result == "=":
        found_numbers[1] = six
    if one_result == "+":
        maybe_numbers.append(one)
    if six_result == "+":
        maybe_numbers.append(six)

    if two_result == "=":
        found_numbers[2] = two
    elif seven_result == "=":
        found_numbers[2] = seven
    if two_result == "+":
        maybe_numbers.append(two)
    if seven_result == "+":
        maybe_numbers.append(seven)

    if three_result == "=":
        found_numbers[3] = three
    elif eight_result == "=":
        found_numbers[3] = eight
    if three_result == "+":
        maybe_numbers.append(three)
    if eight_result == "+":
        maybe_numbers.append(eight)

    if four_result == "=":
        found_numbers[4] = four
    elif nine_result == "=":
        found_numbers[4] = nine
    if four_result == "+":
        maybe_numbers.append(four)
    if nine_result == "+":
        maybe_numbers.append(nine)
    print(found_numbers)
    print(maybe_numbers)

    count = 0
    for x in found_numbers:
        if found_numbers[x] == "":
            count += 1

    if count == 2 and len(maybe_numbers) == 2:
        run = False
        guess3 = found_numbers
        first = True
        for y in guess3:
            if guess3[y] == "" and first == True:
                guess3[y] = maybe_numbers[1]
                first = False
            elif guess3[y] == "" and first == False:
                guess3[y] = maybe_numbers[0]
        string = ""
        for z in guess3:
            string = string+str(guess3[z])
        string = string+'\n'
        print(string)
        sock.send(bytes(string, "utf8"))
        response = str(sock.recv(8192))
        print(response)
        output.append(response)

    print(count)
    if "Congratulations" in str(output):
        print(str(output))