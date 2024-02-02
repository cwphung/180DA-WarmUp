import paho.mqtt.client as mqtt
import numpy as np
import time

def rock_paper_scissors():
    def on_connect(client, userdata, flags, rc):
        client.subscribe("ece180d/test/rps/1", qos=1)

    def on_disconnect(client, userdata, rc):
        if rc != 0:
            print('Unexpected Disconnect')
        else:
            print('Expected Disconnect')

    def on_message(client, userdata, message):
        nonlocal msg
        msg = message.payload.decode().lower()


    msg = None
    client = mqtt.Client(client_id="player2")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect_async('mqtt.eclipseprojects.io')
    client.loop_start()

    # Rock Paper Scissors
    user_input = input('Rock Paper Scissors: ').lower()
    client.publish("ece180d/test/rps/2", user_input, qos=1)

    while msg == None:
        time.sleep(0.1) 

    # Game Logic
    match user_input:
        case "rock":
            user = 1
        case "paper":
            user = 2
        case "scissors":
            user = 3
    
    p2 = 0
    match msg:
        case "rock":
            p2 = 1
            print("Player1: Rock")
        case "paper":
            p2 = 2
            print("Player1: paper")
        case "scissors":
            p2 = 3
            print("Player1: Scissors")

    diff = user - p2
    if diff == 0:
        print("Tie Game!")
    elif (diff % 3) == 1: 
        print("You win!")
    else:
        print("Player1 Wins!")

    client.loop_stop()
    client.disconnect()

while True:
    rock_paper_scissors()
    continue_input = input("Would you like to play again? Y/N ").lower()
    if continue_input != "y":
        break
