from dotenv import dotenv_values

if __name__ == '__main__':
    config = dotenv_values(".env")
    DATA_ROOT = config['DATA_ROOT']
    print(DATA_ROOT)
