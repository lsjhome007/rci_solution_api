# function for preprocess

# 성별
def gender_pre(gender):
    '''
    남자를 1 여성을 0으로 one-hot encoding
    '''
    if gender.startswith('남'):
        return 1
    elif gender.startswith('여'):
        return 0

# 할부금융 상품명

def inst_type_pre(inst_plan):
    '''
    만기시 원금을 적게 내는 순으로 점수를 높게 배분한다.
    정액불 : 7점
    유예할부 : 4점
    만기일시상환 : 1점
    '''
    if inst_plan == '정액불':
        return 7
    elif '유예할부' in inst_plan:
        return 4
    elif inst_plan == '만기일시상환':
        return 1
    
# 할부기간    
def duration_pre(duration):
    '''
    할부기간 전처리 함수
    37이 들어가면 37점
    13이 들어가면 25점
    12가 들어가면 12점
    '''
    
    if '37' in duration:
        return 37
    if '13' in duration:
        return 25        # 13 과 36 중앙값 반올림
    if '12' in duration:
        return 12
    
# 신용한도조회
def credit_check_pre(check):
    '''
    신용한도조회 전처리 함수
    승인 7점
    조건부 4점
    그 이외 1점
    '''
    if check == '승인':
        return 7
    elif check == '조건부':
        return 4
    else:
        return 1
    
# 신용등급
def credit_pre(credit):
    '''
    신용등급 전처리 함수
    1~로 시작하면 13점
    4~로 시작하면 9점
    7~로 시작하면 5점
    10으로 시작하거나 그 이외면 1점
    '''
    if credit.startswith('1~'):
        return 13
    elif credit.startswith('4~'):
        return 9
    elif credit.startswith('7~'):
        return 5
    elif credit.startswith('10') or credit.startswith('na'):
        return 1
    
    
__all__ = ['inst_plan_pre', 'duration_pre', 'credit_check_pre', 'credit_pre']