# -*- coding: utf-8 -*-

import pickle

import numpy as np
import pandas as pd
import argparse
from scipy.stats import percentileofscore

from preprocess_module.feature_prepro import gender_pre, inst_type_pre, duration_pre, credit_check_pre, credit_pre
from preprocess_module.scoring import BinaryToscore
from preprocess_module.make_rank import divide_by_percent


def arg_parse():
    
    '''
    파이썬 파일을 실행시킬때 argument들을 받고, 그 값을 리턴한다.
    자세한 사항은 cardif_solution_final.py -h 을 통해서 살펴볼 수 있다.
    '''

    parser = argparse.ArgumentParser(description='머신러닝 예측을 위한 데이터를 입력하세요')

    parser.add_argument('--age', type=int, default=40, help='연령대를 입력하세요. 예) 20', nargs='?')

    parser.add_argument('--gender', type=str, default='남', help='성별을 입력하세요. 예) 여', choices=['여', '남'], nargs='?')

    # parser.add_argument('--inst_type', type=str, default='정액불', help='할부금융 상품명을 입력하세요 예) 정액불', choices=['정액불', '유예할부', '만기일시상환', '계단식 보너스월 유예할부', '거치식 유예할부'], nargs='?')

    # parser.add_argument('--duration', type=str, default='37개월 이상', help='할부기간을 분류에 맞게 입력하세요 예) 37개월 이상', choices=['37개월 이상', '13개월 이상 36개월 이하', '12개월 이하'], nargs='?')

    parser.add_argument('--contract_month', type=int, default=7, help='할부계약 체결월을 입력하세요 예) 12', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], nargs='?')

    parser.add_argument('--credit_check', type=str, default='승인', help='신용한도조회 결과를 분류에 맞게 입력하세요 예) 승인', choices=['승인', '조건부', '거절'], nargs='?')

    parser.add_argument('--credit', type=str, default='1~3', help='신용등급을 분류에 맞게 입력하세요 예) 1~3', choices=['1~3', '4~6', '7~9', '10이상'], nargs='?')

    parser.add_argument('--postcode', type=str, default='16', help='우편번호 5자리 중 2자리를 입력하세요 예) 07', nargs='?')

    parser.add_argument('--car_price', type=int, default=25730000, help='차랑가격을 숫자로 입력하세요', nargs='?')

    parser.add_argument('--principal', type=int, default=20000000, help='할부원금을 숫자로 입력하세요', nargs='?')
    
    parser.add_argument('--n_div', type=int, default=5, help='몇 등급으로 나누고 싶은지 입력하세요 예) 5', nargs='?')

    args = parser.parse_args()
    
    age = args.age
    gender = args.gender
    # inst_type = args.inst_type
    # duration = args.duration
    contract_month = args.contract_month
    credit_check = args.credit_check
    credit = args.credit
    postcode = args.postcode
    car_price = args.car_price
    principal = args.principal
    n_div = args.n_div

    #return age, gender, inst_type, duration, contract_month, credit_check, credit, postcode, car_price, principal, n_div
    return age, gender, contract_month, credit_check, credit, postcode, car_price, principal, n_div

if __name__ == '__main__':

    # age, gender, inst_type, duration, contract_month, credit_check, credit, postcode, car_price, principal, n_div = arg_parse()  
    age, gender, contract_month, credit_check, credit, postcode, car_price, principal, n_div = arg_parse()
    # 전처리
    age = age
    gender = gender_pre(gender)
    # inst_type = inst_type_pre(inst_type)
    # duration = duration_pre(duration)
    contract_month = contract_month
    credit_check = credit_check_pre(credit_check)
    credit = credit_pre(credit)

    # pc_score.to_score를 실행시키기 위한 피클파일 load
    pc_score = pickle.load(open('./preprocess_module/pc_score.pkl', 'rb'))
    postcode = pc_score.to_score(postcode)
    car_price = car_price
    principal = principal
    principal_ratio = principal / car_price
    
    # 머신러닝 predict 가능한 형태로 변형
    # feature_array = np.array((age, gender, inst_type, duration, contract_month, credit_check, credit, postcode, car_price, principal, principal_ratio))
    feature_array = np.array((age, gender, contract_month, credit_check, credit, postcode, car_price, principal, principal_ratio))
    feature_array = feature_array.reshape(1, -1)
   
    # fit이 되어 있는 catboost 객체 파일 불러오기
    catboost = pickle.load(open('./preprocess_module/catboost.pkl', 'rb'))
    predict_proba = round(catboost.predict_proba(feature_array)[:, 1][0], 4)
    
    prob_list = pickle.load(open('./preprocess_module/prob_list.pkl', 'rb'))
    pct = 1- (percentileofscore(prob_list, predict_proba) / 100)
    rank = divide_by_percent(pct, n_div)
    
    print (f'가입확률: {predict_proba}, 고객등급: {rank}')
