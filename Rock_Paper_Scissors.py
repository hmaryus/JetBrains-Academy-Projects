import random

# All the options for the game -- option: [win condition]
all_choices = {
               'rock': ['fire', 'scissors', 'snake', 'human', 'tree', 'wolf', 'sponge'],
               'gun': ['rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'wolf'],
               'lightning': ['gun', 'rock', 'fire', 'scissors', 'snake', 'human', 'tree'],
               'devil': ['lightning', 'gun', 'rock', 'fire', 'scissors', 'snake', 'human' ],
               'dragon': ['devil', 'lightning', 'gun', 'rock', 'fire', 'scissors', 'snake'],
               'water': ['dragon', 'devil', 'lightning', 'gun', 'rock', 'fire', 'scissors'],
               'air': ['water', 'dragon', 'devil', 'lightning', 'gun', 'rock', 'fire'],
               'paper': ['air', 'water', 'dragon', 'devil', 'lightning', 'gun', 'rock'],
               'sponge': ['paper', 'air', 'water', 'dragon', 'devil', 'lightning', 'gun'],
               'wolf': ['sponge', 'paper', 'air', 'water', 'dragon', 'devil', 'lightning'],
               'tree': ['wolf', 'sponge', 'paper', 'air', 'water', 'dragon', 'devil'],
               'human': ['tree', 'wolf', 'sponge', 'paper', 'air', 'water', 'dragon'],
               'snake': ['human', 'tree', 'wolf', 'sponge', 'paper', 'air', 'water'],
               'scissors': ['snake', 'human', 'tree', 'wolf', 'sponge', 'paper', 'air'],
               'fire': ['scissors', 'snake', 'human', 'tree', 'wolf', 'sponge', 'paper']
               }


def game(game_options, all_opt):
    with open('rating.txt', 'r+') as f:

        # Creating the dictionary with the Player names - ratings
        storage = {}

        for name in f:
            storage[name.split(' ')[0].strip()] = int(name.split(' ')[1].strip())

        if my_name not in storage:
            storage[my_name] = 0

        # Starting the game
        while True:
            my_input = input('> ')

            # AI choosing a random option from the list above
            AI_input = random.choice(game_options)


            # Creating the menu
            if my_input == '!exit':
                print('Bye!')
                break
            elif my_input == '!rating':
                print(f'Your rating: {storage[my_name]}')
                continue
            elif my_input not in game_options:
                print('Invalid input')
                continue


            # Game choices + updating the ratings
            if my_input == AI_input:
                print(f'There is a draw ({AI_input})')
                storage[my_name] += 50
            elif my_input in all_opt[AI_input]:
                print(f'Sorry, but the computer chose {AI_input}')
            else:
                print(f'Well done. The computer chose {AI_input} and failed')
                storage[my_name] += 100


            # Writing the new values into the .txt file
            f.seek(0)
            f.write('\n'.join([str(name) + ' ' + str(rating) for name,rating in storage.items()]))

    f.close()


# Asking for the name of the user
my_name = input('Enter your name: > ')
print(f'Hello, {my_name}')

options = input().split(',')
print("\nOkay, let's start")

if options == ['']:
    game(['rock', 'paper', 'scissors'], {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'})
else:
    # Creating a new dictionary for the new options
    new_choices = {}
    for opt in options:
        new_choices[opt] = all_choices[opt]
    game(options, new_choices)






