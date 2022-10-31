import websocket
import sys
import json
import time
import re

# Adding Comment to know this is an approved script ;)

# Action (connect or steer)
action = sys.argv[1]
ignore = {}
win = False
# domain of the challange host
host = sys.argv[2]

if action == "connect":
    while win == False:
        ws = websocket.create_connection("wss://{}/ws".format(host))
        #ws.send('{"type": "START_GAME", "level": 1}')
        #ws.send('{ "type": "START_GAME", "level": 2, "password": "CTF{CapTA1n-cRUCh}" }')
        #ws.send('{ "type": "START_GAME", "level": 3, "password": "CTF{capt41n-h00k!}" }')
        #ws.send('{ "type": "START_GAME", "level": 4, "password": "CTF{c4pt41N-m0rG4N}" }')
        ws.send('{ "type": "START_GAME", "level": 5, "password": "CTF{C4pt41N-4MErIc4}" }')
        # Fith Flag CTF{CaPT41n-j4Ck-sp4rR0w}
        start = 0
        while True:
            data = json.loads(ws.recv())
            if data['type'] == 'GAME_START':
                obstructions = data['level']['board']['obstructions']
                level = data['level']['id']
                if level == 5:
                    #gate_one = 175
                    #gate_two = 250
                    gate_one = 200
                    gate_two = 260
                else:
                    gate_one = 650
                    gate_two = 900
            elif data['type'] == 'TICK':
                # Find out how many ships that are docked. Count will be the ID of ship we are docking
                target = len(re.findall("'isDocked': True", str(data)))
                for ship in data['ships']:
                    if ship['isDocked'] == False:
                        # To stop latantcy issues with ticks not showing update in placement this will check to see if the ship is not in the ignore list.
                        if ship['id'] not in ignore:
                            shipId = ship['id']
                            speed = ship['speed']
                            direction = ship['direction']
                            x_one = ship['area'][0]['x']
                            x_two = ship['area'][1]['x']
                            y_one = ship['area'][0]['y']
                            y_two = ship['area'][1]['y']
                            # Get all ships to turn so they are going UP or DOWN
                            if start == 5:
                                if direction == 'DOWN':
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                if direction == 'UP':
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                            if start == 5:
                                if direction == 'RIGHT':
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                            if start == 20:
                                if direction == 'LEFT':
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                            # Do different checks based on Direction
                            if direction == 'LEFT':
                                future_x_one = x_one - speed - 50
                                future_x_two = x_two - speed - 50
                                length = x_two - x_one
                                center = (x_one + (length / 2))
                                if speed > 12:
                                    center -= 20
                                elif speed > 10:
                                    center -= 10
                                if center > gate_one and center < gate_two:
                                    # Send ship into gate
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ignore[shipId] = speed + 10
                                elif center < 525 and y_one > 950:
                                    # Turn Ship UP to get it into position to turn between rocks
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ignore[shipId] = speed + 10
                                elif 30 >= future_x_one and 30 <= x_one or 30 >= future_x_two and 30 <= x_two:
                                    # Avoid Boarder
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ignore[shipId] = speed + 10
                                else:
                                    # Obsticle Avoidance
                                    for obstruction in obstructions:
                                        obstruction_x_one = obstruction['area'][0]['x']
                                        obstruction_x_two = obstruction['area'][1]['x']
                                        obstruction_y_one = obstruction['area'][0]['y']
                                        obstruction_y_two = obstruction['area'][1]['y']
                                        if obstruction_y_one >= y_one and obstruction_y_one <= y_two or obstruction_y_two >= y_one and obstruction_y_two <= y_two:
                                            if obstruction_x_one >= future_x_one and obstruction_x_one <= x_one or obstruction_x_one >= future_x_two and obstruction_x_one <= x_two:
                                                # Turn once so it moves the ship into position to go through gap in rocks (This was before static turn)
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ignore[shipId] = speed + 10
                                            elif obstruction_x_two >= future_x_one and obstruction_x_two <= x_one or obstruction_x_two >= future_x_two and obstruction_x_two <= x_two:
                                                # Turn once so it moves the ship into position to go through gap in rocks (This was before static turn)
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ignore[shipId] = speed + 10
                            elif direction == 'RIGHT':
                                future_x_one = x_one + speed + 50
                                future_x_two = x_two + speed + 50
                                if 1856 <= future_x_one and 1856 >= x_one or 1856 <= future_x_two and 1856 >= x_two:
                                    # Avoid Boarder
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ignore[shipId] = speed + 10
                                else:
                                    # Obsticle Avoidance
                                    for obstruction in obstructions:
                                        obstruction_x_one = obstruction['area'][0]['x']
                                        obstruction_x_two = obstruction['area'][1]['x']
                                        obstruction_y_one = obstruction['area'][0]['y']
                                        obstruction_y_two = obstruction['area'][1]['y']
                                        if obstruction_y_one >= y_one and obstruction_y_one <= y_two or obstruction_y_two >= y_one and obstruction_y_two <= y_two:
                                            if obstruction_x_one <= future_x_one and obstruction_x_one >= x_one or obstruction_x_one <= future_x_two and obstruction_x_one >= x_two:
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ignore[shipId] = speed + 10
                                            elif obstruction_x_two <= future_x_one and obstruction_x_two >= x_one or obstruction_x_two <= future_x_two and obstruction_x_two >= x_two:
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ignore[shipId] = speed + 10
                            elif direction == 'UP':
                                future_y_one = y_one - speed - 80
                                future_y_two = y_two - speed - 80
                                if 100 >= future_y_one and 100 <= y_one or 100 >= future_y_two and 100 <= y_two:
                                    if x_one > gate_one and x_one < gate_two or x_two > gate_one and x_two < gate_two:
                                        # Let it go through the gate
                                        ignore[shipId] = speed + 10
                                    else:
                                        # Avoid Boarder
                                        ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                        ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                        ignore[shipId] = speed + 10
                                #else:
                                #    Removed because they were rebounding on the gate
                                #    for obstruction in obstructions:
                                #        obstruction_x_one = obstruction['area'][0]['x']
                                #        obstruction_x_two = obstruction['area'][1]['x']
                                #        obstruction_y_one = obstruction['area'][0]['y']
                                #        obstruction_y_two = obstruction['area'][1]['y']
                                #        if obstruction_x_one >= x_one and obstruction_x_one <= x_two or obstruction_x_two >= x_one and obstruction_x_two <= x_two:
                                #            if obstruction_y_one >= future_y_one and obstruction_y_one <= y_one or obstruction_y_one >= future_y_two and obstruction_y_one <= y_two:
                                #                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                #                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                #                ignore[shipId] = speed + 10
                                #                #print(obstruction['type'], obstruction_y_one,y_one,future_y_one,y_two,future_y_two)
                                #            elif obstruction_y_two >= future_y_one and obstruction_y_two <= y_one or obstruction_y_two >= future_y_two and obstruction_y_two <= y_two:
                                #                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                #                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                #                ignore[shipId] = speed + 10
                                #                #print(obstruction['type'],obstruction_y_two,y_one,future_y_one,y_two,future_y_two)
                            if direction == 'DOWN':
                                future_y_one = y_one + speed + 50
                                future_y_two = y_two + speed + 50
                                length = y_one - y_two
                                center = ((y_two + (length / 2)))
                                if speed >= 12:
                                    center += 10
                                if shipId != target:
                                    # If the ship is not the target (Ship that needs docking)
                                    if 900 <= future_y_one and 900 >= y_one or 900 <= future_y_two and 900 >= y_two:
                                        # Avoid Boarder
                                        ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                        ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                        ignore[shipId] = speed + 10
                                elif 1178 <= future_y_one and 1178 >= y_one or 1178 <= future_y_two and 1178 >= y_two:
                                    # If the ship is about to hit the bottom boarder steer ship
                                    ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                    ignore[shipId] = speed
                                elif 500 >= x_one or 500 >= x_two:
                                    if center > 860 and center < 900:
                                        # Turn the ship through the gap in the rocks
                                        ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                        ignore[shipId] = 5
                                else:
                                    # Obsticle Avoidance
                                    for obstruction in obstructions:
                                        obstruction_x_one = obstruction['area'][0]['x']
                                        obstruction_x_two = obstruction['area'][1]['x']
                                        obstruction_y_one = obstruction['area'][0]['y']
                                        obstruction_y_two = obstruction['area'][1]['y']
                                        if obstruction_x_one >= x_one and obstruction_x_one <= x_two or obstruction_x_two >= x_one and obstruction_x_two <= x_two:
                                            if obstruction_y_one <= future_y_one and obstruction_y_one >= y_one or obstruction_y_one <= future_y_two and obstruction_y_one >= y_two:
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ignore[shipId] = speed + 10
                                            elif obstruction_y_two <= future_y_one and obstruction_y_two >= y_one or obstruction_y_two <= future_y_two and obstruction_y_two >= y_two:
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                                                ignore[shipId] = speed + 10
                        else:
                            # Removes a tick from the ignore list
                            if ignore[ship['id']] == 1:
                                del ignore[ship['id']]
                            else:
                                ignore[ship['id']] -= 1
                start += 1
            elif data['type'] == 'WIN':
                print(data)
                win = True
                break
            elif data['type'] == 'LOSS':
                print(data)
                break
            else:
                print(data)
elif action == "steer":
    # domain of the challange host
    host = sys.argv[2]
    ws = websocket.create_connection("wss://{}/ws".format(host))
    while True:
        userInput = input("Please give a ShipId: ")
        if userInput == "exit":
            break
        while True:
            try:
                steer = input("Enter to Steer: ")
                if steer == "exit":
                    break
                else:
                    shipId = int(userInput)
                    if shipId >= 0 and shipId <= 5:
                        ws.send('{"type": "SHIP_STEER", "shipId": '+str(shipId)+'}')
                        print("Ship "+str(shipId)+" Steered")
                    else:
                        print('No valid Id given')
            except:
                print("Invalid Input Given")
else:
    print('No action given to the script')
