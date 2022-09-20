import user_interaction
import sys

if len(sys.argv) == 1:
    print('Question for user is mandatory.')
    exit(1)

argument = sys.argv[1]
response, offset = user_interaction.question(argument)
print(response)
exit(0)
