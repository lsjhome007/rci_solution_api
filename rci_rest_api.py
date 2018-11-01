import pickle
import argparse
import os

import numpy as np
import pandas as pd
from scipy.stats import percentileofscore
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

from preprocess.feature_prepro import gender_pre, credit_check_pre, credit_pre
from preprocess.scoring import BinaryToscore
from preprocess.make_rank import divide_by_percent

app = Flask(__name__)
api = Api(app)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
PRE_LOC = os.path.join(CUR_DIR, 'preprocess')
PC_SCORE_LOC = os.path.join(PRE_LOC, 'pc_score.pkl')
CATBOOST_LOC = os.path.join(PRE_LOC, 'catboost.pkl')
PROB_LIST_LOC = os.path.join(PRE_LOC, 'prob_list.pkl')

class Prediction(Resource):

    def arg_parse(self):
        """arg. parse"""

        parser = reqparse.RequestParser()
        parser.add_argument('age', type=int, default=40, help='연령대를 입력하세요. 예) 20')
        parser.add_argument('gender', type=str, default='남', help='Bad choice: {error_msg}, choose from [여, 남]', choices=['여', '남'])
        parser.add_argument('contract_month', type=int, default=7, help='Bad chocie: {error_msg}, choose from [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

        parser.add_argument('credit_check', type=str, default='승인', help='Bad choice: {error_msg}, choose from [승인, 조건부, 거절]', choices=['승인', '조건부', '거절'])

        parser.add_argument('credit', type=str, default='1~3', help='Bad choice: {error_msg}, choose from [1~3, 4~6, 7~9, 10이상]', choices=['1~3', '4~6', '7~9', '10이상'])

        parser.add_argument('postcode', type=str, default='16', help='우편번호 5자리중 2자리를 입력하시오 예) 07')

        parser.add_argument('car_price', type=int, default=25730000, help='차량가격을 숫자로 입력하세요')

        parser.add_argument('principal', type=int, default=20000000, help='할부원금을 숫자로 입력하세요')

        parser.add_argument('n_div', type=int, default=5, help='몇 등급으로 나누고 싶은지 입력하세요 예) 5')

        args = parser.parse_args()

        return args


    def preprocess(self):
        """전처리"""
        args = self.arg_parse()

        age = args.age
        gender = args.gender
        contract_month = args.contract_month
        credit_check = args.credit_check
        credit = args.credit
        postcode = args.postcode
        car_price = args.car_price
        principal = args.principal
        n_div = args.n_div

        # 전처리 필요한 내용들 전처리
        age = age
        gender = gender_pre(gender)
        contract_month = contract_month
        credit_check = credit_check_pre(credit_check)
        credit = credit_pre(credit)
        
        ## pc_score.to_score를 실행시키기 위한 피클파일 load
        with open(PC_SCORE_LOC, 'rb') as f:
            pc_score = pickle.load(f)
        postcode = pc_score.to_score(postcode)

        car_price = car_price
        principal = principal
        principal_ratio = principal / car_price

        return {'age': age, 'gender': gender, 'contract_month': contract_month, 'credit_check': credit_check, 'credit': credit, 'postcode': postcode, 'car_price': car_price, 'principal': principal, 'principal_ratio': principal_ratio,'n_div': n_div}

    
    def predict(self):
        
        # preprocess 내용 불러오기
        args = self.preprocess()
        n_div = args['n_div']
        
        # 불러온 내용 불러오고 reshape
        feature_array = np.array(
                (args['age'], args['gender'], args['contract_month'], args['credit_check'], args['credit'], args['postcode'], args['car_price'], args['principal'], args['principal_ratio'])
                )
        feature_array = feature_array.reshape(1, -1)

        # fit이 되어 있는 catboost 객체 파일 불러오기
        with open(CATBOOST_LOC, 'rb') as f:
            catboost = pickle.load(f)
        # 보험 가입할 확률
        predict_proba = round(catboost.predict_proba(feature_array)[:, 1][0], 4)
        # n_div에 따라 보험 가입 등급 매기기
        with open(PROB_LIST_LOC, 'rb') as f:
            prob_list = pickle.load(f)
        pct = 1 - (percentileofscore(prob_list, predict_proba) / 100)
        rank = divide_by_percent(pct, n_div)


        return {'predict_proba': predict_proba, 'rank': rank}



    def post(self):
        
        prediction = self.predict()
        return prediction


api.add_resource(Prediction, '/predict')

if __name__ == '__main__':

    app.run(host='0.0.0.0')

