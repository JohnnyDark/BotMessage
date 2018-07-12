from ConfigInfo import config_info
from all_methods import send_all_type, send_one_type, send_complex, BadRequestError

single_bot = config_info()['single_bot']
single_account = config_info()['single_account']


def message_bomb():
    # while True:
    while True:
        try:
            account_id = input('input an account_id: ')
            bot_num = eval(input('input a bot num: '))
            message_type = eval(input('input message type(1,2,3): '))

            if message_type == 1:
                send_all_type(account_id, bot_num)
                break
            elif message_type == 2:
                message_count = eval(input('how many messages you want to send: '))
                send_one_type(account_id, bot_num, message_count)
                break
            elif message_type == 3:
                message_count = eval(input('how many messages you want to send: '))
                send_complex(account_id, bot_num, message_count)
                break
            else:
                print('choose the message type number in (1,2,3)')
        except (SyntaxError, NameError):
            print("please input a integer")
            continue
        except BadRequestError:
            print("please check the bot number/accountId/image resourceId")
            continue


if __name__ == '__main__':
    message_bomb()
