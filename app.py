from application import main
from libs import load_jieba_env

if __name__ == '__main__':
    # 初始化jieba分词环境
    load_jieba_env()

    # 执行flask
    main()
