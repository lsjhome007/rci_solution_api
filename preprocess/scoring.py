import pandas as pd

class BinaryToscore:
    '''    
    타겟값(Y)가 이 있는 경우 카테고리 피처를 실수형으로 변환시키기 위한 방법이다.
    가령 보험가입여부 예측을 하는 경우 샘플(잠재고객)의 우편번호 앞 2자리(지역번호)와 
    보험가입여부에 관한 데이터가 있다고 가정하자.
    
    해당 클래스는 특정 우편번호의 보험 가입 빈도수를 기준으로 점수를 매기게 해 준다.
    가장 보험 가입 빈도수가 높은 지역의 우편번호를 100점으로 환산하며, 보험 가입 경험이 없는 지역의 경우 0점으로 환산한다.
    
    클래스를 선언하고 to_score method를 pandas apply에 사용할 수 있다.
    
    cl_score = Score_100(df, column, tg_col, tgc_val)
    df['some_column'].apply(cl_score.to_score)
    
    Parameters
    ----------
    df : dataframe
         작업을 진행할 데이터 프레임을 뜻한다.
    
    column : str
             점수를 매길 칼럼명을 선택한다. 칼럼은 위 df dataframe 내부에 존재해야 한다.
    
    dic : None
          나중에 입력을 받기 위한 값. 기본값 None이 세팅되어 있으니 신경쓰지 않아도 됨.
    
    tgc_col : str
              점수를 매기는 기준 칼럼명을 뜻한다.
              해당 클래스는 카디프 프로젝트가 진행중이라 default로 'insurance_check' 칼럼명이 설정되어 있다.
    
    tgc_val : str
              기준 칼럼명의 값 중 어느 값을 기준으로 점수를 매길지를 설정한다.
              현재 'Y' 값이 디폴트로 세팅되어 있다.        
              
    '''
    
    def __init__(self, df: pd.DataFrame, column: str, dic=None, tgc_col: str ='insurance_check', tgc_val: str ='Y') -> dict:
        self.df = df
        self.column = column
        self.dic = dic
        self.tgc_col = tgc_col
        self.tgc_val = tgc_val
    
    @property
    def to_100_score_dict(self):
        '''
        {'1': 51.83823529411765,
         '10': 14.88970588235294,
         '100': 16.727941176470587,
         '101': 17.09558823529412 ...}
        '''
        score_01 = self.df[self.df[self.tgc_col] == self.tgc_val][self.column].value_counts()
        score_02 = score_01 / score_01.max() * 100 # value, 빈도수 100점 환산
        score_dict_01 = {a: b for a, b in zip(score_01.keys(), score_02.values)}
        self.dic = score_dict_01 # self.dic 에 딕셔너리 attribute를 추가한다.

    
    def to_score(self, value):
        if self.dic is None:
            self.to_100_score_dict
        return self.dic.get(value, 0)